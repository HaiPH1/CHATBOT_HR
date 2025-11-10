#!/bin/bash

echo "===================================="
echo "Starting HR Chatbot System"
echo "===================================="
echo ""

echo "[1/3] Initializing database..."
cd sql_api
python3 create_db.py
cd ..

echo ""
echo "[2/3] Starting SQL API server..."
cd sql_api
uvicorn api_sql:app --reload --port 8000 &
SQL_PID=$!
cd ..

sleep 3

echo ""
echo "[3/3] Starting Main Chatbot API..."
cd api
uvicorn api_server:app --reload --port 8080 &
API_PID=$!
cd ..

echo ""
echo "===================================="
echo "All services started!"
echo "===================================="
echo ""
echo "SQL API: http://localhost:8000"
echo "Chatbot API: http://localhost:8080"
echo ""
echo "Note: VLLM server needs to be started manually"
echo "Run this command in a new terminal:"
echo ""
echo "python -m vllm.entrypoints.openai.api_server --model phamhai/Llama-3.2-3B-Instruct-Frog --port 8001 --max-model-len 20000 --enable-auto-tool-choice --tool-call-parser llama3_json --api-key hai"
echo ""
echo "Then open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt signal
trap "kill $SQL_PID $API_PID; exit" INT
wait

