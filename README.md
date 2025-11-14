# ChatSensei Lite

一个基于 FastAPI 的智能消息助手原型，用于 NLP 课程项目。

## 项目简介

ChatSensei Lite 是一个消息助手原型，可以：
- 分析聊天消息的语气（疑问、积极、消极、中性）
- 生成三种不同风格的回复建议：
  - 🎩 **礼貌风格**：正式、尊重、得体
  - 😄 **幽默风格**：轻松、有趣、带emoji
  - 💬 **直接风格**：简洁、清晰、直截了当
- 根据用户反馈学习偏好（简单的强化学习/赌博机算法）
- 支持 OpenAI API 或纯启发式方法（无需外部依赖）

## 功能特点

- ✅ 简单直观的 Web 界面
- ✅ 实时语气分析
- ✅ 多风格回复生成
- ✅ 用户偏好学习（上下文赌博机）
- ✅ 支持在线（OpenAI）和离线（启发式）模式
- ✅ 响应式设计，支持移动端

## 技术栈

- **后端**: Python 3.8+, FastAPI, Uvicorn
- **前端**: HTML5, Vanilla JavaScript, Pico.css
- **模板引擎**: Jinja2
- **AI**: OpenAI API (可选)

## 安装步骤

### 1. 克隆或下载项目

```bash
cd chatsensei_lite
```

### 2. 创建虚拟环境

```bash
python -m venv venv
```

### 3. 激活虚拟环境

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置（可选）

### 使用 OpenAI API

如果你想使用 OpenAI 的 GPT 模型生成更智能的建议，需要设置 API 密钥：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**注意**: 
- 没有设置 API 密钥也可以运行！应用会自动使用内置的启发式方法。
- 你可以在 [OpenAI Platform](https://platform.openai.com/api-keys) 获取 API 密钥。

## 运行应用

### 启动服务器

```bash
uvicorn app:app --reload
```

或者直接运行：

```bash
python app.py
```

### 访问应用

在浏览器中打开：

```
http://127.0.0.1:8000/
```

## 使用说明

1. **粘贴聊天消息**
   - 在文本框中粘贴你收到的聊天消息
   - 可以是 WhatsApp、微信、Discord 等任何聊天内容

2. **分析 & 生成建议**
   - 点击"分析 & 生成建议"按钮
   - 系统会检测语气并生成三种风格的回复

3. **选择和反馈**
   - 每个建议有两个按钮：
     - **使用 👍**: 表示你喜欢这个风格（增加该风格的权重）
     - **不好 👎**: 表示你不喜欢（减少该风格的权重）

4. **查看偏好**
   - 页面底部显示你对各个风格的偏好权重
   - 权重越高，表示系统认为你越喜欢该风格

## 项目结构

```
chatsensei_lite/
├── app.py                 # FastAPI 主应用
├── requirements.txt       # Python 依赖
├── README.md             # 项目文档
├── templates/
│   └── index.html        # 主页面模板
└── static/
    ├── script.js         # 前端 JavaScript 逻辑
    └── styles.css        # 自定义 CSS 样式
```

## API 端点

### GET /
返回主页面（HTML）

### POST /suggest
分析聊天内容并生成建议

**请求体:**
```json
{
  "chat": "你好，周末有空吗？"
}
```

**响应:**
```json
{
  "tone": "question",
  "suggestions": {
    "polite": "感谢你的邀请！让我想想，稍后回复你。",
    "funny": "哈哈，让我想想，稍后回复你。😂",
    "straightforward": "让我想想，稍后回复你。"
  },
  "preferences": {
    "polite": 1.0,
    "funny": 1.0,
    "straightforward": 1.0
  }
}
```

### POST /feedback
提交用户反馈

**请求体:**
```json
{
  "chosen_style": "polite",
  "good": true
}
```

**响应:**
```json
{
  "preferences": {
    "polite": 2.0,
    "funny": 1.0,
    "straightforward": 1.0
  }
}
```

## 强化学习机制

本项目使用简单的**上下文赌博机（Contextual Bandit）**算法：

- 每种风格维护一个权重值（初始为 1.0）
- 用户点击"使用 👍"时，权重 +1.0
- 用户点击"不好 👎"时，权重 -0.5（但最小保持 1.0）
- 权重反映用户对该风格的偏好程度

这是一个适合课程项目的简化 RL 实现，展示了基本的偏好学习概念。

## 开发说明

### 启发式模式（无 API）

如果没有设置 `OPENAI_API_KEY`，应用使用以下规则：

**语气检测:**
- 以 `?` 或 `？` 结尾 → 疑问
- 包含正面词（thanks, great, awesome...）→ 积极
- 包含负面词（hate, bad, terrible...）→ 消极
- 其他 → 中性

**建议生成:**
- 根据检测的语气选择基础回复
- 为不同风格添加相应的包装文字

### OpenAI 模式

使用 `gpt-4o-mini` 模型，通过精心设计的 prompt 生成自然、多样化的建议。

## 故障排除

### 问题：模块未找到错误

确保你已激活虚拟环境并安装了所有依赖：
```bash
pip install -r requirements.txt
```

### 问题：OpenAI API 调用失败

- 检查 API 密钥是否正确设置
- 确认网络连接正常
- 应用会自动回退到启发式模式，不会崩溃

### 问题：端口 8000 已被占用

使用不同的端口：
```bash
uvicorn app:app --reload --port 8001
```

## 未来改进

- [ ] 添加用户账户系统
- [ ] 持久化偏好数据（数据库）
- [ ] 支持更多语言
- [ ] 更复杂的 RL 算法（如 Thompson Sampling）
- [ ] 上下文感知的建议生成
- [ ] 批量处理多条消息

## 许可证

本项目仅用于教育目的（NLP 课程项目）。

## 作者

NLP 课程项目组

## 反馈

如有问题或建议，请提交 Issue 或联系项目团队。

