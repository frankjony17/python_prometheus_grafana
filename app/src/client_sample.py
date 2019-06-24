import prometheus_client
from prometheus_client import Summary, Counter, Histogram, Gauge


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
_INF = float("inf")


def get_dict():
    return {
        'c': Counter('test_of_counter', 'Description of counter'),
        'h': Histogram('test_of_histogram', 'Description of histogram', buckets=(1, 5, 10, 50, 100, 200, 500, _INF)),
        'g': Gauge('test_of_gauge', 'Description of gauge')
    }


graphs = get_dict()


def client_count():
    graphs['c'].inc()
    return requests_count()


def client_update_histogram(request):
    client_print(request)
    k = float(request.args.get('value'))
    graphs['h'].observe(k)
    return requests_count()


def client_update_gauge(request):
    client_print(request)
    k = request.args.get('value')
    graphs['g'].set(k)
    return requests_count()


def requests_count():
    res = []
    for k, v in graphs.iteritems():
        res.append(prometheus_client.generate_latest(v))
    return res


def client_print(request):
    print(request.args)
