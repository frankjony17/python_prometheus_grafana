# python_prometheus_grafana
Python Prometheus e Grafana

## Docker-compose
A fully working example of a basic stack for testing. This compose contains a grafana container, a prometheus container and a really simple and useless flask app that will increment some counters every time we hit an endpoint.

## prometheus folder
Here we just define a basic configuration for the Prometheus in order to get metrics from our app.

## app folder
Disclaimer: in a real world application, it is much better to handle all of this metrics logic at a higher level in the request process. For example, creating our own middleware, so we don't have to repeat code on every endpoint.

## test_app
An app that we can run and tries to simulate random requests with different response status code in order to see some data in our grafana panels.

