# Monitoring

As [we described previously](../chorus-one/monitoring-alerting.md),
at Chorus One we use [Prometheus][prometheus] for monitoring and alerting.
This is the industry-standard monitoring protocol
that is supported by most software we run.

[prometheus]: https://prometheus.io/

## Prometheus

#### Expose Prometheus metrics. {.p1 #expose-prometheus-metrics}

To be able to monitor the node software,
Prometheus needs a target to scrape.
See [the Prometheus documentation][prometheus-instrumenting]
for how to instrument your application.
If your daemon already includes an RPC server,
adding a `/metrics` endpoint there is usually the easiest way to go about it.
Alternatively, a dedicated metrics port works fine too.

While the set of metrics is of course application-specific,
blockchain networks generally have a concept of the _block height_.
Note that unless the block height is for a finalized fork,
block height is generally a [gauge][prometheus-gauge]
and not a [counter][prometheus-counter].

[prometheus-instrumenting]: https://prometheus.io/docs/practices/instrumentation/
[prometheus-gauge]: https://prometheus.io/docs/concepts/metric_types/#gauge
[prometheus-counter]: https://prometheus.io/docs/concepts/metric_types/#counter

#### Expose metrics privately. {.p1 #expose-metrics-privately}

While _we_ want to scape metrics,
we don’t want to expose confidential information to third parties.
It should be possible for the http server that serves the `/metrics` endpoint
to listen on a network interface that is not Internet-exposed.

#### Respect Prometheus metric and label naming standards. {.p3 #respect-prometheus-standards}

Prometheus [has an official standard for naming metrics and labels][prometheus-naming].
Following the standard ensures that metrics are self-explanatory and easy to use,
and that our alerting configuration is consistent and uniform. In particular:

 * Prefix the metric with the name of your application.
 * Metrics should use base units (bytes and seconds, not kilobytes or milliseconds).
 * Metric names should have a suffix explaining the unit,
   in plural (`_seconds`, `_bytes`).
 * Accumulating counters should end in `_total`.

[prometheus-naming]: https://prometheus.io/docs/practices/naming/

<!-- TODO: Finish this section

## Telementry

TODO.
* Have a way to disable.
* We are fine to share on incentivized testnets.
* We do not grant SSH access to our infrastructure, period.

-->
