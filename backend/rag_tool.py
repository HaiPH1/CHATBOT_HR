from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_community import GoogleSearchAPIWrapper

import json
import os
import re
import requests

def load_and_split_documents(pdf_data_path, chunk_size=1024, chunk_overlap=200):
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    return chunks

def embed_and_save(chunks, vector_db_path, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={'device': 'cpu'},)
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    return db


pdf_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")  
vector_db_path = os.path.join(os.path.dirname(__file__), "vectorstores", "db_faiss")

if __name__ == "__main__":
    # Chỉ chạy build vector khi chạy trực tiếp
    chunks = load_and_split_documents(pdf_data_path)
    db = embed_and_save(chunks, vector_db_path)

import json


def docstojson(docs: list[dict]):
    docs = [dict(title=doc.metadata.get("source", ""), content=doc.page_content) for doc in docs]
    if len(docs) == 0:
        docs = [{'title': '', 'content': 'Em xin lỗi, em không có thông tin về câu hỏi của anh chị.'}]
    return json.dumps({"search_result": docs}, ensure_ascii=False)

def kb_search(tool_name: str, tool_args: dict, topk: int = 10):
    if tool_name == 'knowledge_base_search':
        db_path = os.path.join(os.path.dirname(__file__), "vectorstores", "db_faiss")
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cuda'}, encode_kwargs={'batch_size': 8})
        db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)
    
        query = tool_args.get('query')
        docs = db.similarity_search(query, k=topk)
        return docs
    elif tool_name == 'get_salary_info':
        return _get_salary_from_api(**tool_args)
    elif tool_name == 'get_monthly_leave_info':
        return _get_leave_from_api(**tool_args)
    else:
        return general_search(tool_args.get('query'))


def _get_salary_from_api(month: str, year: str):
    
    employee_id = "NV001"

    
    match_month = re.search(r'^\d+$', str(month))
    match_year = re.search(r'^\d+$', str(year))

    if not match_month or not match_year:
        
        return {"error": "Thông tin không hợp lệ. Vui lòng cung cấp tháng và năm dưới dạng số."}

    final_month = match_month.group()
    final_year = match_year.group()
    
    
    try:
        params = {"employee_id": employee_id, "year": final_year, "month": final_month}
        response = requests.get("http://127.0.0.1:8000/get-salary", params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data or ("error" in data and data["error"]):
             return {"error": f"Không có dữ liệu lương cho tháng {final_month}/{final_year}."}
        return data

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Không tìm thấy dữ liệu lương cho tháng {final_month}/{final_year}."}
        else:
            return {"error": "Hệ thống tra cứu lương đang gặp sự cố. Vui lòng thử lại sau."}
    except requests.exceptions.RequestException:
        return {"error": "Không thể kết nối đến hệ thống tra cứu lương. Vui lòng kiểm tra lại dịch vụ."}

def _get_leave_from_api(month: str, year: str):
    
    employee_id = "NV001"
    
    
    match_month = re.search(r'^\d+$', str(month))
    match_year = re.search(r'^\d+$', str(year))

    if not match_month or not match_year:
        return {"error": "Thông tin không hợp lệ. Vui lòng cung cấp tháng và năm dưới dạng số."}

    final_month = match_month.group()
    final_year = match_year.group()

   
    try:
        params = {"employee_id": employee_id, "year": final_year, "month": final_month}
        response = requests.get("http://127.0.0.1:8000/get-leave", params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data or ("error" in data and data["error"]):
             return {"error": f"Không có dữ liệu ngày nghỉ cho tháng {final_month}/{final_year}."}
        return data

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Không tìm thấy dữ liệu ngày nghỉ cho tháng {final_month}/{final_year}."}
        else:
            return {"error": "Hệ thống tra cứu ngày nghỉ đang gặp sự cố. Vui lòng thử lại sau."}
    except requests.exceptions.RequestException:
        return {"error": "Không thể kết nối đến hệ thống tra cứu ngày nghỉ. Vui lòng kiểm tra lại dịch vụ."}


GG_API_KEY = "nonono"
GG_CSE_ID = "e76ca565784734740"
TOPK = 10
gsearch = GoogleSearchAPIWrapper(
    google_api_key=GG_API_KEY, google_cse_id=GG_CSE_ID, k=TOPK
)
def general_search(query):
    gsearch = GoogleSearchAPIWrapper(
        google_api_key=GG_API_KEY,
        google_cse_id=GG_CSE_ID,
        k=TOPK
    )
    result = {"title": "", "content": gsearch.run(query)}
    return {"search_result": [result]}