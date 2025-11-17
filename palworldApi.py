import requests, json, math
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

url = "http://192.168.86.128:8212/v1/api"


@app.route('/palworld/')
def palworldHtml():
    return render_template('palworld.html')

@app.route('/palworld/announce', methods=['POST'])
def announce():
    msg = request.form['msg'] # 'navn' = name på inputen i HTML
    print(msg)
    headers = {
        'Content-Type': 'application/json',
        'authorization': 'Basic YWRtaW46Ynl0ZXMxMjM='
    }
    payload = json.dumps({
      "message": msg
    })
    response = requests.request("POST", f'{url}/announce', headers=headers, data=payload)
    return redirect('/')

@app.route('/palworld/save', methods=['POST'])
def save():
    payload={}
    headers = {
        'Accept': 'application/json',
        'authorization': 'Basic YWRtaW46Ynl0ZXMxMjM='
    }
    response = requests.request("POST", f'{url}/save', headers=headers, data=payload)
    return redirect('/')

@app.route('/palworld/metrics', methods=['GET'])
def metrics():
    payload={}
    headers = {
        'Accept': 'application/json',
        'authorization': 'Basic YWRtaW46Ynl0ZXMxMjM='
    }
    response = requests.request("GET", f'{url}/metrics', headers=headers, data=payload)
    res = json.loads(response.text)
    #print(res)
    uptime = res["uptime"]
    seconds = uptime%60
    minutes = math.floor((uptime)/60)%60
    hours = math.floor((uptime)/3600)%24
    days = math.floor(uptime/(60*60*24))
    #print(seconds, minutes, hours, days)
    #print(f'server uptime: {days}d {hours}h {minutes}m {seconds}s')
    betterUpTime = f'server uptime: {days}d {hours}h {minutes}m {seconds}s'
    return json.dumps({
        "uptime": betterUpTime,
        "players": res["currentplayernum"],
        "maxPlayers": res["maxplayernum"],
        "serverFps": res["serverfps"],
        "serverFrameTime": '{0:.2f}'.format(res["serverframetime"]),
        "ingameDays": res["days"],
    })
    
@app.route('/palworld/players', methods=['GET'])
def players():
    payload={}
    headers = {
        'Accept': 'application/json',
        'authorization': 'Basic YWRtaW46Ynl0ZXMxMjM='
    }
    response = requests.request("GET", f'{url}/players', headers=headers, data=payload)
    #print(response.text)
    print(response.status_code)
    basicPlayers = []
    for i in json.loads(response.text)["players"]:
        temp = {
            "name": i["name"],
            "accountName": i["accountName"],
            "ping": i["ping"],
            "level": i["level"],
            "x": i["location_x"],
            "y": i["location_y"],
        }
        basicPlayers.append(temp)
    return json.dumps(basicPlayers)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8214, debug=True)

