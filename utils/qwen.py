from ollama import Client

client = Client(host='http://localhost:11434')
response = client.generate(
    model='qwen2.5:7b',
    prompt='你好'
)
print(response['response'])