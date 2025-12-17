#!/usr/bin/env python3
"""
Example script demonstrating SRS generation via API

This script shows how to use the SRS Generator API programmatically.
It uses example data similar to what would come from GitHub or Linear templates.
"""

import json
import os


def create_example_request():
    """Create an example API request based on template data."""
    
    # This data mirrors what you'd fill in GitHub or Linear templates
    request_data = {
        "projectName": "TaskFlow - Team Collaboration Platform",
        "targetUsers": """
        Remote teams of 5-50 members including:
        - Project managers and team leads
        - Software development teams  
        - Marketing and creative agencies
        - Age range: 25-55
        - Tech-savvy professionals familiar with SaaS tools
        - Users across different time zones
        """.strip(),
        "projectGoals": """
        1. Improve team collaboration efficiency by 40%
        2. Reduce time spent in status meetings by 50%
        3. Provide real-time visibility into project progress
        4. Enable asynchronous communication across time zones
        5. Integrate with existing tools (Slack, GitHub, Google Workspace)
        6. Achieve 95% user satisfaction score within 6 months
        7. Support 10,000 active teams within first year
        """.strip(),
        "projectScope": """
        INCLUDED:
        - User authentication and team management
        - Project and task management with Kanban boards
        - Real-time collaboration features (comments, mentions, notifications)
        - File sharing and document collaboration
        - Time tracking and reporting
        - Mobile applications (iOS and Android)
        - Web application
        - API for third-party integrations
        - Integration with Slack, GitHub, and Google Workspace
        - Dashboard with analytics and insights
        - Search functionality across projects and tasks
        - Role-based access control (Admin, Manager, Member, Guest)
        
        EXCLUDED:
        - Built-in video conferencing (will integrate with Zoom/Teams)
        - Advanced financial management and invoicing
        - HR and payroll management
        - Customer relationship management (CRM)
        - Email hosting
        - Code repository hosting (will integrate with GitHub/GitLab)
        - Design tools (will integrate with Figma)
        """.strip()
    }
    
    return request_data


def generate_curl_command(data):
    """Generate a curl command for the API request."""
    
    json_data = json.dumps(data, indent=2)
    
    curl_command = f"""
# Example curl command to generate SRS
curl -X POST http://localhost:5000/api/v1/generate_srs \\
  -H "Content-Type: application/json" \\
  -d '{json_data}'
    """.strip()
    
    return curl_command


def generate_python_code(data):
    """Generate Python code for the API request."""
    
    python_code = f'''
import requests
import json

# API endpoint
url = "http://localhost:5000/api/v1/generate_srs"

# Request data (from GitHub/Linear template)
data = {json.dumps(data, indent=4)}

# Make request
response = requests.post(url, json=data)
result = response.json()

# Handle response
if response.status_code == 200:
    print("✓ SRS generated successfully!")
    
    # Save to markdown file
    with open('generated_srs.md', 'w') as f:
        f.write("# Software Requirements Specification\\n\\n")
        
        sections = result.get('sections', {{}})
        for section_name, content in sections.items():
            # Format section name
            title = section_name.replace('_', ' ').title()
            f.write(f"## {{title}}\\n\\n")
            f.write(content)
            f.write("\\n\\n")
    
    print("✓ Saved to generated_srs.md")
else:
    print(f"✗ Error: {{result.get('error')}}")
    if 'missing_fields' in result:
        print(f"  Missing fields: {{result['missing_fields']}}")
    '''.strip()
    
    return python_code


def main():
    """Main function."""
    print("=" * 70)
    print("SRS Generator API Example")
    print("=" * 70)
    print()
    print("This example shows how to use the SRS Generator API with data")
    print("that would typically come from GitHub or Linear templates.")
    print()
    
    # Create example request
    data = create_example_request()
    
    # Print JSON request
    print("1. JSON Request Data")
    print("-" * 70)
    print(json.dumps(data, indent=2))
    print()
    
    # Print curl command
    print("2. cURL Command")
    print("-" * 70)
    print(generate_curl_command(data))
    print()
    
    # Print Python code
    print("3. Python Code Example")
    print("-" * 70)
    print(generate_python_code(data))
    print()
    
    # Save examples to files
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save JSON
    json_file = os.path.join(output_dir, 'example_request.json')
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Saved JSON example to: {json_file}")
    
    # Save curl script
    curl_file = os.path.join(output_dir, 'example_curl.sh')
    with open(curl_file, 'w') as f:
        f.write("#!/bin/bash\n\n")
        f.write("# Example curl command to generate SRS document\n")
        f.write("# Make sure the SRS Generator is running on http://localhost:5000\n\n")
        f.write(generate_curl_command(data))
        f.write("\n")
    os.chmod(curl_file, 0o755)
    print(f"✓ Saved curl script to: {curl_file}")
    
    # Save Python script
    python_file = os.path.join(output_dir, 'example_python.py')
    with open(python_file, 'w') as f:
        f.write("#!/usr/bin/env python3\n")
        f.write('"""\n')
        f.write("Example Python script to generate SRS via API\n")
        f.write('Make sure the SRS Generator is running on http://localhost:5000\n')
        f.write('"""\n\n')
        f.write(generate_python_code(data))
        f.write("\n\n")
        f.write('if __name__ == "__main__":\n')
        f.write('    # Main block intentionally left empty: example code runs on import.\n')
        f.write('    pass\n')
    os.chmod(python_file, 0o755)
    print(f"✓ Saved Python script to: {python_file}")
    
    print()
    print("=" * 70)
    print("To use these examples:")
    print("1. Start the SRS Generator: docker-compose up")
    print("2. Run the curl script: ./templates/example_curl.sh")
    print("3. Or run the Python script: python3 ./templates/example_python.py")
    print("=" * 70)


if __name__ == '__main__':
    main()
