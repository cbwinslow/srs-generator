# SRS Generator - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Choose Your Method

#### Option A: Web Interface (Easiest)
```bash
docker-compose up
# Visit http://localhost:5000
```

#### Option B: CLI Tool (Most Flexible)
```bash
# Install with pipx
pipx install git+https://github.com/cbwinslow/srs-generator.git

# Or use directly with uvx (no installation)
uvx --from git+https://github.com/cbwinslow/srs-generator.git srs-cli --help
```

#### Option C: GitHub/Linear Templates
- Go to Issues → New Issue → Select "SRS Generation Request"
- Fill in the form and submit

---

## 📋 CLI Tool Quick Reference

### Initialize a New SRS Document
```bash
srs-cli init
# Creates: SRS.md and .srs-config.json
```

### Pull Requirements from GitHub
```bash
export GITHUB_TOKEN="your_token_here"
srs-cli pull-issues --repo owner/repo
srs-cli pull-projects --repo owner/repo
```

### Push SRS to GitHub
```bash
srs-cli push-issue --repo owner/repo --title "SRS v1.0" --file SRS.md
```

### Auto-Sync with GitHub
```bash
# Edit .srs-config.json first to configure your repo
srs-cli sync
```

---

## 🔑 GitHub Token Setup

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `project`
4. Copy token and set environment variable:
   ```bash
   export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
   ```

---

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| **[README.md](README.md)** | Main project overview |
| **[CLI_GUIDE.md](CLI_GUIDE.md)** | Complete CLI documentation |
| **[USAGE_GUIDE.md](USAGE_GUIDE.md)** | Web interface guide |
| **[GITHUB_SYNC_SUMMARY.md](GITHUB_SYNC_SUMMARY.md)** | GitHub sync implementation |
| **[templates/README.md](templates/README.md)** | Template documentation |
| **[examples/README.md](examples/README.md)** | Usage examples |

---

## 🎯 Common Use Cases

### Use Case 1: Create New SRS
```bash
srs-cli init --path ./my-project
cd my-project
# Edit SRS.md
```

### Use Case 2: Sync with Existing GitHub Repo
```bash
# 1. Initialize
srs-cli init

# 2. Configure
echo '{
  "template": "default",
  "github": {
    "enabled": true,
    "repo": "owner/repo",
    "sync_issues": true,
    "sync_projects": true
  }
}' > .srs-config.json

# 3. Sync
export GITHUB_TOKEN="your_token"
srs-cli sync
```

### Use Case 3: Convert GitHub Issues to SRS
```bash
# Pull issues
srs-cli pull-issues --repo owner/repo --output issues.json

# Convert (using Python)
python3 << 'EOF'
import json
from backend.github_sync import GitHubSync

with open('issues.json') as f:
    issues = json.load(f)

sync = GitHubSync()
srs = sync.export_to_srs_format(issues)

with open('SRS_from_issues.md', 'w') as f:
    f.write(srs)
    
print("✓ Created SRS_from_issues.md")
EOF
```

### Use Case 4: Automated Daily Sync
```bash
# Add to crontab
0 9 * * * cd /path/to/project && srs-cli sync
```

---

## 🐛 Troubleshooting

### "GitHub token required"
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### "Failed to fetch issues: 404"
- Check repository name: `owner/repo` (not URL)
- Verify you have access to the repository
- Ensure token has `repo` scope

### "Module not found"
```bash
pip install requests
# or
pip install -r requirements.txt
```

### CLI command not found after installation
```bash
# For pipx
pipx ensurepath

# For pip
export PATH="$HOME/.local/bin:$PATH"
```

---

## 💡 Tips

1. **Keep token secure**: Never commit tokens to git
2. **Use labels**: Tag issues with `requirements`, `feature`, etc.
3. **Regular syncs**: Schedule daily syncs for up-to-date data
4. **Version control**: Commit SRS.md to git for history
5. **Templates**: Customize templates in `srs_cli.py`

---

## 🆘 Getting Help

- **Documentation**: Review guides in this repository
- **Examples**: Check `examples/` directory
- **Issues**: Open an issue on GitHub
- **Tests**: Run `pytest tests/` to verify setup

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Installation
pipx install git+https://github.com/cbwinslow/srs-generator.git

# Setup
export GITHUB_TOKEN="token"
srs-cli init

# Pull data
srs-cli pull-issues --repo owner/repo
srs-cli pull-projects --repo owner/repo

# Push data
srs-cli push-issue --repo owner/repo --title "Title" --file SRS.md

# Sync
srs-cli sync

# Help
srs-cli --help
srs-cli COMMAND --help
```

---

**Next Steps**: Choose a method above and start creating your SRS document! 🎉
