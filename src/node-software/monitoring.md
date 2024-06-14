# Monitoring

As [we described previously](../chorus-one/monitoring-alerting.md),
we use [Prometheus][prometheus] for monitoring and alerting.
This is the industry-standard monitoring protocol
that is supported by most software we run.

Exposing metrics is essential for any blockchain project.
Without it, the node software is a black box to us,
and the only thing we could observe is whether the process is still running,
which is not the same as being healthy.
We need to know what’s going on _inside_ that process,
and the standard way of doing that is through logs and Prometheus metrics.

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
Unless the block height is for a finalized fork,
block height is generally a [gauge][prometheus-gauge]
and not a [counter][prometheus-counter].

[prometheus-instrumenting]: https://prometheus.io/docs/practices/instrumentation/
[prometheus-gauge]: https://prometheus.io/docs/concepts/metric_types/#gauge
[prometheus-counter]: https://prometheus.io/docs/concepts/metric_types/#counter

#### Expose metrics privately. {.p1 #expose-metrics-privately}

We need to scape metrics internally,
but we don’t want to expose confidential information to third parties.
It should be possible for the http server that serves the `/metrics` endpoint
to listen on a network interface that is not Internet-exposed.

#### Ensure that metrics are relevant and named appropriately. {.p1 #metrics-are-relevant}

For new projects, of course you only add metrics that measure something relevant.
For projects that fork existing node software,
we encountered software in the past that kept exposing metrics that were no longer meaningful,
or under the name of the original software.
Similar to how clear but incorrect error messages are worse than vague error messages,
misleading metrics are more harmful than not having metrics at all.
“Maybe the metrics are lying to us”
is far down the list of possible causes when troubleshooting.

#### Respect Prometheus metric and label naming standards. {.p3 #respect-prometheus-standards}

Prometheus [has an official standard for naming metrics and labels][prometheus-naming].
Following the standard ensures that metrics are self-explanatory and easy to use,
and enables us to write alerting configuration that is consistent and uniform.
In particular:

 * Prefix the metric with the name of your application.
 * Metrics should use base units (bytes and seconds, not kilobytes or milliseconds).
 * Metric names should have a suffix explaining the unit,
   in plural (`_seconds`, `_bytes`).
 * Accumulating counters should end in `_total`.

[prometheus-naming]: https://prometheus.io/docs/practices/naming/

#### If you expose system metrics, provide a way to disable them. {.p3 #system-metrics-can-be-disabled}

We already run the [Prometheus node exporter][node-exporter] on our hosts.
Exposing that same information from the node software unnecessarily bloats `/metrics` responses,
which puts strain on our bandwidth and storage,
and collecting the information can make the `/metrics` endpoint slow.

[node-exporter]: https://prometheus.io/docs/guides/node-exporter/

#### Expose the node software version as a metric. {.p3 #version-metric}

For automating rollouts,
but also for monitoring manual rollouts,
and observability and troubleshooting in general,
it is useful for us to have a way of identifying what version is running at runtime.
When you run one instance this is easy to track externally,
but when you run a dozen nodes,
it’s easy to lose track of which versions run where.
Exposing a version metric
(with value `1` and the version as a label)
is one of the most convenient ways to expose version information.

#### Expose the validator identity as a metric. {.p3 #identity-metric}

Similar to having runtime information about the version,
when managing multiple nodes,
it is useful to know which identity (address or pubkey) runs where.
Like the version, a convenient place to expose this is in Prometheus metrics.

<!--
TODO: It should *also* be part of the RPC,
cross-reference that after I write the chapter about RPC interface.
-->

## Health

#### Expose an endpoint for health checks. {.p2 #health-endpoint}

For automating restarts and failover,
and for loadbalancing across RPC nodes,
it is useful to have an endpoint where the node software
reports its own view on whether it is healthy and in sync with the network.
A convenient place to do this is with a `/health` or `/status` http endpoint
on the RPC interface.

Ideally the application should respond on that endpoint
even during the startup phase and report startup progress there.

## Telemetry

We understand that node software authors
need visibility into how their software runs to inform development
— that is the reason we are publishing this network handbook in the first place.
However, we are subject to legal and compliance requirements,
which mean that we cannot always allow software to phone home.
In particular,
in some cases we are under non-disclosure agreements.

On incentivized testnets we are happy to share telemetry data.
In these cases we only operate our own identity,
and the risk of telemetry exposing confidential information is low.
For mainnets we do not allow telemetry data to be shared.

#### Ensure telemetry can be disabled. {.p2 #telemetry-can-be-disabled}
As described above,
some confidential information we cannot share for legal and compliance reasons.
The easiest way to prevent inadvertently exposing confidential information,
is to expose as little information as possible.

## Troubleshooting

In case of bugs that are difficult to reproduce,
we are happy to work with you to share relevant information, logs,
try patches, etc.
**Under no circumstance
does Chorus One grant access to our infrastructure to third parties.**
We definitely do not grant SSH access or other forms of remote access.
If we did,
we would not be able to guarantee the integrity of our infrastructure.
