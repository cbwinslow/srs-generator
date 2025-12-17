# SRS CLI Tool Guide

A command-line tool for downloading, initializing, and syncing SRS documents with GitHub Issues and Projects v2.

## Installation

### Using uvx (Recommended)

```bash
# Run directly without installation
uvx srs-cli --help

# Or with pipx
pipx install git+https://github.com/cbwinslow/srs-generator.git
srs-cli --help
```

### Using pip

```bash
# Install from source
git clone https://github.com/cbwinslow/srs-generator.git
cd srs-generator
pip install -e .

# Or install directly
pip install git+https://github.com/cbwinslow/srs-generator.git
```

### Using the script directly

```bash
# Make executable
chmod +x srs_cli.py

# Run directly
./srs_cli.py --help
```

## Quick Start

### 1. Initialize a New SRS Document

```bash
# Initialize in current directory
srs-cli init

# Initialize in specific directory
srs-cli init --path ./docs

# Use a specific template
srs-cli init --template default --path ./requirements
```

This creates:
- `SRS.md` - The SRS document
- `.srs-config.json` - Configuration file for GitHub sync

### 2. Download a Template

```bash
# Download default template
srs-cli download

# Download to specific file
srs-cli download --output my_srs.md

# Download specific template
srs-cli download --template default --output SRS.md
```

### 3. Configure GitHub Sync

Edit `.srs-config.json`:

```json
{
  "template": "default",
  "github": {
    "enabled": true,
    "repo": "owner/repo-name",
    "sync_issues": true,
    "sync_projects": true
  }
}
```

Set your GitHub token:

```bash
export GITHUB_TOKEN="your_github_personal_access_token"
```

### 4. Sync with GitHub

```bash
# Sync using config file
srs-cli sync

# Specify custom config
srs-cli sync --config ./custom-config.json
```

## Commands

### `init` - Initialize SRS Document

Initialize a new SRS document with configuration.

```bash
srs-cli init [OPTIONS]
```

**Options:**
- `--path PATH` - Directory to initialize (default: current directory)
- `--template NAME` - Template to use (default: default)

**Example:**
```bash
# Create new SRS in docs folder
srs-cli init --path ./docs

# Create with custom template
srs-cli init --template minimal
```

### `download` - Download Template

Download an SRS template without initializing a project.

```bash
srs-cli download [OPTIONS]
```

**Options:**
- `--template NAME` - Template name (default: default)
- `--output FILE` - Output file (default: SRS_template.md)

**Example:**
```bash
# Download to specific file
srs-cli download --output requirements/SRS.md
```

### `pull-issues` - Pull GitHub Issues

Pull issues from a GitHub repository and save as JSON.

```bash
srs-cli pull-issues --repo OWNER/REPO [OPTIONS]
```

**Options:**
- `--repo OWNER/REPO` - GitHub repository (required)
- `--output FILE` - Output JSON file (default: srs_issues.json)

**Example:**
```bash
# Pull all issues
srs-cli pull-issues --repo cbwinslow/srs-generator

# Save to custom file
srs-cli pull-issues --repo myorg/myrepo --output ./data/issues.json
```

**Output Format:**
```json
[
  {
    "number": 123,
    "title": "Add user authentication",
    "body": "We need to implement user authentication...",
    "state": "open",
    "labels": ["feature", "high-priority"],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T14:20:00Z",
    "url": "https://github.com/owner/repo/issues/123"
  }
]
```

### `pull-projects` - Pull GitHub Projects v2

Pull Projects v2 items from a GitHub organization or user.

```bash
srs-cli pull-projects --repo OWNER/REPO [OPTIONS]
```

**Options:**
- `--repo OWNER/REPO` - GitHub repository (owner extracted)
- `--output FILE` - Output JSON file (default: srs_projects.json)

**Example:**
```bash
# Pull projects from organization
srs-cli pull-projects --repo myorg/myrepo

# Save to custom file
srs-cli pull-projects --repo myorg/myrepo --output ./data/projects.json
```

**Output Format:**
```json
[
  {
    "id": "PVT_kwDOABcDEF",
    "title": "Product Roadmap Q1",
    "number": 1,
    "url": "https://github.com/orgs/myorg/projects/1",
    "items": [
      {
        "id": "PVTI_lADOABcDEFzgA",
        "number": 123,
        "title": "Implement feature X",
        "body": "Details...",
        "state": "open",
        "labels": ["feature"]
      }
    ]
  }
]
```

### `push-issue` - Push SRS as GitHub Issue

Create a GitHub issue from an SRS document.

```bash
srs-cli push-issue --repo OWNER/REPO --title TITLE --file FILE [OPTIONS]
```

**Options:**
- `--repo OWNER/REPO` - GitHub repository (required)
- `--title TITLE` - Issue title (required)
- `--file FILE` - SRS markdown file (required)
- `--labels LABEL [LABEL...]` - Issue labels (default: srs-generation documentation)

**Example:**
```bash
# Create issue from SRS
srs-cli push-issue \
  --repo myorg/myrepo \
  --title "SRS v1.0 - Product Requirements" \
  --file SRS.md

# With custom labels
srs-cli push-issue \
  --repo myorg/myrepo \
  --title "Updated Requirements" \
  --file SRS.md \
  --labels requirements high-priority documentation
```

### `sync` - Sync with GitHub

Sync SRS document with GitHub based on configuration file.

```bash
srs-cli sync [OPTIONS]
```

**Options:**
- `--config FILE` - Config file (default: .srs-config.json)

**Example:**
```bash
# Sync with default config
srs-cli sync

# Use custom config
srs-cli sync --config ./my-config.json
```

## GitHub Authentication

The CLI requires a GitHub personal access token for API operations.

### Creating a Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "SRS CLI")
4. Select scopes:
   - `repo` (Full control of private repositories)
   - `read:org` (Read org and team membership)
   - `project` (Full control of projects)
5. Click "Generate token"
6. Copy the token immediately (you won't see it again!)

### Setting the Token

**Environment Variable (Recommended):**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
echo 'export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"' >> ~/.bashrc
source ~/.bashrc
```

**Or pass to commands:**
```bash
GITHUB_TOKEN="ghp_xxx" srs-cli pull-issues --repo owner/repo
```

## Configuration File

The `.srs-config.json` file controls sync behavior:

```json
{
  "template": "default",
  "github": {
    "enabled": true,
    "repo": "owner/repo-name",
    "sync_issues": true,
    "sync_projects": true
  }
}
```

**Fields:**
- `template` - Template name used for initialization
- `github.enabled` - Enable/disable GitHub sync
- `github.repo` - Target repository in `owner/repo` format
- `github.sync_issues` - Pull issues when syncing
- `github.sync_projects` - Pull projects when syncing

## Use Cases

### Use Case 1: Initialize New Project

```bash
# Create new project directory
mkdir my-project
cd my-project

# Initialize SRS
srs-cli init

# Edit .srs-config.json to add your GitHub repo
vim .srs-config.json

# Set GitHub token
export GITHUB_TOKEN="ghp_xxx"

# Sync with GitHub
srs-cli sync
```

### Use Case 2: Pull Requirements from GitHub

```bash
# Pull issues labeled as requirements
srs-cli pull-issues --repo myorg/myrepo --output requirements.json

# Pull project items
srs-cli pull-projects --repo myorg/myrepo --output projects.json

# Review the JSON files
cat requirements.json | jq '.[] | {number, title, labels}'
```

### Use Case 3: Push SRS to GitHub

```bash
# Create/update your SRS.md file
vim SRS.md

# Push as new issue
srs-cli push-issue \
  --repo myorg/myrepo \
  --title "Software Requirements Specification v2.0" \
  --file SRS.md \
  --labels srs-generation requirements documentation
```

### Use Case 4: Continuous Sync Workflow

```bash
# Initial setup
srs-cli init --path ./docs
cd docs

# Configure GitHub repo in .srs-config.json
# Set GITHUB_TOKEN

# Daily sync workflow
srs-cli sync                    # Pull latest from GitHub
vim SRS.md                      # Update SRS document
srs-cli push-issue \           # Push updates back
  --repo myorg/myrepo \
  --title "SRS Update $(date +%Y-%m-%d)" \
  --file SRS.md
```

### Use Case 5: Convert GitHub Issues to SRS

```bash
# Pull issues
srs-cli pull-issues --repo myorg/myrepo --output issues.json

# Convert to SRS format using Python
python << EOF
import json
from backend.github_sync import GitHubSync

with open('issues.json') as f:
    issues = json.load(f)

sync = GitHubSync()
srs_content = sync.export_to_srs_format(issues)

with open('SRS_from_issues.md', 'w') as f:
    f.write(srs_content)

print("✓ Created SRS_from_issues.md")
EOF
```

## Integration with Backend

The CLI uses the same `backend/github_sync.py` module as the web backend, ensuring consistency.

### Using in Python Code

```python
from backend.github_sync import GitHubSync

# Initialize
sync = GitHubSync(token="ghp_xxx")

# Fetch issues
issues = sync.fetch_issues("owner/repo", labels=["requirements"])

# Create issue
result = sync.create_issue(
    repo="owner/repo",
    title="New Requirement",
    body="## Description\n\nDetails here...",
    labels=["requirement", "high-priority"]
)

# Export to SRS format
srs_markdown = sync.export_to_srs_format(issues)
```

## Troubleshooting

### "GitHub token required"

**Problem:** CLI can't find GitHub token.

**Solution:**
```bash
export GITHUB_TOKEN="your_token_here"
# Or add to ~/.bashrc or ~/.zshrc
```

### "Failed to fetch issues: 404"

**Problem:** Repository not found or no access.

**Solutions:**
- Check repository name format: `owner/repo` (not URL)
- Verify token has `repo` scope
- Check repository exists and is accessible

### "GraphQL errors" when pulling projects

**Problem:** Token lacks project permissions.

**Solutions:**
- Regenerate token with `project` scope
- Verify organization allows project access
- Check if projects are public or you have access

### "requests library not found"

**Problem:** Missing dependency.

**Solution:**
```bash
pip install requests
```

### File not found when pushing issue

**Problem:** SRS file path incorrect.

**Solution:**
```bash
# Use full path or correct relative path
srs-cli push-issue --file ./SRS.md ...
# Or
srs-cli push-issue --file /full/path/to/SRS.md ...
```

## Tips and Best Practices

### 1. Keep Token Secure

- Never commit tokens to git
- Use environment variables
- Rotate tokens periodically
- Use fine-grained tokens when possible

### 2. Label Strategy

Use consistent labels for better organization:
- `srs-generation` - Issues created by SRS tool
- `requirements` - Requirement specifications
- `functional` - Functional requirements
- `non-functional` - Non-functional requirements
- `constraint` - System constraints

### 3. Sync Workflow

```bash
# Daily routine
cd project-docs
srs-cli sync              # Pull latest
git pull                  # Pull git changes
# Make updates to SRS.md
git add SRS.md
git commit -m "Update requirements"
git push
srs-cli push-issue ...   # Push to GitHub
```

### 4. Automation with Cron

```bash
# Add to crontab (crontab -e)
0 9 * * * cd /path/to/project && /path/to/srs-cli sync
```

### 5. CI/CD Integration

```yaml
# .github/workflows/sync-srs.yml
name: Sync SRS
on:
  schedule:
    - cron: '0 9 * * *'
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Sync SRS
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          pip install -e .
          srs-cli sync
```

## Advanced Usage

### Custom Templates

Create your own template by modifying `srs_cli.py`:

```python
def _get_template(self, template_name: str) -> str:
    if template_name == "minimal":
        return "# SRS\n\n## Requirements\n\n"
    elif template_name == "detailed":
        return "# Comprehensive SRS\n\n..."
    # ... add more templates
```

### Batch Operations

```bash
# Pull from multiple repos
for repo in "org/repo1" "org/repo2" "org/repo3"; do
  srs-cli pull-issues --repo "$repo" --output "issues_${repo//\//_}.json"
done

# Push to multiple repos
for repo in "org/repo1" "org/repo2"; do
  srs-cli push-issue --repo "$repo" --title "SRS v1.0" --file SRS.md
done
```

### Filtering and Processing

```bash
# Pull issues and filter by label using jq
srs-cli pull-issues --repo org/repo | \
  jq '[.[] | select(.labels | contains(["high-priority"]))]'

# Count issues by state
srs-cli pull-issues --repo org/repo | \
  jq 'group_by(.state) | map({state: .[0].state, count: length})'
```

## Support

For issues or questions:
- Review this guide and `USAGE_GUIDE.md`
- Check GitHub Issues: https://github.com/cbwinslow/srs-generator/issues
- Submit bug reports using the bug template

## Version History

- **v1.0.0** (2024): Initial release
  - Core CLI functionality
  - GitHub Issues sync
  - GitHub Projects v2 sync
  - Template system
  - Configuration management
