# ChatSensei Lite - 快速开始指南

## 🚀 10秒快速启动

### macOS / Linux

```bash
cd chatsensei_lite
./start.sh
```

### Windows

```cmd
cd chatsensei_lite
start.bat
```

然后在浏览器打开: http://127.0.0.1:8000

---

## 📝 基本使用

1. **粘贴聊天内容**
   ```
   朋友: 你周末有空吗？我们去看电影吧！
   ```

2. **点击"分析 & 生成建议"**
   
3. **查看三种风格的回复建议**
   - 🎩 礼貌风格
   - 😄 幽默风格  
   - 💬 直接风格

4. **给出反馈**
   - 点击 "使用 👍" → 增加该风格权重
   - 点击 "不好 👎" → 减少该风格权重

5. **查看你的偏好学习**
   - 页面底部会实时显示各风格的权重值

---

## 🔧 使用 OpenAI API（可选）

如果你想使用 GPT 模型生成更智能的建议：

### macOS / Linux
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
./start.sh
```

### Windows
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
start.bat
```

**注意**: 没有 API key 也完全可以使用！系统会自动使用内置的启发式算法。

---

## 🎯 测试示例

### 示例 1: 问题类型
```
朋友: 你明天有空吗？
```
→ 检测到语气: ❓ 疑问

### 示例 2: 积极类型
```
朋友: 谢谢你的帮助，太棒了！
```
→ 检测到语气: 😊 积极

### 示例 3: 消极类型
```
朋友: 今天真是糟糕透了...
```
→ 检测到语气: 😔 消极

### 示例 4: 中性类型
```
朋友: 我在家里。
```
→ 检测到语气: 😐 中性

---

## 📊 偏好学习机制

系统使用简单的**强化学习**算法：

- 初始权重: 每种风格都是 1.0
- 点击"使用 👍": 权重 +1.0
- 点击"不好 👎": 权重 -0.5（最小保持 1.0）
- 权重越高 = 系统认为你越喜欢该风格

**示例流程:**
```
初始: polite=1.0, funny=1.0, straightforward=1.0
↓
使用礼貌风格 → polite=2.0, funny=1.0, straightforward=1.0
↓
不喜欢幽默 → polite=2.0, funny=1.0, straightforward=1.0
↓
使用礼貌风格 → polite=3.0, funny=1.0, straightforward=1.0
```

系统学会了你喜欢礼貌风格！

---

## 🛠️ 手动安装（如果启动脚本不工作）

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务器
uvicorn app:app --reload
```

---

## ❓ 常见问题

**Q: 端口 8000 已被占用怎么办？**
```bash
uvicorn app:app --reload --port 8001
```

**Q: OpenAI API 调用失败？**
- 系统会自动回退到启发式模式
- 检查 API key 是否正确
- 确认网络连接

**Q: 如何重置偏好权重？**
- 重启服务器即可（当前是内存存储）

---

## 📞 技术支持

详细文档请查看: `README.md`

项目结构:
```
chatsensei_lite/
├── app.py              # 后端主程序
├── templates/
│   └── index.html     # 前端页面
├── static/
│   ├── script.js      # JavaScript逻辑
│   └── styles.css     # 样式文件
├── requirements.txt   # Python依赖
├── start.sh          # Mac/Linux启动脚本
└── start.bat         # Windows启动脚本
```

祝使用愉快！🎉

