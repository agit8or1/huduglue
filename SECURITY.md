# HuduGlue Security Documentation

## Overview

HuduGlue implements defense-in-depth security with multiple layers of protection. This document outlines security features, configuration, and best practices.

## Security Features Summary

### Authentication & Authorization
- Argon2 password hashing
- Mandatory 2FA (TOTP)
- Azure AD SSO
- Brute force protection (django-axes)
- Organization-based multi-tenancy
- Automated tenant isolation tests

### Data Protection
- AES-256-GCM encryption (Fernet)
- Encrypted credentials storage
- Field-level encryption with key rotation
- Separate keys per environment

### API Security
- DRF browsable API disabled in production
- JSON-only renderers in production
- Granular throttling (login, password reset, tokens, AI)
- API key authentication

### Web Security
- Strict CSP
- HSTS (1 year in production)
- Clickjacking protection
- Secure cookies (HttpOnly, Secure, SameSite)
- Permissions-Policy

### AI Protection
- Per-user/org request limits (100/day default)
- Per-user/org spend caps ($10/$100 default)
- Burst protection (10/minute)
- PII redaction
- Usage tracking

See full documentation: https://github.com/agit8or1/huduglue/blob/main/SECURITY.md
