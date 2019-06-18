from flask import Flask, Response
import prometheus_client
import random
from metrics import counter, gauge

app = Flask(__name__)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


@app.route('/metrics/')
def metrics():
    gauge(random.randint(0, 7))
    counter(random.randint(0, 10))

    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
