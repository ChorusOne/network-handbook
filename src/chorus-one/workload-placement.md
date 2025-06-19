# Workload placement

The blockchain workloads that we run
place constraints on where and how we can run a piece of software:

* For chains with special hardware or bandwidth requirements,
  only the machines that we ordered specifically for this network are suitable for running it.
* For especially demanding node software, we use a dedicated machine.
  For less demanding node software, we may run multiple different blockchains
  on the same machine to improve utilization.
  To avoid correlated failures,
  we don’t want to co-locate the same pair of blockchains on multiple servers.
* We want to be close enough to peers to get low latency and minimize packet loss,
  though not so close that we risk creating a centralization vector for the network.
  We prefer to avoid data centers that already host too many other nodes,
  though there’s a stability/decentralization trade-off here.
* For a redundant pair
  (two instances of the node software running on different machines),
  we want the two nodes to not be in the same data center,
  and preferably in different countries,
  in data centers owned by different parties.
* The use of hardware security modules further limits the data centers we can use.

In other words, both our workloads and our machines are very heterogeneous with many specific constraints.
Generic workload schedulers such as Kubernetes or Hashicorp Nomad
work well with a fleet of homogeneous machines,
but are less suitable for our blockchain workloads.
On top of that, blockchain node software is typically not designed
to be terminated and restarted elsewhere at short notice by a generic workload scheduler.
(For example, it has to re-discover peers in the peer-to-peer network, which impacts stability.)
In addition, for some high-performance blockchains we tune kernel parameters for that particular blockchain.

Because of these reasons,
we allocate our blockchain workloads statically to machines.
We do use Kubernetes for some internal applications and stateless workloads
that just need to run _somewhere_, but for blockchain workloads,
we want to have full control over workload placement.
Control over placement does not mean that our infrastructure is rigid,
or slow to change.
On the contrary,
we have an advanced configuration system
and internal tools
that enable us to change workload placement at short notice.
We have many servers available that are capable of running a given workload.
We ensure that workloads have a secondary (a _hot spare_) where possible,
so we can fail over workloads in seconds to minutes.
Even reconfiguring where secondaries run
is something we can do in minutes to hours.
In short, our infrastructure is fairly dynamic:
we can and do move workloads around regularly.
This process is automated, but not _autonomous_.
Due to the complexity of constraints and the value at stake,
we keep a human in the loop to make a placement decision.
