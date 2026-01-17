"""
GitHub API integration for bug reporting.
Handles creating issues and uploading attachments to GitHub.
"""
import requests
from typing import Optional, Dict, Any
from django.conf import settings
import base64


class GitHubAPIError(Exception):
    """Raised when GitHub API requests fail."""
    pass


class GitHubIssueCreator:
    """
    Helper class for creating GitHub issues via the GitHub API.
    Supports both system-wide PAT and user-provided credentials.
    """

    def __init__(self, token: str, repo: str = 'agit8or1/huduglue'):
        """
        Initialize GitHub API client.

        Args:
            token: GitHub Personal Access Token
            repo: Repository in format 'owner/repo'
        """
        self.token = token
        self.repo = repo
        self.api_base = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': f'HuduGlue/{settings.VERSION if hasattr(settings, "VERSION") else "dev"}'
        }

    def validate_token(self) -> bool:
        """
        Validate that the GitHub token has access to the repository.

        Returns:
            True if token is valid and has access, False otherwise
        """
        url = f'{self.api_base}/repos/{self.repo}'
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Create a new GitHub issue.

        Args:
            title: Issue title
            body: Issue body (markdown formatted)
            labels: List of label names to apply

        Returns:
            Dict with issue details including 'number' and 'html_url'

        Raises:
            GitHubAPIError: If issue creation fails
        """
        if labels is None:
            labels = ['bug', 'user-reported']

        url = f'{self.api_base}/repos/{self.repo}/issues'
        data = {
            'title': title,
            'body': body,
            'labels': labels
        }

        try:
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 201:
                return response.json()
            else:
                error_msg = f"GitHub API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_msg += f" - {error_data['message']}"
                except:
                    pass
                raise GitHubAPIError(error_msg)

        except requests.RequestException as e:
            raise GitHubAPIError(f"Network error creating issue: {str(e)}")

    def upload_image_to_issue(
        self,
        issue_number: int,
        image_data: bytes,
        filename: str
    ) -> str:
        """
        Upload an image as a comment attachment to an issue.

        Note: GitHub doesn't have a direct image upload API, so we'll
        add the image as a base64 encoded markdown comment.

        Args:
            issue_number: The issue number to attach to
            image_data: Raw image bytes
            filename: Original filename

        Returns:
            URL of the created comment

        Raises:
            GitHubAPIError: If upload fails
        """
        url = f'{self.api_base}/repos/{self.repo}/issues/{issue_number}/comments'

        # Encode image as base64 and create markdown
        b64_image = base64.b64encode(image_data).decode('utf-8')

        # Determine image type from filename
        extension = filename.lower().split('.')[-1]
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        mime_type = mime_types.get(extension, 'image/png')

        # Create markdown with embedded image
        comment_body = f"**Screenshot: {filename}**\n\n"
        comment_body += f"![{filename}](data:{mime_type};base64,{b64_image})"

        data = {'body': comment_body}

        try:
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 201:
                return response.json()['html_url']
            else:
                raise GitHubAPIError(f"Failed to upload image: {response.status_code}")

        except requests.RequestException as e:
            raise GitHubAPIError(f"Network error uploading image: {str(e)}")

    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get current API rate limit status.

        Returns:
            Dict with rate limit information
        """
        url = f'{self.api_base}/rate_limit'
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except requests.RequestException:
            return {}


def format_bug_report_body(
    description: str,
    steps_to_reproduce: str,
    system_info: Dict[str, str],
    reporter_info: Dict[str, str]
) -> str:
    """
    Format a bug report issue body in markdown.

    Args:
        description: Detailed bug description
        steps_to_reproduce: Steps to reproduce the issue
        system_info: System information dict
        reporter_info: Reporter information dict

    Returns:
        Markdown-formatted issue body
    """
    body = "## Description\n\n"
    body += f"{description}\n\n"

    if steps_to_reproduce and steps_to_reproduce.strip():
        body += "## Steps to Reproduce\n\n"
        body += f"{steps_to_reproduce}\n\n"

    body += "## System Information\n\n"
    body += f"- **HuduGlue Version**: {system_info.get('version', 'Unknown')}\n"
    body += f"- **Django Version**: {system_info.get('django_version', 'Unknown')}\n"
    body += f"- **Python Version**: {system_info.get('python_version', 'Unknown')}\n"
    body += f"- **Browser**: {system_info.get('browser', 'Unknown')}\n"
    body += f"- **OS**: {system_info.get('os', 'Unknown')}\n"
    body += f"- **Date**: {system_info.get('timestamp', 'Unknown')}\n\n"

    body += "## Reporter Information\n\n"
    body += f"- **Reported By**: {reporter_info.get('username', 'Unknown')}\n"
    if reporter_info.get('email'):
        body += f"- **Email**: {reporter_info.get('email')}\n"
    if reporter_info.get('organization'):
        body += f"- **Organization**: {reporter_info.get('organization')}\n"

    body += "\n---\n"
    body += "_This bug report was submitted via HuduGlue's built-in bug reporting feature._\n"

    return body
