tools = [
    {
        "type": "function",
        "function": {
            "name": "knowledge_base_search",
            "description": "Sử dụng công cụ này để tìm kiếm các kiến thức, định nghĩa, khái niệm chuyên sâu liên quan đến các môn học, lĩnh vực chuyên ngành cụ thể từ kho kiến thức cho trước.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Câu hỏi, yêu cầu hoặc lệnh của người dùng. Hãy mô tả càng cụ thể càng tốt để có được kết quả chính xác nhất.",
                    },
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "general_web_search",
            "description": "Sử dụng công cụ này để tìm kiếm các thông tin chung, tin tức, sự kiện hoặc bất kỳ chủ đề nào không thuộc kiến thức chuyên ngành.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Câu hỏi, yêu cầu hoặc lệnh của người dùng. Hãy mô tả càng cụ thể càng tốt để có được kết quả chính xác nhất.",
                    },
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_monthly_leave_info",
            
            "description": "Sử dụng công cụ này để tra cứu số ngày nghỉ của nhân viên cho một tháng và năm cụ thể.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {
                        "type": "string",
                        
                        "description": "Tháng cần tra cứu dưới dạng số (ví dụ: '1', '12').",
                    },
                    "year": {
                        "type": "string",
                        
                        "description": "Năm cần tra cứu dưới dạng số (ví dụ: '2024').",
                    },
                },
                
                "required": ["month", "year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_salary_info",
            
            "description": "Sử dụng công cụ này để tra cứu thông tin lương chi tiết của nhân viên cho một tháng và năm cụ thể.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {
                        "type": "string",
                        
                        "description": "Tháng cần tra cứu dưới dạng số (ví dụ: '1', '12').",
                    },
                    "year": {
                        "type": "string",
                        
                        "description": "Năm cần tra cứu dưới dạng số (ví dụ: '2024').",
                    },
                },
                
                "required": ["month", "year"]
            }
        }
    }
]