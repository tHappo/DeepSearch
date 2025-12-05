from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import json

app = Flask(__name__)


@app.route("/")
def serve_frontend():
    return send_from_directory(os.getcwd(), "index.html")


def deepsearch_call(user_msg: str,
                    model: str = "jina-deepsearch-v1",
                    reasoning_effort: str = "medium",
                    search_provider: str = "arxiv",
                    api_key: str = "Key"):

    url = "https://deepsearch.jina.ai/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "Hi, how can I help you?"},
            {"role": "user", "content": user_msg}
        ],
        "reasoning_effort": reasoning_effort,
        "search_provider": search_provider,
        "stream": False    # 关闭流式输出
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()

    obj = res.json()
    return obj["choices"][0]["message"]["content"]

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("question", "")
    reply = deepsearch_call(user_input)
    return jsonify({"answer": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
