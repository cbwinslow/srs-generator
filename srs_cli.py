#!/usr/bin/env python3
"""
SRS Generator CLI Tool

A command-line tool for downloading, initializing, and syncing SRS documents
with GitHub Issues and Projects v2.

Can be run with: uvx srs-cli or pipx run srs-cli
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


class SRSCli:
    """CLI for SRS document management and GitHub sync."""
    
    def __init__(self, github_token: Optional[str] = None):
        """Initialize CLI with optional GitHub token."""
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if self.github_token:
            self.headers["Authorization"] = f"Bearer {self.github_token}"
    
    def init_srs(self, path: str = ".", template: str = "default") -> None:
        """Initialize a new SRS document in the specified path."""
        target_path = Path(path).resolve()
        target_path.mkdir(parents=True, exist_ok=True)
        
        srs_file = target_path / "SRS.md"
        
        if srs_file.exists():
            print(f"⚠️  SRS.md already exists at {srs_file}")
            response = input("Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                return
        
        # Create default SRS template
        template_content = self._get_template(template)
        
        with open(srs_file, 'w') as f:
            f.write(template_content)
        
        print(f"✓ Initialized SRS document at {srs_file}")
        
        # Create .srs-config.json
        config = {
            "template": template,
            "github": {
                "enabled": False,
                "repo": "",
                "sync_issues": False,
                "sync_projects": False
            }
        }
        
        config_file = target_path / ".srs-config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Created configuration at {config_file}")
        print("\nNext steps:")
        print("1. Edit .srs-config.json to configure GitHub sync")
        print("2. Run 'srs-cli sync' to sync with GitHub")
    
    def _get_template(self, template_name: str) -> str:
        """Get SRS template content."""
        default_template = """# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
<!-- Describe the purpose of this SRS document -->

### 1.2 Scope
<!-- Define the scope of the software system -->

### 1.3 Definitions and Acronyms
<!-- List key terms and abbreviations -->

## 2. System Description

### 2.1 System Context
<!-- Describe the system in its operational context -->

### 2.2 System Features
<!-- List main features of the system -->

## 3. Functional Requirements

### 3.1 User Interface
<!-- Describe UI requirements -->

### 3.2 Core Functionality
<!-- Describe core functional requirements -->

## 4. Non-Functional Requirements

### 4.1 Performance
<!-- Performance requirements -->

### 4.2 Security
<!-- Security requirements -->

### 4.3 Reliability
<!-- Reliability requirements -->

## 5. System Constraints

### 5.1 Technical Constraints
<!-- Technical limitations -->

### 5.2 Business Constraints
<!-- Business limitations -->

## 6. External Interface Requirements

### 6.1 User Interfaces
<!-- UI specifications -->

### 6.2 Hardware Interfaces
<!-- Hardware interface specifications -->

### 6.3 Software Interfaces
<!-- Software interface specifications -->

### 6.4 Communication Interfaces
<!-- Communication protocol specifications -->

## 7. System Features

<!-- Detailed feature descriptions -->

## 8. Appendix

### 8.1 Assumptions
<!-- List assumptions made -->

### 8.2 Dependencies
<!-- List dependencies -->

---

*Generated with SRS Generator CLI*
*Synced with GitHub: No*
"""
        return default_template
    
    def pull_issues(self, repo: str, output_file: str = "srs_issues.json") -> None:
        """Pull issues from GitHub repository."""
        if not self.github_token:
            print("❌ GitHub token required. Set GITHUB_TOKEN environment variable.")
            return
        
        print(f"📥 Pulling issues from {repo}...")
        
        url = f"{self.api_base}/repos/{repo}/issues"
        params = {
            "state": "all",
            "labels": "srs-generation,requirements",
            "per_page": 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            issues = response.json()
            
            # Filter and transform issues
            srs_items = []
            for issue in issues:
                item = {
                    "number": issue["number"],
                    "title": issue["title"],
                    "body": issue["body"],
                    "state": issue["state"],
                    "labels": [label["name"] for label in issue["labels"]],
                    "created_at": issue["created_at"],
                    "updated_at": issue["updated_at"],
                    "url": issue["html_url"]
                }
                srs_items.append(item)
            
            # Save to file
            with open(output_file, 'w') as f:
                json.dump(srs_items, f, indent=2)
            
            print(f"✓ Pulled {len(srs_items)} issues to {output_file}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error pulling issues: {e}")
    
    def pull_projects(self, repo: str, output_file: str = "srs_projects.json") -> None:
        """Pull Projects v2 items from GitHub repository."""
        if not self.github_token:
            print("❌ GitHub token required. Set GITHUB_TOKEN environment variable.")
            return
        
        print(f"📥 Pulling Projects v2 items from {repo}...")
        
        # First, get the organization/user from repo
        owner = repo.split('/')[0]
        
        # Query for projects using GraphQL API
        query = """
        query($owner: String!) {
          repositoryOwner(login: $owner) {
            ... on Organization {
              projectsV2(first: 10) {
                nodes {
                  id
                  title
                  number
                  url
                  items(first: 100) {
                    nodes {
                      id
                      content {
                        ... on Issue {
                          number
                          title
                          body
                          state
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
              projectsV2(first: 10) {
                nodes {
                  id
                  title
                  number
                  url
                  items(first: 100) {
                    nodes {
                      id
                      content {
                        ... on Issue {
                          number
                          title
                          body
                          state
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
                print(f"❌ GraphQL errors: {data['errors']}")
                return
            
            projects = data.get("data", {}).get("repositoryOwner", {}).get("projectsV2", {}).get("nodes", [])
            
            # Transform project items
            srs_projects = []
            for project in projects:
                project_data = {
                    "id": project["id"],
                    "title": project["title"],
                    "number": project["number"],
                    "url": project["url"],
                    "items": []
                }
                
                for item in project.get("items", {}).get("nodes", []):
                    content = item.get("content")
                    if content:
                        project_item = {
                            "id": item["id"],
                            "number": content.get("number"),
                            "title": content.get("title"),
                            "body": content.get("body"),
                            "state": content.get("state"),
                            "labels": [label["name"] for label in content.get("labels", {}).get("nodes", [])]
                        }
                        project_data["items"].append(project_item)
                
                srs_projects.append(project_data)
            
            # Save to file
            with open(output_file, 'w') as f:
                json.dump(srs_projects, f, indent=2)
            
            total_items = sum(len(p["items"]) for p in srs_projects)
            print(f"✓ Pulled {len(srs_projects)} projects with {total_items} items to {output_file}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error pulling projects: {e}")
    
    def push_to_issue(self, repo: str, title: str, body: str, labels: List[str] = None) -> None:
        """Push SRS content as a new GitHub issue."""
        if not self.github_token:
            print("❌ GitHub token required. Set GITHUB_TOKEN environment variable.")
            return
        
        print(f"📤 Creating issue in {repo}...")
        
        url = f"{self.api_base}/repos/{repo}/issues"
        
        data = {
            "title": title,
            "body": body,
            "labels": labels or ["srs-generation", "documentation"]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            issue = response.json()
            print(f"✓ Created issue #{issue['number']}: {issue['html_url']}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating issue: {e}")
    
    def sync(self, config_path: str = ".srs-config.json") -> None:
        """Sync SRS document with GitHub based on config."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            print(f"❌ Config file not found: {config_path}")
            print("Run 'srs-cli init' to create a new SRS document with config.")
            return
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        github_config = config.get("github", {})
        
        if not github_config.get("enabled"):
            print("⚠️  GitHub sync is not enabled in config.")
            return
        
        repo = github_config.get("repo")
        if not repo:
            print("❌ GitHub repo not specified in config.")
            return
        
        print(f"🔄 Syncing with {repo}...")
        
        if github_config.get("sync_issues"):
            self.pull_issues(repo)
        
        if github_config.get("sync_projects"):
            self.pull_projects(repo)
        
        print("✓ Sync complete!")
    
    def download_template(self, template_name: str = "default", output: str = "SRS_template.md") -> None:
        """Download an SRS template."""
        print(f"📥 Downloading {template_name} template...")
        
        template_content = self._get_template(template_name)
        
        with open(output, 'w') as f:
            f.write(template_content)
        
        print(f"✓ Template downloaded to {output}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SRS Generator CLI - Manage and sync SRS documents with GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize a new SRS document
  srs-cli init
  
  # Initialize in a specific directory
  srs-cli init --path ./docs
  
  # Download a template
  srs-cli download --template default --output SRS.md
  
  # Pull issues from GitHub
  srs-cli pull-issues --repo owner/repo
  
  # Pull Projects v2 items
  srs-cli pull-projects --repo owner/repo
  
  # Push SRS as GitHub issue
  srs-cli push-issue --repo owner/repo --title "SRS v1.0" --file SRS.md
  
  # Sync with GitHub (uses .srs-config.json)
  srs-cli sync

Environment Variables:
  GITHUB_TOKEN    GitHub personal access token for API access
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new SRS document')
    init_parser.add_argument('--path', default='.', help='Path to initialize SRS (default: current directory)')
    init_parser.add_argument('--template', default='default', help='Template to use (default: default)')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download an SRS template')
    download_parser.add_argument('--template', default='default', help='Template name (default: default)')
    download_parser.add_argument('--output', default='SRS_template.md', help='Output file (default: SRS_template.md)')
    
    # Pull issues command
    pull_issues_parser = subparsers.add_parser('pull-issues', help='Pull issues from GitHub')
    pull_issues_parser.add_argument('--repo', required=True, help='GitHub repository (owner/repo)')
    pull_issues_parser.add_argument('--output', default='srs_issues.json', help='Output file (default: srs_issues.json)')
    
    # Pull projects command
    pull_projects_parser = subparsers.add_parser('pull-projects', help='Pull Projects v2 items from GitHub')
    pull_projects_parser.add_argument('--repo', required=True, help='GitHub repository (owner/repo)')
    pull_projects_parser.add_argument('--output', default='srs_projects.json', help='Output file (default: srs_projects.json)')
    
    # Push issue command
    push_issue_parser = subparsers.add_parser('push-issue', help='Push SRS as GitHub issue')
    push_issue_parser.add_argument('--repo', required=True, help='GitHub repository (owner/repo)')
    push_issue_parser.add_argument('--title', required=True, help='Issue title')
    push_issue_parser.add_argument('--file', required=True, help='SRS file to push')
    push_issue_parser.add_argument('--labels', nargs='+', default=['srs-generation', 'documentation'], help='Issue labels')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync with GitHub using config')
    sync_parser.add_argument('--config', default='.srs-config.json', help='Config file (default: .srs-config.json)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = SRSCli()
    
    # Execute command
    if args.command == 'init':
        cli.init_srs(args.path, args.template)
    
    elif args.command == 'download':
        cli.download_template(args.template, args.output)
    
    elif args.command == 'pull-issues':
        cli.pull_issues(args.repo, args.output)
    
    elif args.command == 'pull-projects':
        cli.pull_projects(args.repo, args.output)
    
    elif args.command == 'push-issue':
        # Read file content
        try:
            with open(args.file, 'r') as f:
                body = f.read()
            cli.push_to_issue(args.repo, args.title, body, args.labels)
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
    
    elif args.command == 'sync':
        cli.sync(args.config)


if __name__ == '__main__':
    main()
