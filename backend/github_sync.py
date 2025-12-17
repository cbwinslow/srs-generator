"""
GitHub Sync Module

Functions for syncing SRS documents with GitHub Issues and Projects v2.
Can be used by both the CLI and web backend.
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None


class GitHubSyncError(Exception):
    """Custom exception for GitHub sync errors."""
    pass


class GitHubSync:
    """Handle GitHub API operations for SRS document sync."""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub sync client.
        
        Args:
            token: GitHub personal access token. If not provided, will try to read from GITHUB_TOKEN env var.
        """
        if requests is None:
            raise GitHubSyncError("requests library is required. Install with: pip install requests")
        
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise GitHubSyncError("GitHub token is required. Provide token or set GITHUB_TOKEN environment variable.")
        
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def fetch_issues(self, repo: str, labels: Optional[List[str]] = None, state: str = "all") -> List[Dict[str, Any]]:
        """
        Fetch issues from a GitHub repository.
        
        Args:
            repo: Repository in format 'owner/repo'
            labels: Optional list of labels to filter by
            state: Issue state ('open', 'closed', 'all')
        
        Returns:
            List of issue dictionaries
        """
        url = f"{self.api_base}/repos/{repo}/issues"
        params = {
            "state": state,
            "per_page": 100
        }
        
        if labels:
            params["labels"] = ",".join(labels)
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            issues = response.json()
            
            # Transform to simplified format
            return [
                {
                    "number": issue["number"],
                    "title": issue["title"],
                    "body": issue["body"] or "",
                    "state": issue["state"],
                    "labels": [label["name"] for label in issue.get("labels", [])],
                    "created_at": issue["created_at"],
                    "updated_at": issue["updated_at"],
                    "url": issue["html_url"],
                    "assignees": [user["login"] for user in issue.get("assignees", [])],
                }
                for issue in issues
            ]
        
        except requests.exceptions.RequestException as e:
            raise GitHubSyncError(f"Failed to fetch issues: {str(e)}")
    
    def create_issue(self, repo: str, title: str, body: str, labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new GitHub issue.
        
        Args:
            repo: Repository in format 'owner/repo'
            title: Issue title
            body: Issue body (markdown)
            labels: Optional list of labels
        
        Returns:
            Created issue dictionary
        """
        url = f"{self.api_base}/repos/{repo}/issues"
        
        data = {
            "title": title,
            "body": body
        }
        
        if labels:
            data["labels"] = labels
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            issue = response.json()
            return {
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["html_url"],
                "created_at": issue["created_at"]
            }
        
        except requests.exceptions.RequestException as e:
            raise GitHubSyncError(f"Failed to create issue: {str(e)}")
    
    def update_issue(self, repo: str, issue_number: int, title: Optional[str] = None, 
                    body: Optional[str] = None, state: Optional[str] = None, 
                    labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update an existing GitHub issue.
        
        Args:
            repo: Repository in format 'owner/repo'
            issue_number: Issue number to update
            title: Optional new title
            body: Optional new body
            state: Optional new state ('open' or 'closed')
            labels: Optional new labels
        
        Returns:
            Updated issue dictionary
        """
        url = f"{self.api_base}/repos/{repo}/issues/{issue_number}"
        
        data = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state is not None:
            data["state"] = state
        if labels is not None:
            data["labels"] = labels
        
        try:
            response = requests.patch(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            issue = response.json()
            return {
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["html_url"],
                "updated_at": issue["updated_at"]
            }
        
        except requests.exceptions.RequestException as e:
            raise GitHubSyncError(f"Failed to update issue: {str(e)}")
    
    def fetch_projects_v2(self, owner: str) -> List[Dict[str, Any]]:
        """
        Fetch Projects v2 from a GitHub organization or user.
        
        Args:
            owner: Organization or user name
        
        Returns:
            List of project dictionaries with items
        """
        query = """
        query($owner: String!) {
          repositoryOwner(login: $owner) {
            ... on Organization {
              projectsV2(first: 20) {
                nodes {
                  id
                  title
                  number
                  url
                  shortDescription
                  public
                  items(first: 100) {
                    nodes {
                      id
                      content {
                        ... on Issue {
                          number
                          title
                          body
                          state
                          url
                          createdAt
                          updatedAt
                          labels(first: 10) {
                            nodes {
                              name
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            ... on User {
              projectsV2(first: 20) {
                nodes {
                  id
                  title
                  number
                  url
                  shortDescription
                  public
                  items(first: 100) {
                    nodes {
                      id
                      content {
                        ... on Issue {
                          number
                          title
                          body
                          state
                          url
                          createdAt
                          updatedAt
                          labels(first: 10) {
                            nodes {
                              name
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                "https://api.github.com/graphql",
                headers=self.headers,
                json={"query": query, "variables": {"owner": owner}}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                raise GitHubSyncError(f"GraphQL errors: {data['errors']}")
            
            projects_data = data.get("data", {}).get("repositoryOwner", {}).get("projectsV2", {}).get("nodes", [])
            
            # Transform to simplified format
            projects = []
            for project in projects_data:
                project_dict = {
                    "id": project["id"],
                    "title": project["title"],
                    "number": project["number"],
                    "url": project["url"],
                    "description": project.get("shortDescription", ""),
                    "public": project.get("public", False),
                    "items": []
                }
                
                for item in project.get("items", {}).get("nodes", []):
                    content = item.get("content")
                    if content:
                        project_item = {
                            "id": item["id"],
                            "number": content.get("number"),
                            "title": content.get("title"),
                            "body": content.get("body", ""),
                            "state": content.get("state"),
                            "url": content.get("url"),
                            "created_at": content.get("createdAt"),
                            "updated_at": content.get("updatedAt"),
                            "labels": [label["name"] for label in content.get("labels", {}).get("nodes", [])]
                        }
                        project_dict["items"].append(project_item)
                
                projects.append(project_dict)
            
            return projects
        
        except requests.exceptions.RequestException as e:
            raise GitHubSyncError(f"Failed to fetch projects: {str(e)}")
    
    def export_to_srs_format(self, issues: List[Dict[str, Any]], 
                            include_closed: bool = False) -> str:
        """
        Export issues to SRS markdown format.
        
        Args:
            issues: List of issue dictionaries
            include_closed: Whether to include closed issues
        
        Returns:
            Markdown formatted string
        """
        if not include_closed:
            issues = [i for i in issues if i["state"] == "open"]
        
        # Group issues by labels
        requirements = {}
        for issue in issues:
            labels = issue.get("labels", [])
            
            # Determine category
            category = "Other Requirements"
            if "functional" in labels or "feature" in labels:
                category = "Functional Requirements"
            elif "non-functional" in labels or "performance" in labels or "security" in labels:
                category = "Non-Functional Requirements"
            elif "constraint" in labels:
                category = "Constraints"
            
            if category not in requirements:
                requirements[category] = []
            
            requirements[category].append(issue)
        
        # Generate markdown
        markdown = "# Requirements from GitHub Issues\n\n"
        markdown += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        
        for category, items in sorted(requirements.items()):
            markdown += f"## {category}\n\n"
            
            for issue in items:
                markdown += f"### {issue['title']} (#{issue['number']})\n\n"
                markdown += f"**Status:** {issue['state'].upper()}\n\n"
                
                if issue['labels']:
                    markdown += f"**Labels:** {', '.join(issue['labels'])}\n\n"
                
                if issue['body']:
                    markdown += f"{issue['body']}\n\n"
                
                markdown += f"**Issue:** {issue['url']}\n\n"
                markdown += "---\n\n"
        
        return markdown
    
    def sync_issues_to_file(self, repo: str, output_file: str, labels: Optional[List[str]] = None) -> int:
        """
        Sync issues from GitHub to a local file.
        
        Args:
            repo: Repository in format 'owner/repo'
            output_file: Output file path
            labels: Optional labels to filter by
        
        Returns:
            Number of issues synced
        """
        issues = self.fetch_issues(repo, labels=labels)
        
        with open(output_file, 'w') as f:
            json.dump(issues, f, indent=2)
        
        return len(issues)
    
    def sync_projects_to_file(self, owner: str, output_file: str) -> int:
        """
        Sync Projects v2 from GitHub to a local file.
        
        Args:
            owner: Organization or user name
            output_file: Output file path
        
        Returns:
            Number of projects synced
        """
        projects = self.fetch_projects_v2(owner)
        
        with open(output_file, 'w') as f:
            json.dump(projects, f, indent=2)
        
        return len(projects)
