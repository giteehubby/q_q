# QQ Bot 配置示例
# 复制此文件为 config.py 并填入你的实际配置

# QQ机器人配置 - 从QQ开放平台获取
BOT_APPID = "your_bot_appid_here"
BOT_SECRET = "your_bot_secret_here"

# 大模型API配置
OPENAI_API_KEY = "your_openai_api_key_here"
OPENAI_BASE_URL = "https://api.openai.com/v1"  # 或其他兼容的API地址
MODEL_NAME = "gpt-3.5-turbo"

# 机器人设置
MAX_MESSAGE_LENGTH = 2000  # 最大回复长度
RESPONSE_TIMEOUT = 30  # API超时时间（秒）
CONTEXT_HISTORY_LENGTH = 5  # 上下文历史消息数量

# 日志设置
LOG_LEVEL = "INFO" 

# 系统提示词设置（可选）

SYSTEM_PROMPT = """你是贾维斯，一个智能的QQ群聊助手。

🎯 **角色定位**：
- 我是李佳伟的人工智能管家贾维斯
- 现在为QQ群友提供智能服务
- 保持专业、高效、略带幽默的风格

💡 **核心能力**：
- 回答各种问题和提供建议
- 协助编程和技术问题
- 创作内容（诗歌、故事、文案等）
- 数据分析和计算
- 学习指导和知识解答

🗣️ **交流风格**：
- 简洁明了，直接有用
- 保持礼貌和专业
- 适当使用emoji增加亲和力
- 必要时展现一点AI的幽默感

请始终用中文回复""" 