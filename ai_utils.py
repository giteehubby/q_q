import asyncio
import openai
from loguru import logger
import aiohttp
import json
from typing import Optional, Dict, Any

class AIClient:
    """AI客户端，支持多种大模型API"""
    
    def __init__(self, api_key: str, base_url: str, model_name: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.timeout = timeout
        
        # 初始化OpenAI客户端
        self.openai_client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    async def chat_completion(self, messages: list, **kwargs) -> Optional[str]:
        """
        调用聊天补全API
        支持OpenAI格式的API
        """
        try:
            # 默认参数
            params = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "stream": False
            }
            
            # 使用异步方式调用OpenAI API
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.openai_client.chat.completions.create,
                    **params
                ),
                timeout=self.timeout
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            else:
                logger.error("API响应中没有choices")
                return None
                
        except asyncio.TimeoutError:
            logger.error(f"API调用超时 ({self.timeout}秒)")
            return "回复超时，请稍后再试。"
        except Exception as e:
            logger.error(f"调用AI API失败: {e}")
            return None
    
    async def chat_completion_with_fallback(self, user_message: str, system_prompt: str = None) -> str:
        """
        带有回退机制的聊天补全
        """
        # 构建消息
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user", 
            "content": user_message
        })
        
        # 尝试调用API
        response = await self.chat_completion(messages)
        
        if response is None:
            # 如果API调用失败，返回默认回复
            return "抱歉，我现在无法处理您的请求，请稍后再试。"
        
        return response

class MessageFormatter:
    """消息格式化工具"""
    
    @staticmethod
    def format_ai_response(response: str, max_length: int = 2000) -> str:
        """格式化AI回复"""
        if not response:
            return "抱歉，我没有获得有效回复。"
        
        # 清理响应内容
        response = response.strip()
        
        # 限制长度
        if len(response) > max_length:
            response = response[:max_length-3] + "..."
        
        return response
    
    @staticmethod
    def extract_user_message(content: str, bot_id: str) -> str:
        """从消息中提取用户输入，移除@机器人的部分"""
        # 移除@机器人的标记
        clean_content = content.replace(f"<@!{bot_id}>", "").strip()
        
        # 移除可能的其他@标记格式
        import re
        clean_content = re.sub(r'<@!\d+>', '', clean_content).strip()
        
        return clean_content

class ConversationContext:
    """对话上下文管理"""
    
    def __init__(self, max_history: int = 5):
        self.conversations = {}
        self.max_history = max_history
    
    def add_message(self, user_id: str, role: str, content: str):
        """添加消息到对话历史"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "role": role,
            "content": content
        })
        
        # 保持历史记录在限制范围内
        if len(self.conversations[user_id]) > self.max_history * 2:
            self.conversations[user_id] = self.conversations[user_id][-self.max_history * 2:]
    
    def get_messages(self, user_id: str, system_prompt: str = None) -> list:
        """获取用户的对话消息列表"""
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        if user_id in self.conversations:
            messages.extend(self.conversations[user_id])
        
        return messages
    
    def clear_conversation(self, user_id: str):
        """清除用户的对话历史"""
        if user_id in self.conversations:
            del self.conversations[user_id] 