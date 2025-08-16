#!/usr/bin/env python3
"""
QQ AI聊天机器人一键设置脚本
"""

import os
import sys
import shutil
from loguru import logger

def setup_config():
    """设置配置文件"""
    if os.path.exists('config.py'):
        logger.info("配置文件 config.py 已存在")
        choice = input("是否要重新创建配置文件？(y/N): ").lower()
        if choice != 'y':
            return
    
    if os.path.exists('config_example.py'):
        shutil.copy('config_example.py', 'config.py')
        logger.info("✓ 已创建 config.py 配置文件")
        logger.info("请编辑 config.py 文件，填入你的机器人配置信息")
    else:
        logger.error("❌ 找不到 config_example.py 文件")

def show_qq_bot_guide():
    """显示QQ机器人申请指南"""
    print("\n" + "="*60)
    print("📋 QQ机器人申请指南")
    print("="*60)
    print("1. 访问 QQ开放平台: https://q.qq.com/bot/")
    print("2. 使用QQ号登录")
    print("3. 创建机器人应用")
    print("4. 获取 AppID 和 Secret")
    print("5. 配置机器人权限和功能")
    print("\n⚠️  注意事项:")
    print("• 需要企业资质或个人开发者认证")
    print("• 机器人需要审核通过才能使用")
    print("• 确保遵守腾讯的使用条款")
    print("="*60)

def show_ai_api_guide():
    """显示AI API获取指南"""
    print("\n" + "="*60)
    print("🤖 AI API获取指南")
    print("="*60)
    print("支持的AI服务提供商:")
    print("1. OpenAI (https://platform.openai.com/)")
    print("   - 注册账号并获取API Key")
    print("   - 模型: gpt-3.5-turbo, gpt-4 等")
    print()
    print("2. DeepSeek (https://platform.deepseek.com/)")
    print("   - 国内AI服务，支持中文")
    print("   - 模型: deepseek-chat")
    print()
    print("3. Moonshot/Kimi (https://platform.moonshot.cn/)")
    print("   - 月之暗面AI服务")
    print("   - 模型: moonshot-v1-8k")
    print()
    print("4. Azure OpenAI")
    print("   - 微软Azure平台的OpenAI服务")
    print("   - 企业级服务，稳定性好")
    print("="*60)

def create_demo_config():
    """创建演示配置"""
    demo_config = '''# QQ机器人演示配置
# ⚠️ 这是一个演示配置，请替换为你的真实配置

# QQ机器人配置 - 从QQ开放平台获取
BOT_APPID = "demo_appid_12345"
BOT_SECRET = "demo_secret_abcdef"

# AI API配置 - 选择一个AI服务提供商
# OpenAI配置示例
OPENAI_API_KEY = "sk-demo_key_here"
OPENAI_BASE_URL = "https://api.openai.com/v1"
MODEL_NAME = "gpt-3.5-turbo"

# 如果使用DeepSeek，取消注释以下配置
# OPENAI_API_KEY = "sk-demo_deepseek_key"
# OPENAI_BASE_URL = "https://api.deepseek.com/v1"
# MODEL_NAME = "deepseek-chat"

# 如果使用Moonshot，取消注释以下配置
# OPENAI_API_KEY = "sk-demo_moonshot_key"
# OPENAI_BASE_URL = "https://api.moonshot.cn/v1"
# MODEL_NAME = "moonshot-v1-8k"

# 机器人设置
MAX_MESSAGE_LENGTH = 2000  # 最大回复长度
RESPONSE_TIMEOUT = 30  # API超时时间（秒）

# 日志设置
LOG_LEVEL = "INFO"  # 可选: DEBUG, INFO, WARNING, ERROR
'''
    
    with open('config_demo.py', 'w', encoding='utf-8') as f:
        f.write(demo_config)
    
    logger.info("✓ 已创建演示配置文件 config_demo.py")

def main():
    """主函数"""
    print("🤖 QQ AI聊天机器人设置向导")
    print("="*50)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        logger.error("❌ 需要Python 3.8或更高版本")
        return
    
    logger.info(f"✓ Python版本: {sys.version}")
    
    # 设置配置文件
    setup_config()
    
    # 创建演示配置
    create_demo_config()
    
    # 显示指南
    show_qq_bot_guide()
    show_ai_api_guide()
    
    print("\n" + "="*60)
    print("🚀 下一步操作:")
    print("="*60)
    print("1. 编辑 config.py 文件，填入你的真实配置")
    print("2. 安装依赖: pip install -r requirements.txt")
    print("3. 启动机器人: python run.py")
    print("="*60)
    
    logger.info("✅ 设置完成！")

if __name__ == "__main__":
    main() 