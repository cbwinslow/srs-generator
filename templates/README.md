# SRS Generator Templates Guide

This directory contains templates for using the SRS Generator with various project management platforms.

## Available Templates

### 1. GitHub Templates

GitHub templates are located in `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`.

#### Issue Templates

##### SRS Generation Request (`srs-generation-request.yml`)
Use this template to request generation of a Software Requirements Specification document.

**How to use:**
1. Go to the GitHub repository
2. Click on "Issues" → "New Issue"
3. Select "SRS Generation Request"
4. Fill in the required fields:
   - Project Name
   - Target Users
   - Project Goals
   - Project Scope
   - Optional: Technical and Business Constraints
5. Submit the issue

The template includes:
- Structured form fields for all required information
- Optional fields for constraints
- Priority selection
- Section selection checkboxes
- Automatic labels (`srs-generation`, `documentation`)

##### Bug Report Template (`bug_report.md`)
Report bugs or issues with the SRS Generator.

##### Feature Request Template (`feature_request.md`)
Suggest new features or improvements.

#### Pull Request Template

The PR template (`PULL_REQUEST_TEMPLATE.md`) provides structure for:
- Description of changes
- Type of change classification
- Related issues linking
- SRS-specific changes documentation
- Testing checklist
- Code review guidelines

**How to use:**
1. Create a new pull request on GitHub
2. The template will auto-populate
3. Fill in all relevant sections
4. Check off completed items
5. Submit for review

### 2. Linear Template

The Linear template (`LINEAR_TEMPLATE.md`) provides a markdown-based template for Linear issue tracking.

**How to set up in Linear:**

1. **Access Template Settings:**
   - Open your Linear workspace
   - Go to Settings → Templates
   - Click "New template"

2. **Configure Template:**
   - Template Name: `SRS Generation Request`
   - Template Type: Issue template
   - Description: `Request generation of a Software Requirements Specification document`

3. **Add Template Content:**
   - Copy the content from `LINEAR_TEMPLATE.md` (starting from "## SRS Generation Request")
   - Paste into the template body in Linear

4. **Set Default Values:**
   - Default Project: Select your project
   - Default Labels: Add `srs-generation`, `documentation`
   - Default Assignee: Assign to appropriate team member
   - Default State: Set to "Backlog" or "To Do"

5. **Save Template**

**How to use in Linear:**
1. Click "New Issue" in Linear
2. Select "SRS Generation Request" template
3. Fill in all fields
4. Set priority
5. Create the issue

## Template Fields Explanation

### Project Name
The name of the software project for which you're creating the SRS.

**Example:** "E-commerce Mobile App", "Customer Portal", "Inventory Management System"

### Target Users
Describe who will use the software. Be specific about demographics, technical expertise, and use cases.

**Examples:**
- "Online shoppers aged 18-45, primarily mobile users"
- "Enterprise IT administrators with technical background"
- "Healthcare providers including doctors and nurses"

### Project Goals
List the primary objectives the project aims to achieve. Use measurable goals when possible.

**Examples:**
- "Increase user engagement by 30%"
- "Reduce customer support tickets by 50%"
- "Process 10,000 transactions per day"
- "Achieve 99.9% uptime"

### Project Scope
Define what is included and excluded from the project. This helps set clear boundaries.

**Included Examples:**
- User authentication and authorization
- Product catalog with search and filter
- Shopping cart functionality
- Payment processing integration
- Order tracking

**Excluded Examples:**
- Physical inventory management
- Vendor management system
- Accounting and financial reporting
- Customer relationship management (CRM)

### Constraints

#### Technical Constraints
Technical limitations or requirements that must be followed.

**Examples:**
- Must support iOS 14+ and Android 10+
- Must use Python/Flask backend
- Must integrate with existing SQL Server database
- Maximum API response time of 200ms
- Must support 1000 concurrent users

#### Business Constraints
Business-related limitations or requirements.

**Examples:**
- Must launch within 6 months
- Budget limit of $100,000
- Must comply with GDPR and CCPA
- Must support 5 languages (English, Spanish, French, German, Japanese)
- Must be accessible (WCAG 2.1 AA compliant)

## Best Practices

### Writing Effective SRS Requests

1. **Be Specific:** Provide detailed information about your project
2. **Be Measurable:** Use quantifiable goals and requirements when possible
3. **Be Realistic:** Set achievable scope and constraints
4. **Be Complete:** Fill in all required fields
5. **Include Context:** Add any relevant background information

### Common Pitfalls to Avoid

1. ❌ **Vague descriptions:** "Make it fast" → ✅ "Response time < 200ms"
2. ❌ **Missing scope:** Not defining what's excluded → ✅ Clear boundaries
3. ❌ **Unrealistic goals:** "100% uptime" → ✅ "99.9% uptime"
4. ❌ **Incomplete constraints:** Missing technical requirements → ✅ All constraints listed
5. ❌ **No priority:** Everything is critical → ✅ Clear prioritization

## Integration with SRS Generator API

These templates are designed to work with the SRS Generator API:

```bash
# Example API call using data from template
curl -X POST http://localhost:5000/api/v1/generate_srs \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "E-commerce Mobile App",
    "targetUsers": "Online shoppers aged 18-45",
    "projectGoals": "Provide seamless shopping experience, increase engagement by 30%",
    "projectScope": "Included: User auth, product catalog, shopping cart. Excluded: Inventory management"
  }'
```

## Automated Workflows

### GitHub Actions Integration

You can create GitHub Actions workflows that automatically trigger SRS generation when issues are created with specific labels:

```yaml
name: Generate SRS from Issue
on:
  issues:
    types: [opened, labeled]

jobs:
  generate-srs:
    if: contains(github.event.issue.labels.*.name, 'srs-generation')
    runs-on: ubuntu-latest
    steps:
      - name: Parse Issue
        # Extract data from issue body
      - name: Call SRS Generator API
        # Make API call with extracted data
      - name: Post SRS as Comment
        # Add generated SRS as issue comment
```

### Linear Automation

Linear supports automation rules that can:
1. Automatically assign SRS generation requests to specific team members
2. Move issues through workflow states
3. Notify stakeholders when SRS is ready
4. Link SRS documents to related issues

**Example Linear Automation:**
```
When issue is created with label "srs-generation"
→ Set project to "Requirements"
→ Set status to "In Progress"
→ Assign to "Tech Lead"
→ Add to current cycle
```

## Customization

Feel free to customize these templates for your organization's needs:

1. **Add Custom Fields:** Include organization-specific requirements
2. **Modify Labels:** Use your own label taxonomy
3. **Adjust Priorities:** Align with your priority system
4. **Add Workflows:** Integrate with your CI/CD pipeline
5. **Extend Sections:** Add additional SRS sections specific to your domain

## Support

For issues or questions about using these templates:
- Open an issue on GitHub
- Check the main README.md for documentation
- Review the SRS.md for example output

## Version History

- **v1.0.0** (2024): Initial template release
  - GitHub issue templates (YAML and Markdown)
  - GitHub PR template
  - Linear template
  - Comprehensive documentation
