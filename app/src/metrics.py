import prometheus_client

# A Counter tracks counts of events or running totals.
counter_inc = prometheus_client.Counter("counter_total", "A Counter tracks counts of events or running totals")
# Gauge metric, to report instantaneous values.
instantaneous_values = prometheus_client.Gauge('track_in_progress', 'Gauge metric, to report instantaneous values')


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


