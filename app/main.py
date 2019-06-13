import random

from flask import Flask, Response, abort
import prometheus_client


CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

app = Flask(__name__)

# Flask routes
index_requests = prometheus_client.Counter("n_requests_index", "Number of requests to the Index / endpoint")
# With Labels
server_requests = prometheus_client.Counter('my_requests_total', 'HTTP Requests', ['status', 'endpoint'])
# Gauge metric, to report instantaneous values
instantaneous_values = prometheus_client.Gauge('track_in_progress', 'Description of gauge')


@app.route("/")
def hello():
    index_requests.inc()
    return "It works! You're visiting /"


@app.route("/labels")
def labels():
    status = [200, 403, 404, 500]
    for i in range(6):
        status.append(200)
    for i in range(3):
        status.append(404)
    code = random.choice(status)
    server_requests.labels(status=code, endpoint="/labels").inc()
    if code == 200:
        return "OK"
    else:
        abort(code)


@app.route('/metrics/')
def metrics():
    gauge(random.randint(0, 7))
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@instantaneous_values.track_inprogress()
def gauge(value):
    if 0 < value < 3:
        instantaneous_values.inc(value)
    elif 3 < value < 6:
        instantaneous_values.dec()
    else:
        instantaneous_values.set(6.2)


if __name__ == '__main__':
    # start_http_server(9888) Note: You would normally use this in a regular python app.
    app.run(debug=True, host="0.0.0.0", port=5000)
