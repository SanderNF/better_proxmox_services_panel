import time, re, sys, json, requests, argparse
from flask import Flask, render_template, request, redirect, Response, stream_with_context

app = Flask(__name__)

url = "http://192.168.86.114:11434/api"

class responseInfo:
    returned_data= {}
    model: str = ""
    created_At: str = ""
    response: str = ""
    done: bool = False
    done_Reason: str = ""
    total_Duration: int = 0
    load_Duration: int = 0
    prompt_Eval_Count: int = 0
    prompt_Eval_Duration: int = 0
    eval_Count: int = 0
    eval_Duration: int = 0
    context: object = []


def extract_text(obj):
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        for k in ("content", "text", "message", "response"):
            if k in obj and isinstance(obj[k], (str,)):
                return obj[k]
        
        s = ""
        for v in obj.values():
            s += extract_text(v)
        return s
    if isinstance(obj, list):
        return "".join(extract_text(v) for v in obj)
    return ""

def count_words_and_tokens(text):
    words = re.findall(r"\b\w+\b", text)

    tokens = re.findall(r"\S+", text)
    return len(words), len(tokens)

def saveOnDone(data):
    if data["done"]:
        print("streaming is done")
        #print(data)
        responseInfo.returned_data = data
        for key, value in data.items():
            if hasattr(responseInfo, key):
                setattr(responseInfo, key, value)
    else:
        #print("still streaming")
        return



@app.route('/ollama/')
def ollamaHtml():
    return render_template('ollama.html')

@app.route('/ollama/generate', methods=['POST'])
def Generate(callback=None):
    data = request.data
    payload = json.loads(data)
    print(data)
    try:
        resp = requests.post(f'{url}/generate', json=payload, stream=True, timeout=60)
    except Exception as e:
        print(f'HTTP request faild: {e}')
        #return None
    return Response(resp.iter_content(chunk_size=10*1024),
        content_type=resp.headers['Content-Type'])

    
@app.route('/ollama/chat', methods=['POST'])
def Chat():
    data = request.data
    payload = json.loads(data)
    print(data)
    try:
        resp = requests.post(f'{url}/chat', json=payload, stream=True, timeout=60)
    except Exception as e:
        print(f'HTTP request faild: {e}')
        #return None
    return Response(resp.iter_content(chunk_size=10*1024),
        content_type=resp.headers['Content-Type'])




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8213, debug=True)



