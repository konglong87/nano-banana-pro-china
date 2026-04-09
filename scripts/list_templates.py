#!/usr/bin/env python3
"""
List all available Wanxiang templates from templates/ directory
"""
import json
from pathlib import Path
import sys

def list_templates():
    """List all available templates from templates/ directory"""
    template_dir = Path(__file__).parent.parent / 'templates'

    if not template_dir.exists():
        print("❌ Templates directory not found")
        print(f"   Expected: {template_dir}")
        sys.exit(1)

    # Support both new subdirectory structure and old flat structure
    template_files = []

    # 1. Check for new structure: templates/*/template.json
    for subdir in template_dir.iterdir():
        if subdir.is_dir():
            template_file = subdir / 'template.json'
            if template_file.exists():
                template_files.append(template_file)

    # 2. Fallback: Check for old flat structure: templates/*.json
    if not template_files:
        template_files = list(template_dir.glob('*.json'))

    if not template_files:
        print(f"❌ No templates found in {template_dir}")
        print("\nCreate a template by adding:")
        print("  - New structure: templates/{name}/template.json")
        print("  - Old structure: templates/{name}.json")
        sys.exit(1)

    templates = []
    for json_file in sorted(template_files):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
                # Calculate relative path from templates/ directory
                relative_path = json_file.relative_to(template_dir)
                templates.append({
                    "name": template.get('name', json_file.stem),
                    "description": template.get('description', 'No description'),
                    "title_position": template.get('title_position', 'N/A'),
                    "illustration_position": template.get('illustration_position', 'N/A'),
                    "dimensions": f"{template['dimensions']['width']}x{template['dimensions']['height']}" if 'dimensions' in template else 'N/A',
                    "base_image": template.get('base_image', 'N/A'),
                    "file": str(relative_path)
                })
        except Exception as e:
            print(f"Warning: Failed to load {json_file}: {e}")

    # Print formatted output
    print("\n📋 Available Wanxiang Templates:\n")
    print("="*80)

    for template in templates:
        print(f"\n🎨 {template['name']}")
        print(f"   Description: {template['description']}")
        print(f"   Title: {template['title_position']}")
        print(f"   Illustration: {template['illustration_position']}")
        print(f"   Dimensions: {template['dimensions']}")
        print(f"   Base Image: {template['base_image']}")
        print(f"   File: templates/{template['file']}")

    print("\n" + "="*80)
    print(f"\nTotal templates: {len(templates)}")
    print("\nUsage:")
    print("  python3 scripts/generate_with_template.py --template \"春节海报\" --title \"标题\" --illustration \"插图描述\"")

    # Return JSON for programmatic use
    return templates

if __name__ == '__main__':
    templates = list_templates()

    # Optional: output JSON format if --json flag
    if '--json' in sys.argv:
        print(json.dumps(templates, indent=2, ensure_ascii=False))