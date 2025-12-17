# SRS Generator Usage Guide

This guide explains how to use the SRS Generator to create Software Requirements Specification documents for your projects.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Using the Web Interface](#using-the-web-interface)
3. [Using GitHub Templates](#using-github-templates)
4. [Using Linear Templates](#using-linear-templates)
5. [Using the API Directly](#using-the-api-directly)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Quick Start

### Option 1: Web Interface (Fastest)

1. Start the application (see [README.md](README.md))
2. Open `http://localhost:5000` in your browser
3. Fill in the form with your project information
4. Click "Generate SRS"
5. Download the generated SRS document

### Option 2: GitHub Issue Template

1. Go to your repository's Issues tab
2. Click "New Issue"
3. Select "SRS Generation Request"
4. Fill in the form
5. Submit the issue
6. Team can review and process the request

### Option 3: Linear Template

1. In Linear, create a new issue
2. Select the "SRS Generation Request" template (if configured)
3. Fill in all fields
4. Create the issue
5. Team processes the request

## Using the Web Interface

The web interface is the simplest way to generate an SRS document.

### Step-by-Step Instructions

1. **Start the Application**
   ```bash
   # Using Docker
   docker-compose up
   
   # Or locally
   ./run.sh
   ```

2. **Open the Interface**
   - Navigate to `http://localhost:5000` (or your deployed URL)

3. **Fill in Project Information**
   
   **Project Name:**
   - Enter a clear, descriptive name for your project
   - Example: "E-commerce Mobile App" or "Customer Portal v2"
   
   **Target Users:**
   - Describe who will use the software
   - Be specific about demographics, expertise, and use cases
   - Example: "Online shoppers aged 18-45, mobile-first users, tech-savvy"
   
   **Project Goals:**
   - List the main objectives (3-7 goals recommended)
   - Use measurable goals when possible
   - Example:
     ```
     - Increase user engagement by 30%
     - Reduce checkout time to under 2 minutes
     - Achieve 99.9% uptime
     ```
   
   **Project Scope:**
   - Define what IS and ISN'T included
   - Be explicit about boundaries
   - Example:
     ```
     Included:
     - User authentication
     - Product catalog
     - Shopping cart
     - Payment processing
     
     Excluded:
     - Inventory management
     - Vendor portal
     ```

4. **Generate Document**
   - Click "Generate SRS"
   - Wait 10-30 seconds for AI generation
   - Review the generated sections

5. **Download SRS**
   - Click "Download SRS" button
   - File saves as `srs_document_YYYY-MM-DD.md`
   - Open in any markdown editor

### Tips for Better Results

- **Be Specific:** More detail = better output
- **Use Examples:** Concrete examples improve clarity
- **Be Realistic:** Set achievable goals and scope
- **Include Context:** Add relevant background information
- **Review Output:** AI-generated content should be reviewed and refined

## Using GitHub Templates

GitHub templates help standardize SRS generation requests within your team.

### Setup (One-Time)

Templates are already included in the repository under `.github/ISSUE_TEMPLATE/`. When you push to GitHub, they become available automatically.

### Creating an SRS Request

1. **Navigate to Issues**
   - Go to your GitHub repository
   - Click "Issues" tab
   - Click "New Issue"

2. **Select Template**
   - You'll see "SRS Generation Request" option
   - Click "Get started"

3. **Fill Out Form**
   - The form includes:
     - Project Name (required)
     - Target Users (required)
     - Project Goals (required)
     - Project Scope (required)
     - Technical Constraints (optional)
     - Business Constraints (optional)
     - Priority (dropdown)
     - Required Sections (checkboxes)

4. **Submit Issue**
   - Review all fields
   - Add a descriptive title
   - Submit the issue

5. **Process Request**
   - Team reviews the issue
   - Use the information to generate SRS via web interface or API
   - Attach generated SRS to issue as comment or file
   - Close issue when complete

### Automation Ideas

You can automate SRS generation from GitHub issues:

```yaml
# .github/workflows/generate-srs.yml
name: Generate SRS from Issue
on:
  issues:
    types: [opened, labeled]

jobs:
  generate:
    if: contains(github.event.issue.labels.*.name, 'srs-generation')
    runs-on: ubuntu-latest
    steps:
      - name: Extract issue data
        id: parse
        run: |
          # Parse issue body and extract fields
          
      - name: Call SRS Generator API
        run: |
          curl -X POST http://your-srs-generator/api/v1/generate_srs \
            -H "Content-Type: application/json" \
            -d "${{ steps.parse.outputs.json }}"
      
      - name: Post result as comment
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'SRS document has been generated!'
            })
```

## Using Linear Templates

Linear templates provide a structured way to request SRS generation in your Linear workspace.

### Setup (One-Time)

1. **Access Linear Settings**
   - Open your Linear workspace
   - Go to Settings (⚙️) → Templates

2. **Create New Template**
   - Click "New template"
   - Template type: "Issue"
   - Template name: "SRS Generation Request"

3. **Add Template Content**
   - Open `templates/LINEAR_TEMPLATE.md`
   - Copy content starting from "## SRS Generation Request"
   - Paste into Linear template body

4. **Configure Template**
   - Description: "Request generation of a Software Requirements Specification document"
   - Default project: Select appropriate project
   - Default labels: Add `srs-generation`, `documentation`
   - Default assignee: Assign to appropriate team member
   - Default state: "Backlog" or "To Do"

5. **Save Template**

### Creating an SRS Request in Linear

1. **Create New Issue**
   - Click "+" or "C" keyboard shortcut
   - Select "SRS Generation Request" template

2. **Fill In Information**
   - All fields from template will be pre-populated
   - Fill in your project details
   - Check relevant section boxes
   - Set priority

3. **Create Issue**
   - Review all information
   - Click "Create"

4. **Process Request**
   - Team reviews the Linear issue
   - Generate SRS using web interface or API
   - Update issue with generated document link
   - Move to "Done" when complete

### Linear Integration Ideas

- **Automation Rules:**
  ```
  When issue created with label "srs-generation"
  → Assign to Tech Lead
  → Move to "In Progress"
  → Add to current cycle
  ```

- **Custom Views:**
  - Create a view filtered by "srs-generation" label
  - Group by priority
  - Sort by creation date

## Using the API Directly

For programmatic access, use the REST API.

### Endpoint

```
POST /api/v1/generate_srs
```

### Request Format

```json
{
  "projectName": "Your Project Name",
  "targetUsers": "Description of target users",
  "projectGoals": "List of project goals",
  "projectScope": "What is included and excluded"
}
```

### Example cURL Request

```bash
curl -X POST http://localhost:5000/api/v1/generate_srs \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "E-commerce Mobile App",
    "targetUsers": "Online shoppers aged 18-45, mobile-first users",
    "projectGoals": "Increase engagement by 30%, reduce checkout time to under 2 minutes",
    "projectScope": "Included: User auth, product catalog, cart, payment. Excluded: Inventory management"
  }'
```

### Example Python Request

```python
import requests
import json

url = "http://localhost:5000/api/v1/generate_srs"
data = {
    "projectName": "E-commerce Mobile App",
    "targetUsers": "Online shoppers aged 18-45, mobile-first users",
    "projectGoals": "Increase engagement by 30%, reduce checkout time to under 2 minutes",
    "projectScope": "Included: User auth, product catalog, cart, payment. Excluded: Inventory management"
}

response = requests.post(url, json=data)
result = response.json()

if response.status_code == 200:
    # Save to file
    with open('generated_srs.md', 'w') as f:
        f.write("# Software Requirements Specification\n\n")
        for section, content in result['sections'].items():
            f.write(f"## {section.replace('_', ' ').title()}\n\n")
            f.write(content)
            f.write("\n\n")
    print("SRS generated successfully!")
else:
    print(f"Error: {result.get('error')}")
```

### Response Format

```json
{
  "status": "success",
  "sections": {
    "introduction": "Generated introduction content...",
    "functional_requirements": "Generated functional requirements...",
    "non_functional_requirements": "Generated non-functional requirements...",
    "constraints": "Generated constraints..."
  }
}
```

### Error Response

```json
{
  "error": "Error message",
  "details": "Detailed error information",
  "missing_fields": ["field1", "field2"]
}
```

## Best Practices

### Writing Effective Project Information

1. **Project Name**
   - ✅ Clear and descriptive: "Customer Support Portal v2"
   - ❌ Vague: "New Project" or "App"

2. **Target Users**
   - ✅ Specific: "Enterprise IT administrators with 5+ years experience, managing 100+ users"
   - ❌ Generic: "People who need the software"

3. **Project Goals**
   - ✅ Measurable: "Reduce support ticket response time from 24 hours to 2 hours"
   - ❌ Vague: "Make things faster"

4. **Project Scope**
   - ✅ Clear boundaries: "Included: X, Y, Z. Excluded: A, B, C"
   - ❌ Unclear: "Everything related to customer support"

### Reviewing Generated SRS

1. **Check Accuracy**
   - Verify all requirements match your needs
   - Ensure no hallucinated features

2. **Add Specifics**
   - Add technical details AI might not know
   - Include specific technologies, APIs, integrations

3. **Refine Requirements**
   - Make requirements more specific and testable
   - Add acceptance criteria

4. **Review with Stakeholders**
   - Share with team for feedback
   - Incorporate domain expertise

5. **Iterate**
   - Regenerate if needed with refined input
   - Update sections manually as needed

### Version Control

- Store SRS documents in your repository
- Use meaningful commit messages
- Tag versions: `v1.0.0`, `v1.1.0`, etc.
- Link to related issues and PRs

## Troubleshooting

### Common Issues

#### "Content-Type must be application/json"

**Problem:** API request missing proper headers

**Solution:**
```bash
curl -X POST http://localhost:5000/api/v1/generate_srs \
  -H "Content-Type: application/json" \  # Add this header
  -d '{"projectName": "...", ...}'
```

#### "Missing required fields"

**Problem:** Not all required fields provided

**Solution:** Ensure all four fields are present:
- `projectName`
- `targetUsers`
- `projectGoals`
- `projectScope`

#### "Failed to generate SRS document"

**Problem:** AI service error or API key issue

**Solution:**
1. Check OpenRouter API key in `.env` file
2. Verify API key is valid
3. Check internet connectivity
4. Review logs: `docker-compose logs backend`

#### Slow Generation (> 60 seconds)

**Problem:** Network latency or API throttling

**Solution:**
1. Check network connection
2. Verify API rate limits not exceeded
3. Try again in a few minutes
4. Consider local AI model for offline use

#### Generated Content is Low Quality

**Problem:** Input lacks detail or context

**Solution:**
1. Provide more detailed input
2. Include specific examples
3. Add context about domain/industry
4. Be specific about technical requirements
5. Regenerate with refined input

### Getting Help

- **GitHub Issues:** Report bugs or request features
- **Documentation:** Review README.md and templates/README.md
- **Examples:** See templates/EXAMPLE_FILLED.md
- **Logs:** Check application logs for errors

## Next Steps

After generating your SRS:

1. **Review and Refine**
   - Technical review by developers
   - Business review by stakeholders
   - Legal review if needed

2. **Version and Store**
   - Commit to version control
   - Tag with version number
   - Link to project documentation

3. **Share and Collaborate**
   - Share with team via GitHub/Linear
   - Gather feedback
   - Iterate as needed

4. **Use in Development**
   - Reference during sprint planning
   - Create tickets from requirements
   - Track implementation progress
   - Update as requirements evolve

5. **Maintain**
   - Review quarterly or when major changes occur
   - Update for new features
   - Archive old versions

---

**Need more help?** See [README.md](README.md) or [templates/README.md](templates/README.md)
