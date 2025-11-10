
apt update
apt install python3-venv -y


python3 -m venv vllm-env
source vllm-env/bin/activate


pip install --upgrade pip
pip install "vllm[triton]"   

python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-3B-Instruct \
  --port 8001 \
  --max-model-len 20000 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes \
  --gpu-memory-utilization 0.75 \
  --api-key hai
  