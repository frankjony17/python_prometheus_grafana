from flask import Flask, Response, abort, request
import prometheus_client
import random

from metrics import counter, gauge, index_requests, server_requests
from client_sample import client_count, client_update_histogram, client_update_gauge

app = Flask(__name__)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


@app.route("/")
def start_server():
    index_requests()
    return "It works! You're visiting /"


@app.route("/labels")
def labels():
    status = [200, 403, 404, 500]
    code = server_requests(status)
    if code == 200:
        return "OK"
    else:
        abort(code)


@app.route("/update/count", methods=["GET"])
def update_count():
    res = client_count()
    return Response(res, mimetype="text/plain")


@app.route("/update/histogram", methods=["GET"])
def update_histogram():
    res = client_update_histogram(request)
    return Response(res, mimetype="text/plain")


@app.route("/update/gauge", methods=["GET"])
def update_gauge():
    res = client_update_gauge(request)
    return Response(res, mimetype="text/plain")


@app.route('/metrics/')
def metrics():
    gauge(random.randint(0, 7))
    counter(random.randint(0, 10))
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
