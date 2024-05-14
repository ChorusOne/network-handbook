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
we allocate our blockchain workloads manually to machines.
We do use Kubernetes for some internal applications and stateless workloads
that just need to run _somewhere_, but for blockchain workloads,
we want to have full control over workload placement.
