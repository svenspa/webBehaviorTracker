from flask import Flask, jsonify, request
import time
import pandas as pd

app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
prev_url = ""

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime
    global prev_url

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    url_timestamp[parent_url] = int(time.time())
    prev_url = parent_url

    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    pd.DataFrame.from_dict(data=url_viewtime, orient='index').to_csv('dict_file.csv', header=False)
    return jsonify({'message': 'quit success!'}), 200

app.run(host='0.0.0.0', port=5000)
