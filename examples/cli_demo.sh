#!/bin/bash
# Demo script showing CLI functionality

set -e

echo "=========================================="
echo "SRS CLI Tool Demo"
echo "=========================================="
echo ""

# Create temporary demo directory
DEMO_DIR="/tmp/srs_demo_$(date +%s)"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR"

echo "Demo directory: $DEMO_DIR"
echo ""

# 1. Initialize SRS document
echo "1️⃣  Initializing SRS document..."
python3 /home/runner/work/srs-generator/srs-generator/srs_cli.py init
echo ""

# 2. Show created files
echo "2️⃣  Created files:"
ls -lh
echo ""

# 3. Show SRS content
echo "3️⃣  SRS.md preview (first 30 lines):"
head -30 SRS.md
echo ""

# 4. Show config
echo "4️⃣  Configuration (.srs-config.json):"
cat .srs-config.json
echo ""

# 5. Download a template
echo "5️⃣  Downloading additional template..."
python3 /home/runner/work/srs-generator/srs-generator/srs_cli.py download --output custom_template.md
echo ""

# 6. Test help command
echo "6️⃣  Available commands:"
python3 /home/runner/work/srs-generator/srs-generator/srs_cli.py --help | head -20
echo ""

echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
echo ""
echo "Files created in: $DEMO_DIR"
echo ""
echo "To test GitHub sync features, set GITHUB_TOKEN:"
echo "  export GITHUB_TOKEN='your_token'"
echo "  srs-cli pull-issues --repo owner/repo"
echo "  srs-cli pull-projects --repo owner/repo"
echo ""
