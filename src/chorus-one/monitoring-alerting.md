# Monitoring and alerting

We employ multiple forms of monitoring
to confirm that our nodes are operating as expected
both on short and longer timescales.

### Prometheus

For monitoring we use the industry-standard [Prometheus][prometheus],
combined with its built-in [Alertmanager][alertmanager] for alerting.
For example,
most chains expose a block height metric
that should go up as new blocks get added to the chain.
When this metric stops going up,
either there is a problem with our node,
or the network itself is halted.
Both are reasons for concern,
so this is something we alert on.
Alerts that need immediate attention get routed to [our 24/7 oncall rotation](oncall.md).

[prometheus]: https://prometheus.io/
[alertmanager]: https://prometheus.io/docs/alerting/latest/alertmanager/

### Local and global views

Prometheus metrics exported by a node tell us what _that node’s_ view of the chain is.
They give us a local view,
which might not match what the chain is doing globally.
For example,
when node software is running on an under-powered machine,
it might not be able to process blocks as fast as the network can add them.
Its view of the chain gets increasingly stale.
Yet, it is still progressing, so the block height metric continues to go up,
and our “block height stopped going up” alert would not catch that.
We use several techniques to still catch this:

 * **Rely on built-in gossip-based metrics.**
   Often the node software differentiates between “syncing” and “in sync”.
   It can do that by comparing its own block height
   against the highest known block height in the p2p gossip network.
   Often this highest block is also exposed as a metric.

 * **Compare across nodes.**
   [We generally run multiple nodes for redundancy](reliable-systems.md).
   One additional benefit of this
   is that we can compare the block height across all our nodes,
   and identify when one falls out of sync.

 * **Use external sources.**
   In some cases we can directly or indirectly obtain others’ view of the chain,
   and leverage this to make our own monitoring more robust.
   For example, through our Wormhole node
   we can learn other guardians’ block height on many networks.

### Log-based metrics

We generally do not work with log-based metrics.
In cases where Prometheus metrics are not natively available,
we write our own patches or exporters,
or we convert logs into something that can be scraped by Prometheus.

### Long-term metrics and optimization

Prometheus metrics are good for short-term monitoring.
This data is most useful
when a change in a metric needs immediate attention
(on a timescale of minutes)
from our [oncall rotation](oncall.md).
On a longer timescale,
there is a different set of metrics that is important to optimize.
For example,
we can measure how many blocks our validator was supposed to produce,
and how many it actually produced.
If we produced only 98% of assigned blocks,
that is something to investigate,
but not something to wake up an oncall engineer for.[^1]

For long-term metrics we combine data from various sources:
we have internal tools that index data from our RPC nodes,
and we work with external sources to verify our own data and fill in the gaps.
To optimize our performance long-term,
we have a [dedicated research team][research] that is continuously
looking for ways to improve our performance.

[research]: https://chorus.one/crypto-research

[^1]: This is because metrics such as _skip rate_
(the percentage of blocks that we failed to produce out of the blocks we were assigned to produce)
are only meaningful when the denominator is large enough.
This only happens at long enough timescales.
For example,
if we measure over a small time window in which we were assigned to produce two blocks,
then the only skip rates we can observe are 0%, 50%, and 100%,
which is very coarse.
To detect small effects on skip rate reliably,
we need a time window with thousands of blocks,
which is typically hours to days,
not minutes.


