# agent.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import add_task, delete_task, list_tasks
from utils import extract_first_json_block

# Ortam değişkenlerini yükle
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """
Sen bir görev yöneticisi agentsın. Kullanıcıdan gelen doğal dili yorumla ve SADECE AŞAĞIDAKİ MCP FORMATINDA bir yanıt üret:

{
  "name": "add_task" | "delete_task" | "list_tasks",
  "arguments": {
    "task": "<görev açıklaması>" // sadece add_task ve delete_task için
  }
}

KURALLAR:
- Sadece geçerli JSON döndür.
- Açıklama veya yorum verme.
- list_tasks için "arguments" boş nesne olmalı: {}

ÖRNEK:
{
  "name": "add_task",
  "arguments": {
    "task": "Annemin doğum günü 24.08.1991"
  }
}
"""

TOOL_MAP = {
    "add_task": lambda args: add_task(args["task"]),
    "delete_task": lambda args: delete_task(args["task"]),
    "list_tasks": lambda args: list_tasks()
}

def run_agent(user_input):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    content_raw = response.choices[0].message.content.strip()
    content_clean = extract_first_json_block(content_raw)

    print("🧠 LLM Yanıtı:", content_clean)

    try:
        parsed = json.loads(content_clean)
        tool_name = parsed["name"]
        arguments = parsed.get("arguments", {})

        if tool_name in TOOL_MAP:
            result = TOOL_MAP[tool_name](arguments)
            print(result)
        else:
            print("❌ Bilinmeyen araç:", tool_name)
    except Exception as e:
        print("❌ JSON çözümlenemedi:", e)
