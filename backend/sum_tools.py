import json
import time
from openai import OpenAI
import os
import base64
from backend.rag_tool import kb_search  
from backend.prompt_modified import SYSTEM_SUM_PROMPT

temperature = 0
model = "Qwen/Qwen2.5-3B-Instruct"
openai_api_key = "hai"
openai_api_base = "http://localhost:8001/v1"

client_sum = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

extra_body = {
    "temperature": temperature,
    "frequency_penalty": 0.5,
    "chat_template_kwargs": {"enable_thinking": False}
}

def get_reponse_from_sum(query, tool_output):
    """
    Hàm này nhận kết quả từ tool (có thể là list[Document] hoặc dict),
    chuyển nó thành một chuỗi ngữ cảnh, và tạo ra câu trả lời cho người dùng.
    
    :param query: Câu hỏi gốc của người dùng.
    :param tool_output: Kết quả trả về từ hàm kb_search.
    """
    context_str = ""

    
    
    if isinstance(tool_output, list):
        
        contents = []
        for doc in tool_output:
            
            content = getattr(doc, 'page_content', None)
            if content:
                contents.append(str(content))
        context_str = "\n\n---\n\n".join(contents)

    elif isinstance(tool_output, dict):
       
        context_str = json.dumps(tool_output, ensure_ascii=False, indent=2)

    else:
        
        context_str = str(tool_output)

    
    if not context_str.strip():
        context_str = "Không tìm thấy thông tin liên quan."
    
    
    messages = [
        {
            "role": "system",
            "content":  SYSTEM_SUM_PROMPT % context_str
        }
    ]
    
    user_message = {
        "role": "user",
        "content": query,
    }
    messages.append(user_message)
    
    chat_completion = client_sum.chat.completions.create(
        messages=messages,
        model=model,
        extra_body=extra_body
    )
    
    model_output = chat_completion.choices[0].message.content
    return model_output