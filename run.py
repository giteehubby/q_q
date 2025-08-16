#!/usr/bin/env python3
"""
QQ AI聊天机器人启动脚本
"""

import os
import sys
import asyncio
from loguru import logger

def check_config():
    """检查配置文件"""
    if not os.path.exists('config.py'):
        logger.error("配置文件不存在！")
        logger.info("请按照以下步骤设置:")
        logger.info("1. 复制 config_example.py 为 config.py")
        logger.info("2. 编辑 config.py 填入你的配置信息")
        logger.info("3. 重新运行此脚本")
        return False
    return True

def check_dependencies():
    """检查依赖包"""
    try:
        import botpy
        import openai
        import loguru
        logger.info("所有依赖包已安装 ✓")
        return True
    except ImportError as e:
        logger.error(f"缺少依赖包: {e}")
        logger.info("请运行: pip install -r requirements.txt")
        return False

async def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("QQ AI聊天机器人启动中...")
    logger.info("=" * 50)
    
    # 检查配置和依赖
    if not check_config():
        return
    
    if not check_dependencies():
        return
    
    # 导入并启动机器人
    try:
        from qq_bot import main as bot_main
        logger.info("配置检查完成，启动机器人...")
        await bot_main()
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭机器人...")
    except Exception as e:
        logger.error(f"启动失败: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序已退出")
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        sys.exit(1) 