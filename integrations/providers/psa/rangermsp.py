"""
RangerMSP (CommitCRM) PSA Provider Integration

RangerMSP is a PSA platform by CommitCRM primarily for MSPs.
API Documentation: https://api.commitcrm.com/

Authentication: API Key authentication via query parameter or header
Base URL Format: https://api.commitcrm.com/api/v1
"""
import logging
from typing import List, Dict, Optional
from datetime import datetime
from ..base import BaseProvider, ProviderError, AuthenticationError

logger = logging.getLogger('integrations')


class RangerMSPProvider(BaseProvider):
    """
    RangerMSP (CommitCRM) integration provider.

    Required credentials:
        - api_key: API authentication key from RangerMSP settings
        - account_id: RangerMSP account identifier (if cloud hosted)

    Optional:
        - base_url: Custom URL if self-hosted (defaults to cloud API)
    """

    provider_name = 'RangerMSP'
    supports_companies = True
    supports_contacts = True
    supports_tickets = True
    supports_projects = False
    supports_agreements = True

    def __init__(self, connection):
        super().__init__(connection)
        # Default to cloud API if not specified
        if not self.base_url or self.base_url == 'https://api.commitcrm.com':
            self.base_url = 'https://api.commitcrm.com/api/v1'

    def _get_auth_headers(self):
        """
        RangerMSP uses API key authentication.
        Can be passed via header or query parameter.
        """
        api_key = self.credentials.get('api_key', '')

        if not api_key:
            raise AuthenticationError("Missing RangerMSP API key")

        return {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def test_connection(self) -> bool:
        """
        Test API connectivity by fetching account info or user info.
        """
        try:
            # Try fetching accounts to verify connection
            response = self._make_request('GET', '/accounts', params={'pageSize': 1})
            return response.status_code == 200
        except Exception as e:
            logger.error(f"RangerMSP connection test failed: {e}")
            return False

    def list_companies(self, page_size=100, updated_since=None) -> List[Dict]:
        """
        List companies (accounts) from RangerMSP.
        RangerMSP calls them "Accounts" in the API.
        """
        companies = []
        page = 1

        params = {
            'pageSize': page_size,
        }

        if updated_since:
            # RangerMSP uses lastModifiedDate for filtering
            params['lastModifiedDate'] = updated_since.strftime('%Y-%m-%dT%H:%M:%SZ')

        while True:
            params['page'] = page

            try:
                response = self._make_request('GET', '/accounts', params=params)
                data = response.json()

                # RangerMSP returns {results: [...], totalCount: X, page: X, pageSize: X}
                results = data.get('results', []) if isinstance(data, dict) else data

                if not results:
                    break

                for raw_company in results:
                    companies.append(self.normalize_company(raw_company))

                # Check if more pages exist
                if isinstance(data, dict):
                    total_count = data.get('totalCount', 0)
                    if page * page_size >= total_count:
                        break

                if len(results) < page_size:
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching RangerMSP companies page {page}: {e}")
                raise ProviderError(f"Failed to fetch companies: {e}")

        return companies

    def get_company(self, company_id: str) -> Dict:
        """
        Get single company (account) by ID.
        """
        try:
            response = self._make_request('GET', f'/accounts/{company_id}')
            return self.normalize_company(response.json())
        except Exception as e:
            logger.error(f"Error fetching RangerMSP company {company_id}: {e}")
            raise ProviderError(f"Failed to fetch company: {e}")

    def list_contacts(self, company_id: Optional[str] = None, page_size=100, updated_since=None) -> List[Dict]:
        """
        List contacts from RangerMSP.
        """
        contacts = []
        page = 1

        params = {
            'pageSize': page_size,
        }

        if company_id:
            params['accountId'] = company_id

        if updated_since:
            params['lastModifiedDate'] = updated_since.strftime('%Y-%m-%dT%H:%M:%SZ')

        while True:
            params['page'] = page

            try:
                response = self._make_request('GET', '/contacts', params=params)
                data = response.json()

                results = data.get('results', []) if isinstance(data, dict) else data

                if not results:
                    break

                for raw_contact in results:
                    contacts.append(self.normalize_contact(raw_contact))

                if isinstance(data, dict):
                    total_count = data.get('totalCount', 0)
                    if page * page_size >= total_count:
                        break

                if len(results) < page_size:
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching RangerMSP contacts page {page}: {e}")
                raise ProviderError(f"Failed to fetch contacts: {e}")

        return contacts

    def list_tickets(self, company_id: Optional[str] = None, status: Optional[str] = None,
                     updated_since: Optional[datetime] = None, page_size=100) -> List[Dict]:
        """
        List tickets from RangerMSP.
        RangerMSP calls them "Tickets" or "Service Tickets".
        """
        tickets = []
        page = 1

        params = {
            'pageSize': page_size,
        }

        if company_id:
            params['accountId'] = company_id

        if status:
            # Map standard status to RangerMSP status
            status_map = {
                'open': 'Open',
                'in_progress': 'In Progress',
                'waiting': 'Pending',
                'resolved': 'Resolved',
                'closed': 'Closed',
            }
            params['status'] = status_map.get(status, status)

        if updated_since:
            params['lastModifiedDate'] = updated_since.strftime('%Y-%m-%dT%H:%M:%SZ')

        while True:
            params['page'] = page

            try:
                response = self._make_request('GET', '/tickets', params=params)
                data = response.json()

                results = data.get('results', []) if isinstance(data, dict) else data

                if not results:
                    break

                for raw_ticket in results:
                    tickets.append(self.normalize_ticket(raw_ticket))

                if isinstance(data, dict):
                    total_count = data.get('totalCount', 0)
                    if page * page_size >= total_count:
                        break

                if len(results) < page_size:
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching RangerMSP tickets page {page}: {e}")
                raise ProviderError(f"Failed to fetch tickets: {e}")

        return tickets

    def get_ticket(self, ticket_id: str) -> Dict:
        """
        Get single ticket by ID.
        """
        try:
            response = self._make_request('GET', f'/tickets/{ticket_id}')
            return self.normalize_ticket(response.json())
        except Exception as e:
            logger.error(f"Error fetching RangerMSP ticket {ticket_id}: {e}")
            raise ProviderError(f"Failed to fetch ticket: {e}")

    def list_agreements(self, company_id: Optional[str] = None) -> List[Dict]:
        """
        List agreements/contracts from RangerMSP.
        RangerMSP calls them "Contracts" or "Agreements".
        """
        agreements = []
        page = 1
        page_size = 100

        params = {
            'pageSize': page_size,
        }

        if company_id:
            params['accountId'] = company_id

        while True:
            params['page'] = page

            try:
                response = self._make_request('GET', '/contracts', params=params)
                data = response.json()

                results = data.get('results', []) if isinstance(data, dict) else data

                if not results:
                    break

                for raw_agreement in results:
                    agreements.append(self.normalize_agreement(raw_agreement))

                if isinstance(data, dict):
                    total_count = data.get('totalCount', 0)
                    if page * page_size >= total_count:
                        break

                if len(results) < page_size:
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching RangerMSP agreements page {page}: {e}")
                raise ProviderError(f"Failed to fetch agreements: {e}")

        return agreements

    def normalize_company(self, raw_data: Dict) -> Dict:
        """
        Normalize RangerMSP account to standard company format.

        RangerMSP account structure:
        {
            "accountId": "A001",
            "accountName": "Acme Corporation",
            "status": "Active",
            "phone": "+1-555-1234",
            "email": "info@acme.com",
            "website": "https://acme.com",
            "address1": "123 Main St",
            "address2": "Suite 100",
            "city": "New York",
            "state": "NY",
            "zipCode": "10001",
            "country": "USA",
            "lastModifiedDate": "2025-01-15T10:30:00Z"
        }
        """
        # Build full address string
        address_parts = [
            raw_data.get('address1', ''),
            raw_data.get('address2', ''),
            raw_data.get('city', ''),
            raw_data.get('state', ''),
            raw_data.get('zipCode', ''),
            raw_data.get('country', ''),
        ]
        full_address = ', '.join(filter(None, address_parts))

        return {
            'external_id': str(raw_data.get('accountId', '')),
            'name': raw_data.get('accountName', ''),
            'status': 'active' if raw_data.get('status', '').lower() == 'active' else 'inactive',
            'phone': raw_data.get('phone', ''),
            'email': raw_data.get('email', ''),
            'website': raw_data.get('website', ''),
            'address': full_address,
            'raw_data': raw_data,
        }

    def normalize_contact(self, raw_data: Dict) -> Dict:
        """
        Normalize RangerMSP contact to standard format.

        RangerMSP contact structure:
        {
            "contactId": "C001",
            "accountId": "A001",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@acme.com",
            "phone": "+1-555-5678",
            "mobile": "+1-555-9012",
            "title": "IT Manager",
            "isPrimary": true,
            "isActive": true
        }
        """
        return {
            'external_id': str(raw_data.get('contactId', '')),
            'company_id': str(raw_data.get('accountId', '')),
            'first_name': raw_data.get('firstName', ''),
            'last_name': raw_data.get('lastName', ''),
            'email': raw_data.get('email', ''),
            'phone': raw_data.get('phone', '') or raw_data.get('mobile', ''),
            'title': raw_data.get('title', ''),
            'is_primary': raw_data.get('isPrimary', False),
            'is_active': raw_data.get('isActive', True),
            'raw_data': raw_data,
        }

    def normalize_ticket(self, raw_data: Dict) -> Dict:
        """
        Normalize RangerMSP ticket to standard format.

        RangerMSP ticket structure:
        {
            "ticketId": "T001",
            "accountId": "A001",
            "contactId": "C001",
            "subject": "Email not working",
            "description": "User cannot send emails",
            "status": "Open",
            "priority": "High",
            "assignedTo": "tech@msp.com",
            "createdDate": "2025-01-15T09:00:00Z",
            "lastModifiedDate": "2025-01-15T10:30:00Z",
            "resolvedDate": null,
            "closedDate": null
        }
        """
        # Map RangerMSP status to standard status
        status_map = {
            'open': 'open',
            'in progress': 'in_progress',
            'pending': 'waiting',
            'resolved': 'resolved',
            'closed': 'closed',
        }

        ranger_status = raw_data.get('status', '').lower()
        standard_status = status_map.get(ranger_status, 'open')

        # Parse dates
        created_at = self._parse_datetime(raw_data.get('createdDate'))
        updated_at = self._parse_datetime(raw_data.get('lastModifiedDate'))
        resolved_at = self._parse_datetime(raw_data.get('resolvedDate'))
        closed_at = self._parse_datetime(raw_data.get('closedDate'))

        return {
            'external_id': str(raw_data.get('ticketId', '')),
            'company_id': str(raw_data.get('accountId', '')),
            'contact_id': str(raw_data.get('contactId', '')),
            'title': raw_data.get('subject', ''),
            'description': raw_data.get('description', ''),
            'status': standard_status,
            'priority': raw_data.get('priority', 'medium').lower(),
            'assigned_to': raw_data.get('assignedTo', ''),
            'created_at': created_at,
            'updated_at': updated_at,
            'resolved_at': resolved_at,
            'closed_at': closed_at,
            'raw_data': raw_data,
        }

    def normalize_agreement(self, raw_data: Dict) -> Dict:
        """
        Normalize RangerMSP contract/agreement to standard format.

        RangerMSP contract structure:
        {
            "contractId": "CT001",
            "accountId": "A001",
            "contractName": "Managed Services Agreement",
            "contractType": "Monthly",
            "status": "Active",
            "startDate": "2025-01-01",
            "endDate": "2025-12-31",
            "monthlyValue": 2500.00,
            "billCycle": "Monthly"
        }
        """
        return {
            'external_id': str(raw_data.get('contractId', '')),
            'company_id': str(raw_data.get('accountId', '')),
            'name': raw_data.get('contractName', ''),
            'type': raw_data.get('contractType', ''),
            'status': raw_data.get('status', 'active').lower(),
            'start_date': self._parse_date(raw_data.get('startDate')),
            'end_date': self._parse_date(raw_data.get('endDate')),
            'monthly_value': raw_data.get('monthlyValue', 0.0),
            'billing_cycle': raw_data.get('billCycle', 'monthly'),
            'raw_data': raw_data,
        }

    def _parse_datetime(self, date_string):
        """Parse datetime from RangerMSP format."""
        if not date_string:
            return None
        try:
            # RangerMSP uses ISO 8601 format
            from dateutil import parser
            return parser.parse(date_string)
        except:
            return None

    def _parse_date(self, date_string):
        """Parse date from RangerMSP format."""
        if not date_string:
            return None
        try:
            from dateutil import parser
            return parser.parse(date_string).date()
        except:
            return None
