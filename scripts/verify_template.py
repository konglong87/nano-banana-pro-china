#!/usr/bin/env python3
"""
Verify template configuration - check base image existence and template setup
"""
import json
from pathlib import Path
import sys

def verify_template(template_name: str):
    """Verify template config and base image"""

    # Find template config
    template_dir = Path(__file__).parent.parent / 'templates'

    # Search by Chinese name or filename
    template_file = None
    template = None

    # Support both new subdirectory structure and old flat structure

    # Chinese name to slug mapping
    name_to_slug = {
        '春节海报': 'spring-festival',
        '产品宣传': 'product-promotion',
        '企业文化': 'corporate-culture'
    }

    # Strategy 1: New structure - templates/{slug}/template.json
    slug = name_to_slug.get(template_name, template_name.lower().replace(' ', '-'))
    new_structure_file = template_dir / slug / 'template.json'

    if new_structure_file.exists():
        template_file = new_structure_file
    else:
        # Strategy 2: Old structure - templates/{name}.json
        possible_files = [
            template_dir / f"{template_name}.json",
            template_dir / f"{template_name.lower()}.json",
        ]

        for f in possible_files:
            if f.exists():
                template_file = f
                break

        # Strategy 3: Search by Chinese name in old structure
        if not template_file:
            for json_file in template_dir.glob('*.json'):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('name') == template_name:
                            template_file = json_file
                            template = data
                            break
                except:
                    continue

    if not template_file:
        print(f"❌ Template config not found: {template_name}")
        print(f"\nAvailable templates:")

        # List templates from both structures
        # New structure: templates/*/template.json
        for subdir in template_dir.iterdir():
            if subdir.is_dir():
                template_json = subdir / 'template.json'
                if template_json.exists():
                    try:
                        with open(template_json, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            print(f"  - {data.get('name')} ({subdir.name}/template.json)")
                    except:
                        pass

        # Old structure: templates/*.json
        for json_file in template_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"  - {data.get('name')} ({json_file.name})")
            except:
                pass

        sys.exit(1)

    # Load template if not already loaded
    if not template:
        with open(template_file, 'r', encoding='utf-8') as f:
            template = json.load(f)

    relative_path = template_file.relative_to(template_dir)
    print(f"✅ Template config: {relative_path}")
    print(f"   Name: {template['name']}")
    print(f"   Description: {template['description']}")

    # Check base image - resolve based on structure
    # New structure: templates/{slug}/template.json - base image in same directory
    # Old structure: templates/{name}.json - base image path from JSON field

    if template_file.parent != template_dir:
        # New structure: base image relative to template subdirectory
        base_image_path = template_file.parent / template['base_image']
    else:
        # Old structure: use filename only (legacy behavior)
        base_image_path = template_dir / Path(template['base_image']).name

    if not base_image_path.exists():
        relative_base_path = base_image_path.relative_to(template_dir.parent)
        print(f"\n❌ Base image NOT FOUND: {relative_base_path}")
        print(f"   Required: {template['base_image']}")
        print(f"\n💡 Solution:")
        print(f"   1. Prepare base image (现成的设计模板图片)")
        print(f"   2. Save to: {base_image_path}")
        print(f"   3. Requirements:")
        print(f"      - Shows layout: 标题在{template['title_position']}, 插图在{template['illustration_position']}")
        print(f"      - Size: {template['dimensions']['width']}x{template['dimensions']['height']}")
        print(f"      - Font style reference: {template['font_style']}")
        sys.exit(1)
    else:
        file_size = base_image_path.stat().st_size / 1024
        relative_base_path = base_image_path.relative_to(template_dir.parent)
        print(f"\n✅ Base image found: {relative_base_path}")
        print(f"   File size: {file_size:.1f} KB")
        print(f"\n🎉 Template '{template['name']}' is ready to use!")

        return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Verify template configuration')
    parser.add_argument('--template', required=True, help='Template name')

    args = parser.parse_args()
    verify_template(args.template)