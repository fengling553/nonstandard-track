/**
 * AI教育顾问 - Coze Chat SDK 集成
 * 
 * 使用步骤：
 * 1. 在 coze.cn 创建"AI教育顾问"智能体（参考 ai-advisor-prompt.md）
 * 2. 发布智能体，选择"Chat SDK"渠道
 * 3. 复制安装代码中的 bot_id 和 token，填入下方配置
 * 4. 网站自动启用聊天功能
 */

(function() {
  // ============ 配置区（必填）============
  const BOT_ID = 'YOUR_BOT_ID';        // 替换为你的智能体ID
  const AUTH_TOKEN = 'YOUR_TOKEN';      // 替换为Chat SDK发布时获取的token
  // =====================================

  // 未配置时显示"即将上线"提示
  if (BOT_ID === 'YOUR_BOT_ID' || !BOT_ID) {
    console.log('[AI教育顾问] 未配置bot_id，显示占位按钮');
    var fab = document.querySelector('.ai-fab');
    var tooltip = document.querySelector('.ai-fab-tooltip');
    if (fab && tooltip) {
      // 保留原有浮动按钮和tooltip
      fab.addEventListener('click', function() {
        tooltip.classList.toggle('show');
        setTimeout(function() { tooltip.classList.remove('show'); }, 3000);
      });
    }
    return;
  }

  // 已配置：隐藏原有浮动按钮，启用Coze Chat SDK
  var fab = document.querySelector('.ai-fab');
  var tooltip = document.querySelector('.ai-fab-tooltip');
  if (fab) fab.style.display = 'none';
  if (tooltip) tooltip.style.display = 'none';

  // 动态加载Coze Chat SDK
  var script = document.createElement('script');
  script.src = 'https://lf-cdn.coze.cn/obj/unpkg/flow-platform/chat-app-sdk/latest/libs/cn/index.js';
  script.onload = function() {
    new CozeWebSDK.WebChatClient({
      config: {
        type: 'bot',
        bot_id: BOT_ID,
      },
      auth: {
        type: 'token',
        token: AUTH_TOKEN,
        onRefreshToken: async function() { return AUTH_TOKEN; },
      },
      componentProps: {
        title: 'AI教育顾问',
      },
    });
    console.log('[AI教育顾问] Chat SDK 已启动');
  };
  script.onerror = function() {
    console.error('[AI教育顾问] SDK加载失败');
    // 回退：显示原有按钮
    if (fab) fab.style.display = '';
    if (tooltip) {
      tooltip.style.display = '';
      tooltip.innerHTML = '<strong>AI教育顾问</strong><br>服务暂时不可用，请稍后再试。';
    }
  };
  document.body.appendChild(script);
})();
