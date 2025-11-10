from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Đảm bảo bạn đã import dòng này
from pydantic import BaseModel
import sys
import os
import traceback

# Thêm thư mục gốc vào path để có thể import các module từ backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo rằng file `backend/tools_definitions.py` tồn tại
# và chứa hàm `get_chatbot_response`
try:
    from backend.tools_definitions import get_chatbot_response 
except ImportError:
    print("LỖI: Không thể import 'get_chatbot_response' từ 'backend.tools_definitions'.")
    print("Vui lòng kiểm tra lại tên file và tên hàm.")
    sys.exit(1)

app = FastAPI(title="HR Chatbot API", version="1.0.0")

# ---- SỬA LỖI Ở ĐÂY ----
# Thay thế "..." bằng đoạn code khởi tạo middleware hoàn chỉnh.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn gốc (thay đổi thành domain của bạn trong thực tế)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, etc.)
    allow_headers=["*"],  # Cho phép tất cả các header
)
# -------------------------

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

class ChatResponse(BaseModel):
    response: str
    conversation_history: list

@app.get("/")
def root():
    return {"message": "HR Chatbot API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        print(f"Received history with {len(request.conversation_history)} messages.")

        # Gọi hàm logic chính, truyền vào cả message và history
        final_answer, updated_history = get_chatbot_response(
            user_input=request.message,
            history=request.conversation_history
        )
        
        # Trả về cả câu trả lời và lịch sử đã cập nhật
        return ChatResponse(
            response=final_answer,
            conversation_history=updated_history
        )
    except Exception as e:
        # In lỗi chi tiết ra console của server để dễ dàng debug
        print("Đã có lỗi xảy ra trong endpoint /chat:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Khởi động HR Chatbot API server tại http://0.0.0.0:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)