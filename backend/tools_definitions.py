import json
import time
from openai import OpenAI
import os


from backend.rag_tool import kb_search
from backend.sum_tools import get_reponse_from_sum
from backend.prompt_modified import SYSTEM_PROMPT
from backend.tool import tools


temperature = 0
model = "Qwen/Qwen2.5-3B-Instruct"
openai_api_key = "hai"
openai_api_base = "http://localhost:8001/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

sys_turn = {
    "role": "system",
    "content": SYSTEM_PROMPT
}

extra_body = {
    "temperature": temperature,
    "max_tokens": 16000,
    "chat_template_kwargs": {"enable_thinking": False}
}


def _format_history_from_frontend(frontend_history: list) -> list:
    
    model_messages = []
    for msg in frontend_history:
        role = "user" if msg.get("isUser") else "assistant"
        content = msg.get("message", "")
        if content: 
            model_messages.append({"role": role, "content": content})
    return model_messages

def _format_history_for_frontend(model_messages: list) -> list:
    
    frontend_history = []
    for msg in model_messages:
       
        if msg['role'] in ['user', 'assistant'] and msg.get("content"):
            frontend_history.append({
                "message": msg["content"],
                "isUser": msg['role'] == 'user'
            })
    return frontend_history


def get_chatbot_response(user_input: str, history: list):
   
    messages = _format_history_from_frontend(history)
    
    if not messages:
        messages.insert(0, sys_turn)

    
    user_message = { "role": "user", "content": user_input }
    messages.append(user_message)

    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        tools=tools,
        tool_choice="auto",
        extra_body=extra_body
    )

    
    if chat_completion.choices[0].message.tool_calls:
        tool_calls = chat_completion.choices[0].message.tool_calls
        assistant_message = {"role": "assistant", "tool_calls": tool_calls}
        
        tool_name = tool_calls[0].function.name
        tool_args = json.loads(tool_calls[0].function.arguments)
        
        tool_output_content = kb_search(tool_name, tool_args)
        response_content = get_reponse_from_sum(user_input, tool_output_content)
        
        tool_response_message = {
            'role': 'tool',
            'name': tool_calls[0].function.name,
            'content': response_content
        }
        final_response_message = {
            'role': 'assistant',
            'content': response_content
        }
        
        messages.extend([assistant_message, tool_response_message, final_response_message])
        final_answer = response_content
    else:
        model_output = chat_completion.choices[0].message.content
        final_response_message = {
            "role": "assistant",
            "content": model_output,
        }
        messages.append(final_response_message)
        final_answer = model_output
    
    
    updated_history_for_frontend = _format_history_for_frontend(messages)
    
    return final_answer, updated_history_for_frontend