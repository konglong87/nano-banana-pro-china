#!/usr/bin/env python3
"""
Nano Banana Pro China - Template-Based Image Generator
Uses Gemini 3 Pro Image via Cloudflare Gateway + OpenRouter API
"""
import os
import sys
import json
import base64
import requests
from pathlib import Path
from datetime import datetime

def load_env_config():
    """Load configuration from .env file"""
    config = {}

    # Check multiple .env locations
    env_paths = [
        Path(__file__).parent.parent / '.env',  # Skill directory
        Path.cwd() / '.env'  # Current directory
    ]

    for env_path in env_paths:
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key and key not in os.environ:
                            os.environ[key] = value

    # Load from environment
    config['api_key'] = os.getenv('OPENROUTER_API_KEY')
    config['base_url'] = os.getenv('OPENROUTER_BASE_URL')
    config['cf_token'] = os.getenv('CF_AIG_TOKEN')
    config['save_dir'] = os.getenv('SAVE_DIR', './materials/raw')

    # Validate
    if not config['api_key']:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    if not config['base_url']:
        raise ValueError("OPENROUTER_BASE_URL not found in .env file")
    if not config['cf_token']:
        print("⚠️  Warning: CF_AIG_TOKEN not found. Gateway authentication may fail.")

    return config

def load_template(template_name: str):
    """Load template configuration"""
    template_dir = Path(__file__).parent.parent / 'templates'

    # Chinese name to slug mapping
    name_to_slug = {
        '春节海报': 'spring-festival',
        '产品宣传': 'product-promotion',
        '企业文化': 'corporate-culture'
    }

    # Try to find template
    slug = name_to_slug.get(template_name, template_name.lower().replace(' ', '-'))
    template_file = template_dir / slug / 'template.json'

    if not template_file.exists():
        # Fallback: search by name
        for subdir in template_dir.iterdir():
            if subdir.is_dir():
                tf = subdir / 'template.json'
                if tf.exists():
                    with open(tf, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('name') == template_name:
                            template_file = tf
                            template = data
                            break
        else:
            raise FileNotFoundError(f"Template '{template_name}' not found. Run: python3 scripts/list_templates.py")

    if not 'template' in locals():
        with open(template_file, 'r', encoding='utf-8') as f:
            template = json.load(f)

    return template, template_file.parent

def generate_with_template(template_name: str, title: str, illustration: str, resolution: str = '1K', config: dict = None):
    """Generate image using template with Gemini 3 Pro Image API"""

    if config is None:
        config = load_env_config()

    # Load template
    template, template_dir = load_template(template_name)
    base_image_path = template_dir / template['base_image']

    # Verify base image
    if not base_image_path.exists():
        raise FileNotFoundError(f"Base image not found: {base_image_path}\nRun: python3 scripts/verify_template.py --template '{template_name}'")

    # Construct prompt based on template
    prompt = f"""生成一张{template['description']}风格的图片。
要求：
- 标题位置：{template['title_position']}
- 标题内容：{title}
- 字体风格：{template['font_style']}
- 插图位置：{template['illustration_position']}
- 插图内容：{illustration}

请保持与模板图片的整体风格和布局一致。"""

    print(f"🎨 使用模板: {template['name']}")
    print(f"📐 基础图片: {base_image_path.name}")
    print(f"📝 提示词: {prompt[:100]}...")

    # Encode base image
    with open(base_image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Detect image type
    suffix = base_image_path.suffix.lower()
    image_type_map = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}
    image_type = image_type_map.get(suffix, 'image/png')

    # Build payload
    payload = {
        "model": "google/gemini-3-pro-image-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "modalities": ["image", "text"],
        "image_config": {"image_size": resolution},
        "stream": False
    }

    # Build headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {config['api_key']}"
    }

    if config.get('cf_token'):
        headers['cf-aig-authorization'] = f"Bearer {config['cf_token']}"

    print(f"🚀 调用 API ({resolution} 分辨率)...")
    print(f"🔑 认证方式: Cloudflare Gateway + OpenRouter")

    # Make request
    response = requests.post(
        config['base_url'],
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"API error: HTTP {response.status_code}\n{response.text}")

    result = response.json()

    # Extract image URLs
    image_urls = []

    # Try multiple response formats
    # Format 1: OpenAI-style with choices
    if 'choices' in result and len(result['choices']) > 0:
        choice = result['choices'][0]
        message = choice.get('message', {})

        # Content can be string or list
        content = message.get('content')
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'image_url':
                        url_data = item.get('image_url', {})
                        url = url_data.get('url', '') if isinstance(url_data, dict) else url_data
                        if url:
                            image_urls.append(url)

        # Check for images array (Gemini format)
        if 'images' in message:
            for img in message['images']:
                if isinstance(img, dict) and 'image_url' in img:
                    url_data = img['image_url']
                    url = url_data.get('url', '') if isinstance(url_data, dict) else url_data
                    if url:
                        image_urls.append(url)

    # Format 2: Direct image_url in response
    elif 'image_url' in result:
        url_data = result['image_url']
        url = url_data.get('url', '') if isinstance(url_data, dict) else url_data
        if url:
            image_urls.append(url)

    if not image_urls:
        print(f"\n❌ 未找到图片URL。完整响应:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        raise Exception("No image URLs in response")

    # Download images
    save_dir = Path(config['save_dir'])
    save_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_files = []

    for idx, url in enumerate(image_urls):
        filename = f"{timestamp}_{template['name']}_{idx+1}.png" if len(image_urls) > 1 else f"{timestamp}_{template['name']}.png"
        save_path = save_dir / filename

        # Download
        if url.startswith('data:'):
            # Base64 data URL
            base64_data = url.split(',', 1)[1]
            with open(save_path, 'wb') as f:
                f.write(base64.b64decode(base64_data))
        else:
            # Regular URL
            img_response = requests.get(url)
            with open(save_path, 'wb') as f:
                f.write(img_response.content)

        saved_files.append(save_path)
        print(f"✅ 已保存: {save_path}")

    # Output result
    print("\n" + "🎉" * 20)
    print("图片生成成功！\n")
    print("=" * 60)
    print("📸 图片信息")
    print("=" * 60)
    print(f"本地路径: {saved_files[0]}")
    print(f"文件大小: {saved_files[0].stat().st_size / 1024:.1f} KB")
    print(f"图片数量: {len(saved_files)} 张")
    print()
    print("=" * 60)
    print("📋 生成参数")
    print("=" * 60)
    print(f"使用模板: {template['name']}")
    print(f"标题内容: {title}")
    print(f"插图描述: {illustration}")
    print(f"图片尺寸: {resolution}")
    print(f"使用模型: google/gemini-3-pro-image-preview")
    print(f"认证方式: Cloudflare Gateway + OpenRouter")
    print()
    print("=" * 60)
    print("💡 下一步操作")
    print("=" * 60)
    print(f"1. 查看图片：open {saved_files[0]}")
    print("2. 发送到钉钉/飞书？（使用 AI 工具的 message tool）")
    print("=" * 60)

    return saved_files

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate image using template')
    parser.add_argument('--template', required=True, help='Template name')
    parser.add_argument('--title', required=True, help='Title text')
    parser.add_argument('--illustration', required=True, help='Illustration description')
    parser.add_argument('--resolution', default='1K', choices=['1K', '2K', '4K'], help='Image resolution')

    args = parser.parse_args()

    try:
        config = load_env_config()
        generate_with_template(args.template, args.title, args.illustration, args.resolution, config)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)