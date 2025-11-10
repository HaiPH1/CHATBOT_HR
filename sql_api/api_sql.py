from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

def query_db(query, params=()):
    
    import os
    db_path = os.path.join(os.path.dirname(__file__), "hr.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/get-salary")
def get_salary(employee_id: str, year: str, month: str):
    query = """
        SELECT month, base_salary, bonus, net_salary
        FROM salary
        WHERE employee_id = ? AND year = ? AND month = ?
    """
    result = query_db(query, (employee_id, year, month))
    if not result:
        return {"error": "No data found"}
    data = result[0]
    return {
        "employee_id": employee_id,
        "year": year,
        "month": data[0],
        "base_salary": data[1],
        "bonus": data[2],
        "net_salary": data[3]
    }

@app.get("/get-leave")
def get_leave(employee_id: str, year: str, month: str):
    query = """
        SELECT month, days_off, remaining_leave
        FROM leave_data
        WHERE employee_id = ? AND year = ? AND month = ?
    """
    result = query_db(query, (employee_id, year, month))
    if not result:
        return {"error": "No data found"}
    data = result[0]
    return {
        "employee_id": employee_id,
        "year": year,
        "month": data[0],
        "days_off": data[1],
        "remaining_leave": data[2]
    }
@app.get("/")
def root():
    return {"message": " HR API is running!"}

