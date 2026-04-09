# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Template-based image generation
- Free-form image editing
- Support for 3 built-in templates
- Cloudflare Gateway integration for China access
- Dual authentication mechanism
- Chinese-friendly output format

## [1.0.0] - 2026-04-09

### Added
- **Core Features**
  - Template-based image generation using predefined templates
  - Free-form image editing with natural language instructions
  - Support for single and multiple image editing
  - Multi-resolution support (1K/2K/4K)
  
- **Templates**
  - Corporate Culture template (企业文化)
  - Product Promotion template (产品宣传)
  - Spring Festival template (春节海报)
  
- **API Integration**
  - OpenRouter API integration
  - Cloudflare Gateway support for China access
  - Dual authentication (Gateway + OpenRouter)
  - Gemini 3 Pro Image model support
  
- **Scripts**
  - `list_templates.py` - List available templates
  - `verify_template.py` - Verify template configuration
  - `generate_with_template.py` - Generate images with templates
  - `edit_image.py` - Edit images with instructions
  
- **Documentation**
  - Comprehensive README.md
  - SKILL.md with detailed usage instructions
  - Test reports
  - Contributing guidelines
  
- **Developer Experience**
  - Environment configuration via .env
  - Example configuration (.env.example)
  - Chinese-friendly output formatting
  - Detailed error messages

### Security
- Environment variables for sensitive data
- No hardcoded API keys in source code
- .gitignore protection for .env files

### Tested
- ✅ All 6 test cases passed (3 editing + 3 template)
- ✅ Cloudflare Gateway authentication verified
- ✅ Multi-resolution generation tested
- ✅ Chinese text rendering validated
- ✅ Large file handling (6.3MB base images)

---

## Version History

- **1.0.0** (2026-04-09): Initial release
  - Template generation and image editing functionality
  - Cloudflare Gateway integration
  - Production-ready

---

## Roadmap

### Planned Features
- [ ] Web UI interface
- [ ] More built-in templates
- [ ] Template creation wizard
- [ ] Batch processing
- [ ] Image compression options
- [ ] Custom model support
- [ ] API rate limiting and retry logic
- [ ] Image history management
- [ ] Direct messaging integration (DingTalk/Lark)

### Improvements
- [ ] Performance optimization
- [ ] Better error handling
- [ ] More detailed logging
- [ ] Unit test coverage
- [ ] CI/CD pipeline
- [ ] Docker support

---

**Note**: This project is under active development. Breaking changes may occur in minor versions before 1.0.0.