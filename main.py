import requests, json, math
from flask import Flask, render_template, request, redirect
from palworldApi import palworldHtml, save, metrics, players, announce
from ollamaChatBot import ollamaHtml, Generate, Chat

app = Flask(__name__)




#@app.route('/')

@app.route('/ollama/')
def ollamaIndexHtml():
    return ollamaHtml()
@app.route('/ollama/generate', methods=['POST'])
def ollamaGenerate():
    return Generate()
@app.route('/ollama/chat', methods=['POST'])
def ollamaChat():
    return Chat()


@app.route('/palworld/')
def palworldIndexHtml():
    return palworldHtml()

@app.route('/palworld/announce', methods=['POST'])
def palworldAnnounce():
    return announce()

@app.route('/palworld/save')
def palworldSave():
    return save()

@app.route('/palworld/players')
def palworldPlayers():
    return players()

@app.route('/palworld/metrics')
def palworldMetrics():
    return metrics()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8213, debug=True)
