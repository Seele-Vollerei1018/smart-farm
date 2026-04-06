const QWEN_API_KEY = import.meta.env.VITE_QWEN_API_KEY || ''
const QWEN_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'

/**
 * 发送AI聊天请求
 * @param {string} message - 用户输入的消息
 * @returns {Promise<string>} AI的回复
 */
export async function sendChatMessage(message) {
  if (!message) {
    throw new Error('请输入问题')
  }

  if (!QWEN_API_KEY) {
    throw new Error('API Key 未配置，请检查 .env 文件中的 VITE_QWEN_API_KEY 配置')
  }

  try {
    const response = await fetch(QWEN_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${QWEN_API_KEY}`
      },
      body: JSON.stringify({
        model: 'qwen-plus',
        messages: [
          {
            role: 'system',
            content: '你是一个教导中小学生的农业老师，请简单、通俗易懂地用中文回答以下问题，不要用过于专业的术语。'
          },
          {
            role: 'user',
            content: message
          }
        ],
        temperature: 0.7,
        max_tokens: 1000
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      if (errorData.error && errorData.error.code === 'invalid_api_key') {
        throw new Error('API Key 无效，请检查 .env 文件中的 VITE_QWEN_API_KEY 配置')
      }
      throw new Error(`网络请求失败: ${response.status} - ${errorData.error?.message || '未知错误'}`)
    }

    const data = await response.json()
    if (data.choices && data.choices.length > 0 && data.choices[0].message) {
      return data.choices[0].message.content
    } else {
      throw new Error('获取AI回复失败')
    }
  } catch (err) {
    console.error('AI API调用错误:', err)
    throw new Error(`AI聊天失败: ${err.message}`)
  }
}
