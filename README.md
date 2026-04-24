# 🎨skills🎨 nano-banana && GPT Image2 use in china 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**国内直接可用的 AI 图片生成和编辑工具** | AI Image Generation & Editing Tool for China

通过 Cloudflare Gateway + OpenRouter + Gemini 3 Pro Image，完美解决国内访问问题，无需科学上网。

## ✨ 特性

- 🎨 **模板生成**：使用预定义模板快速生成统一风格的图片
- ✏️ **图片编辑**：通过自然语言指令编辑现有图片
- 🇨🇳 **国内友好**：通过 Cloudflare Gateway 解决国内访问问题
- 🔐 **双重认证**：Gateway + OpenRouter 双重认证，安全可靠
- 📐 **多分辨率**：支持 1K/2K/4K 多种分辨率
- 📋 **内置模板**：3个常用模板开箱即用
- 🖼️ **多图支持**：支持单图编辑和多图合并
- 🌏 **中文优化**：中文友好的输出格式和错误提示

## 🚀 快速开始

<details>
<summary><b>📺 观看快速演示视频</b></summary>

_即将推出_
</details>

### 前置要求

- Python 3.8+
- OpenRouter API Key
- Cloudflare Gateway 配置（国内访问必需）

### 安装

#### 方式一：作为 Claude Code / OpenClaw Skills 安装

**适用于 Claude Code 或 OpenClaw 用户**

```bash
# 1. 进入 skills 目录
cd ~/.openclaw/workspace/skills/
# 或者对于 Claude Code
cd ~/.claude/skills/

# 2. 克隆仓库
git clone https://github.com/konglong87/nano-banana-pro-china.git

# 3. 安装 Python 依赖
cd nano-banana-pro-china
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API keys
vim .env  # 或使用其他编辑器
```

**验证安装**：
```bash
# 测试模板列表功能
python3 scripts/list_templates.py

# 应该看到3个可用模板
```

**在 Claude、openclaw 中使用**：
```
用户：使用春节海报模板生成图片，标题"2026新春快乐"，插图"一家人团聚"
Claude、openclaw：我会使用 nano-banana-pro-china skill 来生成图片...
```

#### 方式二：独立使用（通用安装）

**适用于所有用户**

```bash
# 1. 克隆仓库到任意目录
git clone https://github.com/konglong87/nano-banana-pro-china.git
cd nano-banana-pro-china

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API keys
nano .env  # 或使用你喜欢的编辑器
```

### 配置 API Keys

编辑 `.env` 文件：

```bash
# OpenRouter API Key (必需)
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here

# Cloudflare Gateway URL (必需，国内访问)
OPENROUTER_BASE_URL=https://gateway.ai.cloudflare.com/v1/YOUR_ACCOUNT_ID/YOUR_GATEWAY_ID/openrouter/v1/chat/completions

# Cloudflare Gateway Token (必需)
CF_AIG_TOKEN=cfut_your-cloudflare-gateway-token-here
```

**获取 API Keys**：

1. **OpenRouter API Key**:
   - 访问 https://openrouter.ai
   - 注册并登录
   - 进入 https://openrouter.ai/keys
   - 创建新的 API Key

2. **Cloudflare Gateway 配置**:
   - 访问 https://dash.cloudflare.com
   - 进入 AI Gateway 页面
   - 创建新 Gateway（如果还没有）
   - 获取 Account ID 和 Gateway ID
   - 在 Tokens 标签页创建 Gateway Token

3. **构建 Base URL**:
   ```
   https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/{GATEWAY_ID}/openrouter/v1/chat/completions
   ```
   将 `{ACCOUNT_ID}` 和 `{GATEWAY_ID}` 替换为你的实际值

### 基础使用

#### 1️⃣ 列出可用模板

```bash
python3 scripts/list_templates.py
```

输出：
```
📋 Available Wanxiang Templates:

🎨 企业文化
   Description: Corporate culture poster...
   Title: 底部居中
   Illustration: 左侧
   Dimensions: 1280x720
```

#### 2️⃣ 使用模板生成图片

```bash
python3 scripts/generate_with_template.py \
  --template "春节海报" \
  --title "2026新春快乐" \
  --illustration "一家人团聚吃年夜饭，红灯笼，烟花" \
  --resolution 1K
```

#### 3️⃣ 编辑图片

```bash
python3 scripts/edit_image.py \
  --images test_img/img.png \
  --instruction "把标题改为：新产品发布" \
  --resolution 2K
```

#### 4️⃣ 多图合并

```bash
python3 scripts/edit_image.py \
  --images bg.png,logo.png \
  --instruction "把logo放在背景图片中央" \
  --resolution 4K
```

## 📖 详细文档

### 模板生成

**验证模板**：
```bash
python3 scripts/verify_template.py --template "春节海报"
```

**生成图片**：
```bash
python3 scripts/generate_with_template.py \
  --template "企业文化" \
  --title "追求卓越，共创未来" \
  --illustration "团队合作场景，现代办公室" \
  --resolution 2K
```

**参数说明**：
- `--template`: 模板名称（必需）
- `--title`: 标题文本（必需）
- `--illustration`: 插图描述（必需）
- `--resolution`: 分辨率（可选，默认1K）- 1K/2K/4K

### 图片编辑

**单图编辑**：
```bash
python3 scripts/edit_image.py \
  --images img.png \
  --instruction "修改标题为：如何寻找诱因？" \
  --resolution 1K
```

**多图合并**：
```bash
python3 scripts/edit_image.py \
  --images person.png,background.png \
  --instruction "把人物放在背景图片中央" \
  --resolution 4K
```

**参数说明**：
- `--images`: 图片路径，多张用逗号分隔（必需）
- `--instruction`: 编辑指令（必需）
- `--resolution`: 分辨率（可选，默认1K）

## 🎨 内置模板

### 1. 企业文化 (corporate-culture)
- **尺寸**: 1280x720
- **标题位置**: 底部居中
- **插图位置**: 左侧
- **风格**: 专业商务风格

### 2. 产品宣传 (product-promotion)
- **尺寸**: 1024x1024
- **标题位置**: 左上角
- **插图位置**: 中央
- **风格**: 现代简约风格

### 3. 春节海报 (spring-festival)
- **尺寸**: 2048x2048
- **标题位置**: 顶部居中
- **插图位置**: 右侧
- **风格**: 传统中国喜庆风格

## 🔧 API 配置详解

### Cloudflare Gateway 配置（国内必需）

**为什么需要 Gateway？**
- OpenRouter API 在国内无法直接访问
- 通过 Cloudflare Gateway 中转，实现国内访问

**配置步骤**：

1. 创建 Cloudflare Gateway
   - 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
   - 进入 AI Gateway 页面
   - 创建新 Gateway

2. 获取配置信息
   - Account ID: 在 Gateway 页面可见
   - Gateway ID: 你创建的 Gateway 名称
   - Gateway Token: 在 Tokens 标签页创建

3. 构建 Base URL
   ```
   https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/{GATEWAY_ID}/openrouter/v1/chat/completions
   ```

### 双重认证机制

所有API调用需要双重认证：

```python
headers = {
    'Authorization': f'Bearer {OPENROUTER_API_KEY}',      # OpenRouter认证
    'cf-aig-authorization': f'Bearer {CF_AIG_TOKEN}'      # Gateway认证
}
```

## 📂 项目结构

```
nano-banana-pro-china/
├── scripts/                    # 核心脚本
│   ├── list_templates.py      # 列出模板
│   ├── verify_template.py     # 验证模板
│   ├── generate_with_template.py  # 模板生成
│   └── edit_image.py          # 图片编辑
├── templates/                  # 模板目录
│   ├── corporate-culture/
│   ├── product-promotion/
│   └── spring-festival/
├── materials/                  # 输出目录
│   ├── raw/                   # 模板生成输出
│   └── raw_edit/              # 图片编辑输出
├── test_img/                   # 测试图片
├── .env.example               # 环境变量示例
├── requirements.txt           # Python依赖
├── SKILL.md                   # 详细使用文档
├── CONTRIBUTING.md            # 贡献指南
├── CHANGELOG.md               # 变更日志
└── LICENSE                    # MIT许可证
```

## 🧪 测试

查看完整的测试报告：
- [图片编辑测试报告](test_img/TEST_REPORT.md)
- [模板生成测试报告](test_img/TEMPLATE_TEST_REPORT.md)

测试状态：✅ 全部通过 (6/6)

## 🌟 特性对比

| 特性 | nano-banana-pro-china | 其他方案 |
|------|----------------------|---------|
| 国内访问 | ✅ 完美支持 | ❌ 需要科学上网 |
| API稳定性 | ✅ 双重认证 | ⚠️ 单一认证 |
| 模板系统 | ✅ 内置3个模板 | ❌ 无模板 |
| 图片编辑 | ✅ 支持编辑 | ⚠️ 仅生成 |
| 多图合并 | ✅ 支持 | ❌ 不支持 |
| 中文输出 | ✅ 完美支持 | ⚠️ 部分支持 |

## ❓ 常见问题

<details>
<summary><b>Q: 为什么需要 Cloudflare Gateway？</b></summary>

**A**: OpenRouter API 在国内无法直接访问。通过 Cloudflare Gateway 中转，可以实现国内无障碍访问，无需科学上网。
</details>

<details>
<summary><b>Q: 如何获取 OpenRouter API Key？</b></summary>

**A**: 
1. 访问 https://openrouter.ai
2. 注册账号
3. 进入 https://openrouter.ai/keys
4. 创建新的 API Key
</details>

<details>
<summary><b>Q: 如何配置 Cloudflare Gateway？</b></summary>

**A**: 详见 [API 配置详解](#api-配置详解) 章节。
</details>

<details>
<summary><b>Q: 支持哪些图片格式？</b></summary>

**A**: 支持 PNG、JPEG、GIF、WebP 等常见格式。
</details>

<details>
<summary><b>Q: 生成图片的分辨率如何选择？</b></summary>

**A**: 
- 1K (1024px): 快速测试，文件小
- 2K (2048px): 平衡质量和速度
- 4K (4096px): 高质量，文件大
</details>

<details>
<summary><b>Q: 生成速度慢怎么办？</b></summary>

**A**: 
- 使用1K分辨率测试
- 简化提示词
- 检查网络连接
- 尝试非高峰时段
</details>

## 🤝 贡献

欢迎贡献代码、报告Bug、提出新功能建议！

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [OpenRouter](https://openrouter.ai) - API平台
- [Cloudflare](https://cloudflare.com) - Gateway服务
- [Google Gemini](https://ai.google.dev) - 图片生成模型
- 所有贡献者

## 📧 联系方式

- Issues: https://github.com/your-username/nano-banana-pro-china/issues
- Discussions: https://github.com/your-username/nano-banana-pro-china/discussions

---

**Star ⭐ 本项目以获得最新更新！**

Made with ❤️ by the nano-banana-pro-china team
