import random
import prometheus_client

# A Counter tracks counts of events or running totals.
counter_inc = prometheus_client.Counter("counter_total", "A Counter tracks counts of events or running totals")
# Gauge metric, to report instantaneous values.
instantaneous_values = prometheus_client.Gauge('track_in_progress', 'Gauge metric, to report instantaneous values')
# Flask routes
index_requests = prometheus_client.Counter("total_requests_index", "Number of requests to the Index / endpoint")
# With Labels
server_requests = prometheus_client.Counter('my_requests_total', 'HTTP Requests', ['status', 'endpoint'])


def index_requests():
    index_requests.inc()


def server_requests(status):
    for i in range(6):
        status.append(200)
    for i in range(3):
        status.append(404)
    code = random.choice(status)
    server_requests.labels(status=code, endpoint="/labels").inc()
    return code


@counter_inc.count_exceptions()
def counter(value):
    counter_inc.inc(value)


@instantaneous_values.track_inprogress()
def gauge(value):
    if 0 < value < 3:
        instantaneous_values.inc(value)
    elif 3 < value < 6:
        instantaneous_values.dec()
    else:
        instantaneous_values.set(6.2)
