"""
ChatSensei Lite - 消息助手原型
FastAPI 后端应用
"""
import os
import random
from typing import Dict, Literal
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# 尝试导入 OpenAI（如果可用）
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# 初始化 FastAPI 应用
app = FastAPI(title="ChatSensei Lite")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="templates")

# 全局状态：风格偏好权重（简单的上下文赌博机）
style_preferences: Dict[str, float] = {
    "polite": 1.0,
    "funny": 1.0,
    "straightforward": 1.0
}

# 关键词集合用于语气检测（支持中英文）
POSITIVE_KEYWORDS = {
    # 英文
    "thanks", "thank", "great", "awesome", "love", "good", "happy", "excellent", "wonderful",
    # 中文
    "谢谢", "感谢", "太好了", "很好", "不错", "棒", "开心", "高兴", "喜欢", "爱"
}
NEGATIVE_KEYWORDS = {
    # 英文
    "hate", "bad", "terrible", "sad", "angry", "upset", "sorry", "annoying", "frustrating",
    # 中文
    "讨厌", "糟糕", "不好", "难过", "生气", "愤怒", "烦", "抱歉", "遗憾", "失望"
}


# ============ Pydantic 模型 ============

class SuggestRequest(BaseModel):
    chat: str


class FeedbackRequest(BaseModel):
    chosen_style: Literal["polite", "funny", "straightforward"]
    good: bool


# ============ 辅助函数 ============

def detect_tone(context: str) -> str:
    """
    检测聊天上下文的语气
    
    返回值：
    - "question": 如果消息以 ? 结尾
    - "positive": 如果包含正面关键词
    - "negative": 如果包含负面关键词
    - "neutral": 默认情况
    """
    context_lower = context.lower().strip()
    
    # 检查是否是问题
    if context_lower.endswith("?") or context_lower.endswith("？"):
        return "question"
    
    # 检查正面关键词
    for keyword in POSITIVE_KEYWORDS:
        if keyword in context_lower:
            return "positive"
    
    # 检查负面关键词
    for keyword in NEGATIVE_KEYWORDS:
        if keyword in context_lower:
            return "negative"
    
    return "neutral"


async def generate_suggestions(context: str) -> Dict[str, str]:
    """
    生成三种风格的回复建议
    
    如果设置了 OPENAI_API_KEY，使用 OpenAI API
    否则使用启发式方法
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key and OPENAI_AVAILABLE:
        return await generate_suggestions_openai(context, api_key)
    else:
        return generate_suggestions_heuristic(context)


async def generate_suggestions_openai(context: str, api_key: str) -> Dict[str, str]:
    """
    使用 OpenAI API 生成建议
    """
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""你是一个消息助手。用户刚收到以下聊天消息：

{context}

请生成三种不同风格的简短回复建议（每个不超过50字）：
1. 礼貌风格（polite）：正式、尊重、得体
2. 幽默风格（funny）：轻松、有趣、可能带emoji
3. 直接风格（straightforward）：简洁、清晰、直截了当

请以JSON格式返回，格式如下：
{{"polite": "...", "funny": "...", "straightforward": "..."}}
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个有帮助的消息助手，能生成不同风格的回复建议。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        # 解析响应
        content = response.choices[0].message.content.strip()
        
        # 尝试提取 JSON
        import json
        # 移除可能的 markdown 代码块标记
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        suggestions = json.loads(content)
        
        # 验证返回了所有三种风格
        if all(style in suggestions for style in ["polite", "funny", "straightforward"]):
            return suggestions
        else:
            # 如果格式不对，回退到启发式方法
            return generate_suggestions_heuristic(context)
            
    except Exception as e:
        print(f"OpenAI API 调用失败: {e}")
        # 回退到启发式方法
        return generate_suggestions_heuristic(context)


def generate_suggestions_heuristic(context: str) -> Dict[str, str]:
    """
    使用启发式方法生成建议（不依赖外部 API）
    """
    tone = detect_tone(context)
    
    # 根据语气选择基础回复
    base_responses = {
        "question": "让我想想，稍后回复你。",
        "positive": "我也很高兴听到这个！",
        "negative": "我很遗憾听到这个。",
        "neutral": "我明白了。"
    }
    
    base = base_responses.get(tone, "收到。")
    
    # 为不同风格添加包装
    suggestions = {
        "polite": f"感谢你的分享！{base}",
        "funny": f"哈哈，{base} 😂",
        "straightforward": base
    }
    
    return suggestions


def update_preferences(chosen_style: str, reward: float) -> None:
    """
    更新风格偏好权重
    
    Args:
        chosen_style: 被选择的风格
        reward: 奖励值（正值增加权重，负值减少权重）
    """
    if chosen_style in style_preferences:
        style_preferences[chosen_style] += reward
        # 确保最小值为 1.0
        style_preferences[chosen_style] = max(1.0, style_preferences[chosen_style])


def weighted_style_choice() -> str:
    """
    根据当前权重随机选择一种风格
    （备用函数，可用于未来的自动推荐）
    """
    styles = list(style_preferences.keys())
    weights = list(style_preferences.values())
    return random.choices(styles, weights=weights, k=1)[0]


# ============ API 端点 ============

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    渲染主页
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/suggest")
async def suggest(request: SuggestRequest):
    """
    分析聊天内容并生成回复建议
    
    返回：
    - tone: 检测到的语气
    - suggestions: 三种风格的建议
    - preferences: 当前偏好权重
    """
    # 验证输入
    if not request.chat or not request.chat.strip():
        raise HTTPException(status_code=400, detail="聊天内容不能为空")
    
    # 检测语气
    tone = detect_tone(request.chat)
    
    # 生成建议
    suggestions = await generate_suggestions(request.chat)
    
    return {
        "tone": tone,
        "suggestions": suggestions,
        "preferences": style_preferences
    }


@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    """
    处理用户反馈并更新偏好
    
    Args:
        chosen_style: 用户选择的风格
        good: True 表示喜欢，False 表示不喜欢
    
    返回：
    - preferences: 更新后的偏好权重
    """
    # 根据反馈更新权重
    if request.good:
        update_preferences(request.chosen_style, reward=1.0)
    else:
        update_preferences(request.chosen_style, reward=-0.5)
    
    return {
        "preferences": style_preferences
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

