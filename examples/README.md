# SRS Generator Examples

This directory contains examples demonstrating various features of the SRS Generator.

## Available Examples

### 1. Interactive Mode API (`interactive_mode_example.py`) 🆕

Demonstrates the conversational AI agent for guided SRS generation.

```bash
# Make sure the server is running first
docker-compose up
# or
./run.sh

# Then run the example in another terminal
python3 interactive_mode_example.py
```

**What it shows:**
- Starting an interactive session
- Having a conversation with the AI agent
- Progressive information gathering
- Automatic SRS document generation
- Saving the generated document

### 2. CLI Tool Demo (`cli_demo.sh`)

Demonstrates the command-line interface for managing SRS documents.

```bash
# Run the demo
./cli_demo.sh
```

**What it shows:**
- Initializing a new SRS document
- Viewing generated files
- Downloading templates
- Configuration setup

### 2. GitHub Sync Module (`github_sync_example.py`)

Shows how to use the GitHub sync module programmatically in Python.

```bash
# Run the example
python3 github_sync_example.py
```

**What it covers:**
- Fetching issues from GitHub
- Creating issues
- Exporting issues to SRS format
- Complete sync workflows
- Error handling

## Prerequisites

### For Interactive Mode Examples

The server must be running:

```bash
# Option 1: Using Docker (recommended)
docker-compose up

# Option 2: Local development
./run.sh
```

The example will connect to `http://localhost:5000` by default.

### For CLI Examples

No additional setup required. The CLI tool works out of the box.

### For GitHub Sync Examples

Set your GitHub personal access token:

```bash
export GITHUB_TOKEN="your_github_token_here"
```

To create a token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `project`
4. Copy the token

## Example Workflows

### Basic SRS Initialization

```bash
# Initialize in current directory
srs-cli init

# Initialize in specific directory
srs-cli init --path ./my-project/docs
```

### Pull Requirements from GitHub

```bash
export GITHUB_TOKEN="your_token"

# Pull issues
srs-cli pull-issues --repo owner/repo --output requirements.json

# Pull Projects v2
srs-cli pull-projects --repo owner/repo --output projects.json
```

### Push SRS to GitHub

```bash
# Create/update SRS.md first
vim SRS.md

# Push as GitHub issue
srs-cli push-issue \
  --repo owner/repo \
  --title "Software Requirements Specification v1.0" \
  --file SRS.md \
  --labels srs-generation documentation
```

### Automated Sync

```bash
# Configure .srs-config.json with your repo
# Then run sync periodically
srs-cli sync
```

### Programmatic Usage

```python
from backend.github_sync import GitHubSync

# Initialize
sync = GitHubSync(token="your_token")

# Fetch issues
issues = sync.fetch_issues("owner/repo", labels=["requirements"])

# Export to SRS
srs_markdown = sync.export_to_srs_format(issues)

# Save
with open("SRS.md", "w") as f:
    f.write(srs_markdown)
```

## Running Multiple Examples

```bash
# Run all examples
cd examples

echo "Running CLI demo..."
./cli_demo.sh

echo "Running GitHub sync examples..."
python3 github_sync_example.py
```

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/sync-srs.yml
name: Sync SRS
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install SRS CLI
        run: pip install -e .
      
      - name: Sync with GitHub
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: srs-cli sync
      
      - name: Commit changes
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add srs_*.json
          git commit -m "Update SRS data" || true
          git push
```

### Cron Job

```bash
# Add to crontab (crontab -e)
# Sync SRS every day at 9 AM
0 9 * * * cd /path/to/project && /usr/local/bin/srs-cli sync
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Validate SRS document before commit

if [ -f "SRS.md" ]; then
    echo "Validating SRS document..."
    # Add validation logic here
fi
```

## Troubleshooting

### "GitHub token required"

Set the GITHUB_TOKEN environment variable:
```bash
export GITHUB_TOKEN="your_token"
```

### "Failed to fetch issues: 404"

Check:
- Repository name format is correct (`owner/repo`)
- You have access to the repository
- Token has appropriate scopes

### "Module not found"

Install the package:
```bash
pip install -e /path/to/srs-generator
```

## Additional Resources

- **[Interactive Mode Guide](../INTERACTIVE_MODE_GUIDE.md)** - Conversational agent guide
- **[CLI_GUIDE.md](../CLI_GUIDE.md)** - Complete CLI documentation
- **[USAGE_GUIDE.md](../USAGE_GUIDE.md)** - Web interface guide
- **[templates/README.md](../templates/README.md)** - Template documentation
- **[backend/github_sync.py](../backend/github_sync.py)** - API reference

## Contributing Examples

Have a useful example? Contributions are welcome!

1. Create your example file
2. Add documentation
3. Test it works
4. Submit a pull request

## Questions?

- Open an issue on GitHub
- Review the documentation
- Check existing examples
