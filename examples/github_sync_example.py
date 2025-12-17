#!/usr/bin/env python3
"""
Example: Using the GitHub Sync Module

This example demonstrates how to use the backend.github_sync module
programmatically to sync SRS documents with GitHub.
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.github_sync import GitHubSync, GitHubSyncError


def example_fetch_issues():
    """Example: Fetch issues from a repository."""
    print("=" * 60)
    print("Example 1: Fetching Issues")
    print("=" * 60)
    
    # Note: This example requires GITHUB_TOKEN to be set
    if not os.getenv('GITHUB_TOKEN'):
        print("⚠️  GITHUB_TOKEN not set. Skipping live example.")
        print("   Set with: export GITHUB_TOKEN='your_token'")
        return
    
    try:
        # Initialize sync client
        sync = GitHubSync()
        
        # Fetch issues (replace with your repo)
        repo = "octocat/Hello-World"  # Example public repo
        print(f"Fetching issues from {repo}...")
        
        issues = sync.fetch_issues(
            repo=repo,
            labels=None,  # Get all issues
            state="open"  # Only open issues
        )
        
        print(f"✓ Found {len(issues)} open issues")
        
        # Display first few issues
        for i, issue in enumerate(issues[:3], 1):
            print(f"\n  {i}. #{issue['number']}: {issue['title']}")
            print(f"     Labels: {', '.join(issue['labels']) if issue['labels'] else 'None'}")
            print(f"     URL: {issue['url']}")
        
        if len(issues) > 3:
            print(f"\n  ... and {len(issues) - 3} more issues")
    
    except GitHubSyncError as e:
        print(f"❌ Error: {e}")


def example_create_issue():
    """Example: Create a new issue."""
    print("\n" + "=" * 60)
    print("Example 2: Creating an Issue")
    print("=" * 60)
    
    if not os.getenv('GITHUB_TOKEN'):
        print("⚠️  GITHUB_TOKEN not set. Skipping live example.")
        return
    
    # Demonstration only - uncomment to actually create an issue
    print("📝 Example code (not executed to avoid creating test issues):")
    print("""
    sync = GitHubSync()
    
    result = sync.create_issue(
        repo="owner/repo",
        title="SRS Requirements - v1.0",
        body=\"\"\"# Software Requirements Specification
        
## Overview
This issue contains the SRS document for our project.

## Requirements
1. User authentication
2. Data management
3. Reporting dashboard
        \"\"\",
        labels=["srs-generation", "documentation"]
    )
    
    print(f"✓ Created issue #{result['number']}")
    print(f"  URL: {result['url']}")
    """)


def example_export_to_srs():
    """Example: Export issues to SRS format."""
    print("\n" + "=" * 60)
    print("Example 3: Export Issues to SRS Format")
    print("=" * 60)
    
    # Create sample issues data
    sample_issues = [
        {
            'number': 1,
            'title': 'User Authentication',
            'body': 'Users must be able to log in with email and password.',
            'state': 'open',
            'labels': ['feature', 'functional'],
            'url': 'https://github.com/example/repo/issues/1'
        },
        {
            'number': 2,
            'title': 'Performance Requirements',
            'body': 'System must respond within 200ms for 95% of requests.',
            'state': 'open',
            'labels': ['non-functional', 'performance'],
            'url': 'https://github.com/example/repo/issues/2'
        },
        {
            'number': 3,
            'title': 'Database Constraints',
            'body': 'Must use PostgreSQL 14 or higher.',
            'state': 'open',
            'labels': ['constraint'],
            'url': 'https://github.com/example/repo/issues/3'
        }
    ]
    
    # Initialize sync (token not needed for export)
    try:
        sync = GitHubSync()
    except GitHubSyncError:
        # If no token, create a mock instance for export only
        sync = type('obj', (object,), {
            'export_to_srs_format': lambda self, issues, include_closed=False: 
                GitHubSync.__dict__['export_to_srs_format'](self, issues, include_closed)
        })()
    
    # Export to SRS format
    print("Converting issues to SRS markdown...")
    srs_content = sync.export_to_srs_format(sample_issues, include_closed=False)
    
    # Display result
    print("\n📄 Generated SRS Content:")
    print("-" * 60)
    print(srs_content[:500])  # First 500 characters
    print("...")
    print("-" * 60)
    
    # Save to file
    output_file = "/tmp/sample_srs_from_issues.md"
    with open(output_file, 'w') as f:
        f.write(srs_content)
    
    print(f"\n✓ Full SRS saved to: {output_file}")


def example_sync_workflow():
    """Example: Complete sync workflow."""
    print("\n" + "=" * 60)
    print("Example 4: Complete Sync Workflow")
    print("=" * 60)
    
    print("📋 Typical workflow:")
    print("""
1. Initialize sync client:
   sync = GitHubSync(token='your_token')

2. Fetch issues for requirements:
   issues = sync.fetch_issues(
       repo='owner/repo',
       labels=['requirements', 'feature']
   )

3. Export to SRS format:
   srs_markdown = sync.export_to_srs_format(issues)

4. Save to file:
   with open('SRS.md', 'w') as f:
       f.write(srs_markdown)

5. Push updated SRS back to GitHub:
   sync.create_issue(
       repo='owner/repo',
       title='Updated SRS Document',
       body=srs_markdown,
       labels=['documentation']
   )

6. Fetch Projects v2 items:
   projects = sync.fetch_projects_v2('organization')
   
7. Process project items:
   for project in projects:
       for item in project['items']:
           print(f"- {item['title']}")
    """)


def example_error_handling():
    """Example: Error handling."""
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    print("🛡️  Best practices for error handling:")
    print("""
from backend.github_sync import GitHubSync, GitHubSyncError

try:
    sync = GitHubSync()
    issues = sync.fetch_issues('owner/repo')
    
except GitHubSyncError as e:
    # Handle specific GitHub sync errors
    print(f"GitHub sync error: {e}")
    
except Exception as e:
    # Handle other unexpected errors
    print(f"Unexpected error: {e}")

# Check for token before operations
if not os.getenv('GITHUB_TOKEN'):
    print("Please set GITHUB_TOKEN environment variable")
    sys.exit(1)
    """)


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("GitHub Sync Module Examples")
    print("=" * 60)
    
    print("\n📚 These examples show how to use backend.github_sync")
    print("   programmatically in your Python code.")
    print()
    
    # Run examples
    example_fetch_issues()
    example_create_issue()
    example_export_to_srs()
    example_sync_workflow()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)
    print("\n💡 For more information:")
    print("   - See backend/github_sync.py for full API")
    print("   - See CLI_GUIDE.md for CLI usage")
    print("   - See USAGE_GUIDE.md for web interface")
    print()


if __name__ == '__main__':
    main()
