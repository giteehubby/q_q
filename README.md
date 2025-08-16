# QQ AI聊天机器人

一个基于QQ频道机器人API和大模型API的智能聊天机器人，当有人@机器人时会自动调用AI进行回复。

## ✨ 功能特性

- 🤖 **智能回复**: 使用大模型API（OpenAI/兼容API）进行智能对话
- 📱 **QQ群聊支持**: 支持QQ群聊@回复和私聊
- 🔄 **异步处理**: 高性能异步架构，支持并发处理
- 🛡️ **错误处理**: 完善的错误处理和回退机制
- 📝 **日志记录**: 详细的日志记录，便于调试和监控
- ⚙️ **易于配置**: 简单的配置文件，支持多种AI服务

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- pip
- 需要在[qq开放平台](https://bot.q.qq.com/)注册机器人，获得id和密码复制到config.py中；
- 测试时需要添加ip白名单（自己的公网ip地址，可通过https://www.whatismyip.com/获得）
- 需要openai的url及api_key

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置机器人

#### 3.1 获取QQ机器人凭证

1. 访问 [QQ开放平台](https://q.qq.com/bot/)
2. 创建机器人应用
3. 获取 `AppID` 和 `Secret`

#### 3.2 获取AI API密钥

支持以下AI服务：
- OpenAI GPT
- Azure OpenAI
- 其他兼容OpenAI API格式的服务（如DeepSeek、Moonshot等）

#### 3.3 创建配置文件

```bash
cp config_example.py config.py
```

编辑 `config.py` 文件，填入你的配置：

```python
# QQ机器人配置
BOT_APPID = "your_bot_appid_here"
BOT_SECRET = "your_bot_secret_here"

# AI API配置  
OPENAI_API_KEY = "your_api_key_here"
OPENAI_BASE_URL = "https://api.openai.com/v1"  # 或其他API地址
MODEL_NAME = "gpt-3.5-turbo"

# 可选配置
MAX_MESSAGE_LENGTH = 2000
RESPONSE_TIMEOUT = 30
LOG_LEVEL = "INFO"
```

### 4. 启动机器人

```bash
python run.py
```

或者直接运行：

```bash
python qq_bot.py
```

## 📖 使用说明

### 群聊使用

在QQ群中@机器人并提问：

```
@机器人 你好，今天天气怎么样？
@机器人 帮我写一个Python函数
```

### 私聊使用

直接向机器人发送私聊消息即可获得回复。

## 🔧 配置说明

### config.py 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `BOT_APPID` | QQ机器人应用ID | `"123456789"` |
| `BOT_SECRET` | QQ机器人密钥 | `"your_secret"` |
| `OPENAI_API_KEY` | AI API密钥 | `"sk-..."` |
| `OPENAI_BASE_URL` | AI API地址 | `"https://api.openai.com/v1"` |
| `MODEL_NAME` | 使用的模型名称 | `"gpt-3.5-turbo"` |
| `MAX_MESSAGE_LENGTH` | 最大回复长度 | `2000` |
| `RESPONSE_TIMEOUT` | API超时时间（秒） | `30` |
| `LOG_LEVEL` | 日志级别 | `"INFO"` |

### 支持的AI服务

#### OpenAI
```python
OPENAI_API_KEY = "sk-..."
OPENAI_BASE_URL = "https://api.openai.com/v1"
MODEL_NAME = "gpt-3.5-turbo"
```

#### Azure OpenAI
```python
OPENAI_API_KEY = "your_azure_key"
OPENAI_BASE_URL = "https://your-resource.openai.azure.com/openai/deployments/your-deployment"
MODEL_NAME = "gpt-35-turbo"
```

#### DeepSeek
```python
OPENAI_API_KEY = "sk-..."
OPENAI_BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"
```

#### Moonshot (Kimi)
```python
OPENAI_API_KEY = "sk-..."
OPENAI_BASE_URL = "https://api.moonshot.cn/v1"
MODEL_NAME = "moonshot-v1-8k"
```

## 📁 项目结构

```
aichat/
├── qq_bot.py           # QQ机器人主程序
├── ai_utils.py         # AI工具类和消息处理
├── run.py              # 启动脚本
├── config_example.py   # 配置示例文件
├── requirements.txt    # 依赖包列表
├── .gitignore         # Git忽略文件
└── README.md          # 说明文档
```

## 🔍 故障排除

### 常见问题

1. **配置文件错误**
   ```
   错误: 请先复制 config_example.py 为 config.py 并填入你的配置信息
   ```
   解决: 确保已创建 `config.py` 文件并填入正确配置

2. **依赖包缺失**
   ```
   错误: 缺少依赖包
   ```
   解决: 运行 `pip install -r requirements.txt`

3. **API调用失败**
   ```
   错误: 调用AI API失败
   ```
   解决: 检查API密钥、网络连接和API地址是否正确

4. **机器人无法启动**
   ```
   错误: 启动机器人失败
   ```
   解决: 检查QQ机器人AppID和Secret是否正确

### 调试模式

将配置中的 `LOG_LEVEL` 设置为 `"DEBUG"` 可以获得更详细的日志信息。

## 📝 开发说明

### 添加新功能

可以在 `qq_bot.py` 中的 `MyClient` 类中添加新的消息处理方法。

### 自定义AI回复

可以修改 `ai_utils.py` 中的 `AIClient` 类来自定义AI回复逻辑。

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## ⚠️ 注意事项

1. 请妥善保管你的API密钥，不要提交到公共代码仓库
2. 注意API调用频率限制，避免超出配额
3. 机器人需要适当的权限才能在QQ群中正常工作
4. 遵守相关平台的使用条款和政策

## 📞 支持

如果遇到问题，可以：
1. 查看日志文件了解错误详情
2. 检查配置是否正确
3. 提交Issue描述问题 