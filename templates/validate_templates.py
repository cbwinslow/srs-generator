#!/usr/bin/env python3
"""
Template Validation Script

This script validates that all templates are properly formatted and can be parsed.
"""

import yaml
import os
import sys


def validate_yaml_template(filepath):
    """Validate a YAML template file."""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check required fields for GitHub issue templates
        if 'name' in data:
            assert data['name'], "Template name cannot be empty"
            print(f"  ✓ Name: {data['name']}")
        
        if 'description' in data:
            print(f"  ✓ Description: {data['description'][:50]}...")
        
        if 'body' in data:
            print(f"  ✓ Form fields: {len(data['body'])}")
            
            # Validate each field
            for i, field in enumerate(data['body']):
                field_type = field.get('type')
                field_id = field.get('id', f'field_{i}')
                
                if field_type not in ['markdown', 'input', 'textarea', 'dropdown', 'checkboxes']:
                    print(f"  ⚠ Warning: Unknown field type '{field_type}' for {field_id}")
                else:
                    print(f"    - Field {i+1}: {field_type} ({field_id})")
        
        if 'labels' in data:
            print(f"  ✓ Labels: {', '.join(data['labels'])}")
        
        if 'contact_links' in data:
            print(f"  ✓ Contact links: {len(data['contact_links'])}")
        
        return True
    
    except yaml.YAMLError as e:
        print(f"  ✗ YAML parsing error: {e}")
        return False
    except AssertionError as e:
        print(f"  ✗ Validation error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False


def validate_markdown_template(filepath):
    """Validate a Markdown template file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check for front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Parse front matter
                front_matter = yaml.safe_load(parts[1])
                print(f"  ✓ Front matter found")
                if 'name' in front_matter:
                    print(f"  ✓ Name: {front_matter['name']}")
                if 'about' in front_matter:
                    print(f"  ✓ About: {front_matter['about'][:50]}...")
                if 'labels' in front_matter:
                    print(f"  ✓ Labels: {', '.join(front_matter['labels'])}")
        
        # Check content length
        lines = content.split('\n')
        print(f"  ✓ Lines: {len(lines)}")
        
        # Check for basic markdown structure
        has_headings = any(line.startswith('#') for line in lines)
        if has_headings:
            print(f"  ✓ Contains markdown headings")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Main validation function."""
    print("=" * 60)
    print("Template Validation Report")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_valid = True
    
    # Validate GitHub issue templates (YAML)
    print("\n📋 GitHub Issue Templates (YAML)")
    print("-" * 60)
    
    yaml_templates = [
        '.github/ISSUE_TEMPLATE/srs-generation-request.yml',
        '.github/ISSUE_TEMPLATE/config.yml',
    ]
    
    for template in yaml_templates:
        filepath = os.path.join(base_dir, template)
        if os.path.exists(filepath):
            print(f"\n{template}:")
            if not validate_yaml_template(filepath):
                all_valid = False
        else:
            print(f"\n{template}: ✗ File not found")
            all_valid = False
    
    # Validate GitHub issue templates (Markdown)
    print("\n\n📝 GitHub Issue Templates (Markdown)")
    print("-" * 60)
    
    md_templates = [
        '.github/ISSUE_TEMPLATE/bug_report.md',
        '.github/ISSUE_TEMPLATE/feature_request.md',
    ]
    
    for template in md_templates:
        filepath = os.path.join(base_dir, template)
        if os.path.exists(filepath):
            print(f"\n{template}:")
            if not validate_markdown_template(filepath):
                all_valid = False
        else:
            print(f"\n{template}: ✗ File not found")
            all_valid = False
    
    # Validate PR template
    print("\n\n🔀 Pull Request Template")
    print("-" * 60)
    
    pr_template = '.github/PULL_REQUEST_TEMPLATE.md'
    filepath = os.path.join(base_dir, pr_template)
    if os.path.exists(filepath):
        print(f"\n{pr_template}:")
        if not validate_markdown_template(filepath):
            all_valid = False
    else:
        print(f"\n{pr_template}: ✗ File not found")
        all_valid = False
    
    # Validate Linear template
    print("\n\n📊 Linear Template")
    print("-" * 60)
    
    linear_template = 'templates/LINEAR_TEMPLATE.md'
    filepath = os.path.join(base_dir, linear_template)
    if os.path.exists(filepath):
        print(f"\n{linear_template}:")
        if not validate_markdown_template(filepath):
            all_valid = False
    else:
        print(f"\n{linear_template}: ✗ File not found")
        all_valid = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ All templates are valid!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some templates have validation errors")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
