"""Tests for GitHub sync module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.github_sync import GitHubSync, GitHubSyncError


@pytest.fixture
def mock_github_sync():
    """Create a GitHubSync instance with mocked token."""
    with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
        return GitHubSync()


def test_github_sync_initialization():
    """Test GitHubSync initialization."""
    with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
        sync = GitHubSync()
        assert sync.token == 'test_token'
        assert sync.api_base == "https://api.github.com"
        assert 'Authorization' in sync.headers


def test_github_sync_no_token():
    """Test GitHubSync raises error without token."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(GitHubSyncError, match="GitHub token is required"):
            GitHubSync()


@patch('backend.github_sync.requests')
def test_fetch_issues(mock_requests, mock_github_sync):
    """Test fetching issues from GitHub."""
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            'number': 1,
            'title': 'Test Issue',
            'body': 'Test body',
            'state': 'open',
            'labels': [{'name': 'bug'}],
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-02T00:00:00Z',
            'html_url': 'https://github.com/test/repo/issues/1',
            'assignees': []
        }
    ]
    mock_requests.get.return_value = mock_response
    
    # Fetch issues
    issues = mock_github_sync.fetch_issues('test/repo')
    
    # Verify
    assert len(issues) == 1
    assert issues[0]['number'] == 1
    assert issues[0]['title'] == 'Test Issue'
    assert 'bug' in issues[0]['labels']


@patch('backend.github_sync.requests')
def test_fetch_issues_with_labels(mock_requests, mock_github_sync):
    """Test fetching issues with label filter."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_requests.get.return_value = mock_response
    
    mock_github_sync.fetch_issues('test/repo', labels=['bug', 'feature'])
    
    # Verify labels parameter was passed
    call_args = mock_requests.get.call_args
    assert 'bug,feature' in str(call_args)


@patch('backend.github_sync.requests')
def test_create_issue(mock_requests, mock_github_sync):
    """Test creating a GitHub issue."""
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        'number': 42,
        'title': 'New Issue',
        'html_url': 'https://github.com/test/repo/issues/42',
        'created_at': '2024-01-01T00:00:00Z'
    }
    mock_requests.post.return_value = mock_response
    
    result = mock_github_sync.create_issue(
        'test/repo',
        'New Issue',
        'Issue body',
        labels=['enhancement']
    )
    
    assert result['number'] == 42
    assert result['title'] == 'New Issue'


@patch('backend.github_sync.requests')
def test_update_issue(mock_requests, mock_github_sync):
    """Test updating a GitHub issue."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'number': 42,
        'title': 'Updated Issue',
        'html_url': 'https://github.com/test/repo/issues/42',
        'updated_at': '2024-01-02T00:00:00Z'
    }
    mock_requests.patch.return_value = mock_response
    
    result = mock_github_sync.update_issue(
        'test/repo',
        42,
        title='Updated Issue',
        state='closed'
    )
    
    assert result['number'] == 42
    assert result['title'] == 'Updated Issue'


@patch('backend.github_sync.requests')
def test_fetch_issues_error(mock_requests, mock_github_sync):
    """Test error handling when fetching issues."""
    import requests as real_requests
    mock_requests.exceptions = real_requests.exceptions
    mock_requests.get.side_effect = real_requests.exceptions.RequestException("API Error")
    
    with pytest.raises(GitHubSyncError, match="Failed to fetch issues"):
        mock_github_sync.fetch_issues('test/repo')


def test_export_to_srs_format(mock_github_sync):
    """Test exporting issues to SRS format."""
    issues = [
        {
            'number': 1,
            'title': 'User Authentication',
            'body': 'Implement user login',
            'state': 'open',
            'labels': ['feature', 'functional'],
            'url': 'https://github.com/test/repo/issues/1'
        },
        {
            'number': 2,
            'title': 'Performance Requirements',
            'body': 'Response time < 200ms',
            'state': 'open',
            'labels': ['non-functional', 'performance'],
            'url': 'https://github.com/test/repo/issues/2'
        }
    ]
    
    markdown = mock_github_sync.export_to_srs_format(issues)
    
    assert '# Requirements from GitHub Issues' in markdown
    assert 'User Authentication' in markdown
    assert 'Performance Requirements' in markdown
    assert 'Functional Requirements' in markdown
    assert 'Non-Functional Requirements' in markdown


def test_export_to_srs_format_exclude_closed(mock_github_sync):
    """Test exporting excludes closed issues by default."""
    issues = [
        {
            'number': 1,
            'title': 'Open Issue',
            'body': 'Content',
            'state': 'open',
            'labels': ['feature'],
            'url': 'https://github.com/test/repo/issues/1'
        },
        {
            'number': 2,
            'title': 'Closed Issue',
            'body': 'Content',
            'state': 'closed',
            'labels': ['feature'],
            'url': 'https://github.com/test/repo/issues/2'
        }
    ]
    
    markdown = mock_github_sync.export_to_srs_format(issues, include_closed=False)
    
    assert 'Open Issue' in markdown
    assert 'Closed Issue' not in markdown


@patch('backend.github_sync.requests')
def test_fetch_projects_v2(mock_requests, mock_github_sync):
    """Test fetching Projects v2 from GitHub."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'repositoryOwner': {
                'projectsV2': {
                    'nodes': [
                        {
                            'id': 'PVT_test',
                            'title': 'Test Project',
                            'number': 1,
                            'url': 'https://github.com/orgs/test/projects/1',
                            'shortDescription': 'Test description',
                            'public': True,
                            'items': {
                                'nodes': [
                                    {
                                        'id': 'PVTI_test',
                                        'content': {
                                            'number': 1,
                                            'title': 'Test Item',
                                            'body': 'Test body',
                                            'state': 'open',
                                            'url': 'https://github.com/test/repo/issues/1',
                                            'createdAt': '2024-01-01T00:00:00Z',
                                            'updatedAt': '2024-01-02T00:00:00Z',
                                            'labels': {'nodes': [{'name': 'feature'}]}
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    }
    mock_requests.post.return_value = mock_response
    
    projects = mock_github_sync.fetch_projects_v2('test')
    
    assert len(projects) == 1
    assert projects[0]['title'] == 'Test Project'
    assert len(projects[0]['items']) == 1
    assert projects[0]['items'][0]['title'] == 'Test Item'
