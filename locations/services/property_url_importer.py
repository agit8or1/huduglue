"""
AI-Powered Property URL Import Service

Uses Claude AI to extract property data from property appraiser websites.
Works with Duval County and other property records sites.
"""

import requests
from anthropic import Anthropic
from django.conf import settings
import logging
from typing import Optional, Dict
import json

logger = logging.getLogger('locations')


class PropertyURLImporter:
    """Import property data from property appraiser URLs using AI."""

    def __init__(self):
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key is required for URL import")

        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = getattr(settings, 'CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')

    def import_from_url(self, url: str) -> Dict:
        """
        Import property data from a property appraiser URL.

        Args:
            url: Property appraiser detail page URL

        Returns:
            Dict with extracted property data
        """
        logger.info(f"Importing property data from URL: {url}")

        # Fetch the HTML content
        html_content = self._fetch_html(url)
        if not html_content:
            raise Exception("Could not fetch HTML from URL")

        # Use Claude to extract property data
        property_data = self._extract_with_ai(html_content, url)

        return property_data

    def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            return response.text

        except requests.RequestException as e:
            logger.error(f"Failed to fetch HTML: {e}")
            return None

    def _extract_with_ai(self, html_content: str, source_url: str) -> Dict:
        """Use Claude AI to extract property data from HTML."""

        # Truncate HTML if too long (keep first 50k chars to stay within context limits)
        if len(html_content) > 50000:
            html_content = html_content[:50000] + "\n... [truncated]"

        prompt = f"""You are analyzing property data from a property appraiser website.

Extract ALL available property information from the HTML below and return it as JSON.

Source URL: {source_url}

Look for these fields (extract whatever is available):
- building_sqft: Total building square footage (number only)
- lot_sqft: Lot/land square footage (number only)
- year_built: Year building was constructed (number only)
- property_type: Property classification (e.g., "Commercial Office", "Single Family", "Industrial")
- property_id: Parcel ID or property ID
- floors_count: Number of floors/stories (number only)
- bedrooms: Number of bedrooms (if residential)
- bathrooms: Number of bathrooms (if residential)
- owner_name: Property owner name
- owner_address: Owner mailing address
- assessed_value: Assessed value for tax purposes
- market_value: Market value
- legal_description: Legal property description
- zoning: Zoning classification
- land_use: Land use description
- address: Property street address
- city: City
- state: State
- zip_code: ZIP code
- county: County name

HTML Content:
{html_content}

Return ONLY a valid JSON object with the extracted data. Use null for any fields that are not found.
Example format:
{{
    "building_sqft": 5000,
    "year_built": 1995,
    "property_type": "Commercial Office",
    "property_id": "1442930000",
    "floors_count": 2,
    "owner_name": "ABC Company LLC",
    "assessed_value": 450000,
    "address": "230 Arlington Road",
    "city": "Jacksonville",
    "state": "FL",
    "zip_code": "32211",
    "county": "Duval"
}}"""

        try:
            logger.debug(f"Sending {len(html_content)} chars to Claude for extraction")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract the JSON response
            response_text = response.content[0].text.strip()
            logger.debug(f"Claude response: {response_text[:500]}")

            # Try to parse JSON from response
            # Handle markdown code blocks if present
            if response_text.startswith('```'):
                # Extract JSON from code block
                lines = response_text.split('\n')
                json_lines = []
                in_code_block = False
                for line in lines:
                    if line.strip().startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        json_lines.append(line)
                response_text = '\n'.join(json_lines)

            property_data = json.loads(response_text)

            # Add metadata
            property_data['source_url'] = source_url
            property_data['source'] = 'url_import'
            property_data['extraction_method'] = 'ai'

            logger.info(f"Successfully extracted property data: {property_data.get('property_id', 'unknown')} - {property_data.get('building_sqft', 'N/A')} sqft")

            return property_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI response: {e}")
            logger.error(f"Response text: {response_text}")
            raise Exception(f"AI returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"AI extraction failed: {e}", exc_info=True)
            raise Exception(f"Failed to extract property data: {e}")


def get_property_url_importer():
    """Get PropertyURLImporter instance."""
    return PropertyURLImporter()
