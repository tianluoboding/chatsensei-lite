/**
 * ChatSensei Lite - 前端逻辑
 * 处理用户交互、API 调用和 UI 更新
 */

// DOM 元素引用
let chatTextarea;
let analyzeBtn;
let resultsSection;
let toneDisplay;
let suggestionsContainer;
let errorMessage;

// 风格标签映射
const styleLabels = {
    polite: "礼貌风格",
    funny: "幽默风格",
    straightforward: "直接风格"
};

const styleEmojis = {
    polite: "🎩",
    funny: "😄",
    straightforward: "💬"
};

const toneLabels = {
    question: "❓ 疑问",
    positive: "😊 积极",
    negative: "😔 消极",
    neutral: "😐 中性"
};

/**
 * 初始化应用
 */
document.addEventListener('DOMContentLoaded', () => {
    // 获取 DOM 元素
    chatTextarea = document.getElementById('chat');
    analyzeBtn = document.getElementById('analyzeBtn');
    resultsSection = document.getElementById('resultsSection');
    toneDisplay = document.getElementById('toneDisplay');
    suggestionsContainer = document.getElementById('suggestionsContainer');
    errorMessage = document.getElementById('errorMessage');

    // 绑定事件
    analyzeBtn.addEventListener('click', handleAnalyze);
});

/**
 * 处理"分析 & 生成建议"按钮点击
 */
async function handleAnalyze() {
    const chatContent = chatTextarea.value.trim();

    // 验证输入
    if (!chatContent) {
        showError('请先输入聊天内容！');
        return;
    }

    // 隐藏错误消息
    hideError();

    // 设置加载状态
    setLoading(true);

    try {
        // 调用 /suggest API
        const response = await fetch('/suggest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ chat: chatContent })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '请求失败');
        }

        const data = await response.json();

        // 显示结果
        displayResults(data);

    } catch (error) {
        showError(`错误: ${error.message}`);
    } finally {
        setLoading(false);
    }
}

/**
 * 显示分析结果
 */
function displayResults(data) {
    // 显示语气
    toneDisplay.textContent = `检测语气: ${toneLabels[data.tone] || data.tone}`;
    toneDisplay.className = `tone-badge tone-${data.tone}`;

    // 清空之前的建议
    suggestionsContainer.innerHTML = '';

    // 创建建议卡片
    const styles = ['polite', 'funny', 'straightforward'];
    styles.forEach(style => {
        const card = createSuggestionCard(style, data.suggestions[style]);
        suggestionsContainer.appendChild(card);
    });

    // 更新偏好显示
    updatePreferences(data.preferences);

    // 显示结果区域
    resultsSection.style.display = 'block';

    // 平滑滚动到结果
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * 创建建议卡片
 */
function createSuggestionCard(style, suggestion) {
    const card = document.createElement('article');
    card.className = 'suggestion-card';

    const header = document.createElement('header');
    header.innerHTML = `<strong>${styleEmojis[style]} ${styleLabels[style]}</strong>`;

    const content = document.createElement('p');
    content.textContent = suggestion;
    content.className = 'suggestion-text';

    const footer = document.createElement('footer');
    footer.className = 'suggestion-actions';

    // "使用" 按钮
    const useBtn = document.createElement('button');
    useBtn.textContent = '使用 👍';
    useBtn.className = 'use-btn';
    useBtn.onclick = () => handleFeedback(style, true, card);

    // "不好" 按钮
    const badBtn = document.createElement('button');
    badBtn.textContent = '不好 👎';
    badBtn.className = 'bad-btn outline';
    badBtn.onclick = () => handleFeedback(style, false, card);

    footer.appendChild(useBtn);
    footer.appendChild(badBtn);

    card.appendChild(header);
    card.appendChild(content);
    card.appendChild(footer);

    return card;
}

/**
 * 处理用户反馈
 */
async function handleFeedback(chosenStyle, isGood, cardElement) {
    // 禁用该卡片的按钮
    const buttons = cardElement.querySelectorAll('button');
    buttons.forEach(btn => btn.disabled = true);

    try {
        // 调用 /feedback API
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chosen_style: chosenStyle,
                good: isGood
            })
        });

        if (!response.ok) {
            throw new Error('反馈提交失败');
        }

        const data = await response.json();

        // 更新偏好显示
        updatePreferences(data.preferences);

        // 视觉反馈
        cardElement.classList.add(isGood ? 'feedback-good' : 'feedback-bad');

        // 显示反馈消息
        const feedbackMsg = document.createElement('small');
        feedbackMsg.textContent = isGood ? '✓ 已记录你的偏好' : '✓ 已记录反馈';
        feedbackMsg.className = 'feedback-message';
        cardElement.querySelector('footer').appendChild(feedbackMsg);

    } catch (error) {
        showError(`反馈提交失败: ${error.message}`);
        // 重新启用按钮
        buttons.forEach(btn => btn.disabled = false);
    }
}

/**
 * 更新偏好权重显示
 */
function updatePreferences(preferences) {
    document.getElementById('polite-weight').textContent = preferences.polite.toFixed(1);
    document.getElementById('funny-weight').textContent = preferences.funny.toFixed(1);
    document.getElementById('straightforward-weight').textContent = preferences.straightforward.toFixed(1);
}

/**
 * 设置加载状态
 */
function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    analyzeBtn.textContent = isLoading ? '⏳ 分析中...' : '🔍 分析 & 生成建议';
    analyzeBtn.setAttribute('aria-busy', isLoading);
}

/**
 * 显示错误消息
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * 隐藏错误消息
 */
function hideError() {
    errorMessage.style.display = 'none';
}

