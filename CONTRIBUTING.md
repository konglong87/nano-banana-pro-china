# Contributing to nano-banana-pro-china

感谢你有兴趣为 nano-banana-pro-china 做贡献！

## 🤝 如何贡献

### 报告Bug

如果你发现了bug，请创建一个Issue，包含：
1. 清晰的标题和描述
2. 复现步骤
3. 预期行为
4. 实际行为
5. 环境信息（OS、Python版本等）

### 提出新功能

如果你有新功能建议，请创建一个Issue，包含：
1. 功能描述
2. 使用场景
3. 可能的实现方式

### 提交代码

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📝 代码规范

### Python代码

- 遵循PEP 8规范
- 使用有意义的变量名
- 添加适当的注释和文档字符串
- 编写单元测试

### 提交信息

使用清晰的提交信息：
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 代码格式调整`
- `refactor: 重构代码`
- `test: 添加测试`
- `chore: 构建过程或辅助工具的变动`

## 🔒 安全问题

如果你发现了安全漏洞，请**不要**在公开Issue中报告。
请发送邮件至：[your-email@example.com]

## 📋 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-username/nano-banana-pro-china.git
cd nano-banana-pro-china

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入你的API keys

# 运行测试
python3 scripts/list_templates.py
```

## ✅ Pull Request检查清单

- [ ] 代码遵循项目的编码规范
- [ ] 已进行自我代码审查
- [ ] 代码有适当的注释
- [ ] 文档已更新（如需要）
- [ ] 没有引入新的警告
- [ ] 添加了测试（如适用）
- [ ] 所有测试都通过
- [ ] 依赖项已在requirements.txt中列出

## 📧 联系方式

- 项目维护者：[Your Name]
- Email：[your-email@example.com]
- GitHub：[your-username]

感谢你的贡献！🎉