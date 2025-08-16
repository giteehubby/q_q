import asyncio
import botpy
from botpy import logging
from botpy.message import GroupMessage, C2CMessage
import openai
from loguru import logger
import sys
import traceback

# 导入配置
try:
    from config import *
except ImportError:
    logger.error("请先复制 config_example.py 为 config.py 并填入你的配置信息")
    sys.exit(1)

# 配置日志
logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL)

# 配置OpenAI客户端
openai_client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

class MyClient(botpy.Client):
    async def on_ready(self):
        logger.info(f"机器人 {self.robot.name} 已启动!")

    async def on_group_at_message_create(self, message: GroupMessage):
        """处理群聊@消息"""
        try:
            # 获取消息内容，去除@机器人的部分
            content = message.content.strip()
            logger.info(f"收到群聊@消息: {content}")
            
            # 如果消息为空或只是@，返回帮助信息
            if not content or content == f"<@!{self.robot.id}>":
                await self._send_help_message(message)
                return
            
            # 移除@机器人的标记
            clean_content = content.replace(f"<@!{self.robot.id}>", "").strip()
            
            if not clean_content:
                await self._send_help_message(message)
                return
            
            # 调用大模型API
            response = await self._call_ai_api(clean_content)
            
            # 发送回复
            if response:
                await self._send_reply(message, response)
            else:
                await self._send_reply(message, "抱歉，我现在无法回复，请稍后再试。")
                
        except Exception as e:
            logger.error(f"处理群聊消息时出错: {e}")
            logger.error(traceback.format_exc())
            await self._send_reply(message, "出现了一些问题，请稍后再试。")

    async def on_c2c_message_create(self, message: C2CMessage):
        """处理私聊消息"""
        try:
            content = message.content.strip()
            logger.info(f"收到私聊消息: {content}")
            
            if not content:
                await self._send_help_message_c2c(message)
                return
            
            # 调用大模型API
            response = await self._call_ai_api(content)
            
            # 发送回复
            if response:
                await self._send_reply_c2c(message, response)
            else:
                await self._send_reply_c2c(message, "抱歉，我现在无法回复，请稍后再试。")
                
        except Exception as e:
            logger.error(f"处理私聊消息时出错: {e}")
            logger.error(traceback.format_exc())
            await self._send_reply_c2c(message, "出现了一些问题，请稍后再试。")

    async def _call_ai_api(self, user_message: str) -> str:
        """调用大模型API"""
        try:
            logger.info(f"调用AI API，用户消息: {user_message}")
            
            # 构建对话消息
            messages = [
                {
                    "role": "system", 
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ]
            
            # 调用OpenAI API
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    openai_client.chat.completions.create,
                    model=MODEL_NAME,
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                ),
                timeout=RESPONSE_TIMEOUT
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # 限制回复长度
            if len(ai_response) > MAX_MESSAGE_LENGTH:
                ai_response = ai_response[:MAX_MESSAGE_LENGTH-3] + "..."
            
            logger.info(f"AI回复: {ai_response}")
            return ai_response
            
        except asyncio.TimeoutError:
            logger.error("AI API调用超时")
            return "回复超时，请稍后再试。"
        except Exception as e:
            logger.error(f"调用AI API时出错: {e}")
            return None

    async def _send_reply(self, message: GroupMessage, reply_content: str):
        """发送群聊回复"""
        try:
            await message.reply(content=reply_content)
            logger.info(f"已发送群聊回复: {reply_content}")
        except Exception as e:
            logger.error(f"发送群聊回复失败: {e}")

    async def _send_reply_c2c(self, message: C2CMessage, reply_content: str):
        """发送私聊回复"""
        try:
            await message.reply(content=reply_content)
            logger.info(f"已发送私聊回复: {reply_content}")
        except Exception as e:
            logger.error(f"发送私聊回复失败: {e}")

    async def _send_help_message(self, message: GroupMessage):
        """发送群聊帮助信息"""
        help_text = "👋 你好！我是贾维斯，@我并提问即可获得回复。\n例如：@我 今天天气怎么样？"
        await self._send_reply(message, help_text)

    async def _send_help_message_c2c(self, message: C2CMessage):
        """发送私聊帮助信息"""
        help_text = "👋 你好！我是AI助手，直接发送消息即可获得回复。"
        await self._send_reply_c2c(message, help_text)

    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        try:
            # 尝试从配置文件读取自定义prompt
            from config import SYSTEM_PROMPT
            return SYSTEM_PROMPT
        except ImportError:
            # 如果配置文件中没有SYSTEM_PROMPT，使用默认prompt
            return """你是贾维斯，一个智能的QQ群聊助手。你的特点：

🤖 **身份**：我是贾维斯，钢铁侠的AI助手，现在为QQ群友服务
💡 **能力**：我可以回答问题、协助编程、创作内容、解决问题
🎯 **风格**：友善、专业、有一点幽默感，像真正的贾维斯一样
📝 **回复**：简洁明了，不废话，直接有用

请用中文回复，保持贾维斯的专业和智能风格。"""

async def main():
    """主函数"""
    # 设置机器人的意图
    intents = botpy.Intents(
        public_messages=True,  # 监听公域消息
        guild_messages=True,   # 监听群组消息
        direct_message=True,   # 监听私信
    )
    
    # 创建机器人客户端
    client = MyClient(intents=intents)
    
    try:
        # 启动机器人
        await client.start(appid=BOT_APPID, secret=BOT_SECRET)
    except Exception as e:
        logger.error(f"启动机器人失败: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    # 运行机器人
    asyncio.run(main()) 