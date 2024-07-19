import ollama

from qBot.plugins import config


async def ai_chat(msg: str):
    client = ollama.AsyncClient(host=config.MODEL_URL)
    message = ""
    messages = [
        {
            'role': 'user',
            'content': msg,
        },
    ]
    async for response in await client.chat(model=config.MODEL_NAME, messages=messages, stream=True):
        if response['done']:  # 如果响应表示聊天结束
            return message
        message = message + response['message']['content']  # 获取响应消息
        pass
