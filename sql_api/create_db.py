import sqlite3

conn = sqlite3.connect("hr.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS leave_data;

CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT,
    position TEXT,
    department TEXT
);

CREATE TABLE salary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    year TEXT,
    month TEXT,
    base_salary INTEGER,
    bonus INTEGER,
    net_salary INTEGER
);

CREATE TABLE leave_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    year TEXT,
    month TEXT,
    days_off INTEGER,
    remaining_leave INTEGER
);

INSERT INTO employees VALUES ('NV001', 'Nguyễn Văn A', 'Nhân viên Kinh doanh', 'Sales');
INSERT INTO employees VALUES ('NV002', 'Trần Thị B', 'Kế toán', 'Finance');

INSERT INTO salary (employee_id, year, month, base_salary, bonus, net_salary)
VALUES
('NV001', '2025', '9', 50000000, 5000000, 52500000),
('NV001', '2025', '10', 50000000, 7000000, 54500000),
('NV002', '2025', '10', 60000000, 0, 58000000);

INSERT INTO leave_data (employee_id, year, month, days_off, remaining_leave)
VALUES
('NV001', '2025', '9', 1, 11),
('NV001', '2025', '10', 2, 10),
('NV002', '2025', '10', 0, 12);
""")

conn.commit()
conn.close()
print("Database created successfully!")
