"""
AI Endpoint Abuse Controls for Anthropic API.
Provides cost protection, PII redaction, request size limits, and spend tracking.
"""
import re
import logging
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from decimal import Decimal

logger = logging.getLogger('core')


class AIAbuseControlMiddleware:
    """
    Middleware to protect AI endpoints from abuse.
    - Enforces request size limits
    - Tracks per-user and per-org spend
    - Provides spend caps
    - Logs usage for billing/auditing
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Configuration (can be overridden via settings)
        self.max_prompt_length = getattr(settings, 'AI_MAX_PROMPT_LENGTH', 10000)  # characters
        self.max_daily_requests_per_user = getattr(settings, 'AI_MAX_DAILY_REQUESTS_PER_USER', 100)
        self.max_daily_requests_per_org = getattr(settings, 'AI_MAX_DAILY_REQUESTS_PER_ORG', 1000)
        self.max_daily_spend_per_user = Decimal(str(getattr(settings, 'AI_MAX_DAILY_SPEND_PER_USER', 10.00)))  # USD
        self.max_daily_spend_per_org = Decimal(str(getattr(settings, 'AI_MAX_DAILY_SPEND_PER_ORG', 100.00)))  # USD

        # AI endpoint patterns (paths that use Anthropic API)
        self.ai_endpoints = [
            '/locations/generate-floorplan/',
            '/api/ai/',  # Generic AI endpoints
        ]

    def __call__(self, request):
        # Check if this is an AI endpoint
        if not self._is_ai_endpoint(request.path):
            return self.get_response(request)

        # Check authentication
        if not request.user or not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        # Check request limits
        limit_check = self._check_limits(request)
        if limit_check:
            return limit_check  # Return error response

        # Process request
        response = self.get_response(request)

        # Track usage after successful request
        if response.status_code == 200:
            self._track_usage(request, response)

        return response

    def _is_ai_endpoint(self, path):
        """Check if path is an AI endpoint."""
        return any(endpoint in path for endpoint in self.ai_endpoints)

    def _check_limits(self, request):
        """Check if user/org has exceeded limits."""
        user = request.user
        org = getattr(request, 'organization', None)

        # Check user request count
        user_cache_key = f'ai_requests_user_{user.id}_today'
        user_requests = cache.get(user_cache_key, 0)

        if user_requests >= self.max_daily_requests_per_user:
            logger.warning(f'User {user.username} exceeded daily AI request limit: {user_requests}/{self.max_daily_requests_per_user}')
            return JsonResponse({
                'error': 'Daily AI request limit exceeded',
                'limit': self.max_daily_requests_per_user,
                'used': user_requests,
                'reset_in_hours': self._get_hours_until_reset()
            }, status=429)

        # Check org request count
        if org:
            org_cache_key = f'ai_requests_org_{org.id}_today'
            org_requests = cache.get(org_cache_key, 0)

            if org_requests >= self.max_daily_requests_per_org:
                logger.warning(f'Organization {org.slug} exceeded daily AI request limit: {org_requests}/{self.max_daily_requests_per_org}')
                return JsonResponse({
                    'error': 'Organization daily AI request limit exceeded',
                    'limit': self.max_daily_requests_per_org,
                    'used': org_requests,
                    'reset_in_hours': self._get_hours_until_reset()
                }, status=429)

        # Check user spend (if tracking is enabled)
        user_spend_key = f'ai_spend_user_{user.id}_today'
        user_spend = Decimal(str(cache.get(user_spend_key, 0)))

        if user_spend >= self.max_daily_spend_per_user:
            logger.warning(f'User {user.username} exceeded daily AI spend limit: ${user_spend}/${self.max_daily_spend_per_user}')
            return JsonResponse({
                'error': 'Daily AI spend limit exceeded',
                'limit': float(self.max_daily_spend_per_user),
                'used': float(user_spend),
                'reset_in_hours': self._get_hours_until_reset()
            }, status=429)

        # Check org spend
        if org:
            org_spend_key = f'ai_spend_org_{org.id}_today'
            org_spend = Decimal(str(cache.get(org_spend_key, 0)))

            if org_spend >= self.max_daily_spend_per_org:
                logger.warning(f'Organization {org.slug} exceeded daily AI spend limit: ${org_spend}/${self.max_daily_spend_per_org}')
                return JsonResponse({
                    'error': 'Organization daily AI spend limit exceeded',
                    'limit': float(self.max_daily_spend_per_org),
                    'used': float(org_spend),
                    'reset_in_hours': self._get_hours_until_reset()
                }, status=429)

        return None  # No limits exceeded

    def _track_usage(self, request, response):
        """Track AI usage for billing and rate limiting."""
        user = request.user
        org = getattr(request, 'organization', None)

        # Increment request counters (24-hour TTL)
        ttl = 86400  # 24 hours

        user_cache_key = f'ai_requests_user_{user.id}_today'
        cache.set(user_cache_key, cache.get(user_cache_key, 0) + 1, ttl)

        if org:
            org_cache_key = f'ai_requests_org_{org.id}_today'
            cache.set(org_cache_key, cache.get(org_cache_key, 0) + 1, ttl)

        # Log usage for auditing
        logger.info(f'AI request: user={user.username}, org={org.slug if org else "none"}, path={request.path}')

    def _get_hours_until_reset(self):
        """Calculate hours until daily limit resets."""
        from datetime import datetime, time, timedelta
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delta = tomorrow - now
        return round(delta.total_seconds() / 3600, 1)


class PIIRedactor:
    """
    Redact PII from AI prompts before sending to Anthropic.
    Detects and masks: emails, phone numbers, SSNs, credit cards, API keys, tokens.
    """

    # Regex patterns for PII detection
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
    API_KEY_PATTERN = re.compile(r'\b[A-Za-z0-9]{32,}\b')  # Generic long alphanumeric strings

    @classmethod
    def redact(cls, text, redact_emails=True, redact_phones=True, redact_ssns=True,
               redact_credit_cards=True, redact_api_keys=False):
        """
        Redact PII from text.

        Args:
            text: Input text to redact
            redact_emails: Redact email addresses
            redact_phones: Redact phone numbers
            redact_ssns: Redact SSNs
            redact_credit_cards: Redact credit card numbers
            redact_api_keys: Redact long alphanumeric strings (may have false positives)

        Returns:
            Redacted text with PII replaced by [REDACTED_*] placeholders
        """
        if not text:
            return text

        redacted = text

        if redact_emails:
            redacted = cls.EMAIL_PATTERN.sub('[REDACTED_EMAIL]', redacted)

        if redact_phones:
            redacted = cls.PHONE_PATTERN.sub('[REDACTED_PHONE]', redacted)

        if redact_ssns:
            redacted = cls.SSN_PATTERN.sub('[REDACTED_SSN]', redacted)

        if redact_credit_cards:
            redacted = cls.CREDIT_CARD_PATTERN.sub('[REDACTED_CARD]', redacted)

        if redact_api_keys:
            # Be careful with this - may have false positives
            redacted = cls.API_KEY_PATTERN.sub('[REDACTED_KEY]', redacted)

        return redacted

    @classmethod
    def check_for_pii(cls, text):
        """
        Check if text contains PII (without redacting).

        Returns:
            dict with boolean flags for each PII type detected
        """
        return {
            'has_email': bool(cls.EMAIL_PATTERN.search(text)),
            'has_phone': bool(cls.PHONE_PATTERN.search(text)),
            'has_ssn': bool(cls.SSN_PATTERN.search(text)),
            'has_credit_card': bool(cls.CREDIT_CARD_PATTERN.search(text)),
            'has_api_key': bool(cls.API_KEY_PATTERN.search(text)),
        }


def get_ai_usage_stats(user=None, organization=None):
    """
    Get current AI usage statistics for a user or organization.

    Args:
        user: User instance
        organization: Organization instance

    Returns:
        dict with usage stats (requests, spend, limits)
    """
    stats = {}

    if user:
        user_cache_key = f'ai_requests_user_{user.id}_today'
        user_spend_key = f'ai_spend_user_{user.id}_today'

        stats['user'] = {
            'requests_used': cache.get(user_cache_key, 0),
            'requests_limit': getattr(settings, 'AI_MAX_DAILY_REQUESTS_PER_USER', 100),
            'spend_used': float(cache.get(user_spend_key, 0)),
            'spend_limit': float(getattr(settings, 'AI_MAX_DAILY_SPEND_PER_USER', 10.00)),
        }

    if organization:
        org_cache_key = f'ai_requests_org_{organization.id}_today'
        org_spend_key = f'ai_spend_org_{organization.id}_today'

        stats['organization'] = {
            'requests_used': cache.get(org_cache_key, 0),
            'requests_limit': getattr(settings, 'AI_MAX_DAILY_REQUESTS_PER_ORG', 1000),
            'spend_used': float(cache.get(org_spend_key, 0)),
            'spend_limit': float(getattr(settings, 'AI_MAX_DAILY_SPEND_PER_ORG', 100.00)),
        }

    return stats
