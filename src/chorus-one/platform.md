# The Chorus One platform

Chorus One is a node operator on many different blockchains and decentralized networks.
To enable this,
we build an internal platform optimized for running distributed systems.
It consists of:

 * [A global network of bare metal servers](#global-presence)
 * [A small cloud footprint](#cloud-footprint)
 * [A unified internal network](#network)
 * [A base layer of core services](#core-services)
 * [A flexible configuration layer](#flexible-configuration-layer)
 * [Build and deployment automation](#build-and-deployment-automation)
 * [Monitoring and alerting infrastructure](#monitoring-and-alerting)
 * [An experienced platforms engineering team](#platforms-engineering)

Together these enable us to run blockchain workloads quickly, efficiently, and securely.

## Global presence

We operate a network of hundreds of [bare metal](the-hardware-layer.md)
servers [worldwide](physical-location.md).
We have presence in dozens of cities across 15+ countries,
across multiple vendors and transit providers.
This makes us redundant against the most thorny kinds of failure,
including loss of an entire data center,
natural disaster,
and vendor network failure.
It also gives us the flexibility to move workloads around,
to optimize performance and aid decentralization.

Our hardware layer is dynamic:
we add and remove servers multiple times per week.
We have good relationships with vendors
that enable us to get access to the latest hardware,
expand our presence at short notice,
and reconfigure machines when needed.

To thrive in this heterogeneous environment,
we have internal tooling that integrates with vendor APIs
to give us a single cross-vendor overview of our infrastructure,
and we provision all machines using our own installer
that ensures a uniform base OS regardless of vendor idiosyncracies.

## Cloud footprint

We have a small cloud footprint that complements our bare metal presence.
For [reasons described in later chapters](cloud-vs-bare-metal.md),
the majority of our production workloads run on bare metal,
but we leverage cloud where it makes sense.
A small fraction of our workloads run on virtual machines,
and aside from that we use object storage,
container registries,
etc.

## Unified internal network {#network}

Our multi-vendor setup is resilient,
but it means that for private traffic between servers,
we cannot always rely on vendors’ internal networks such as VLANs.
To enable workloads to connect across vendors
without exposing them to the public Internet,
we use a secure internal Wireguard network.
This is a point-to-point network:
machines connect directly to other machines,
without additional hops that add latency or create central points of failure.
The network is guarded by strict access policies
that act as an additional layer of defence,
before a firewall even comes into play.

Most of the services we run are geographically replicated.
We have internal tooling that routes traffic to the nearest healthy node,
with the ability to fall back to further nodes
when a service becomes unhealthy.
This enables us to offer the lowest latencies in the common case,
and in case of maintenance or hardware failure,
systems remain available,
just temporarily at slightly reduced performance.
This way we can offer both high performance and high availability.

## Core services

We operate core the services that our workloads depend on ourselves.
This gives us full visibility and control in case of issues,
and enables us to be resilient against outages of an entire vendor.
Core services include a highly available HashiCorp Vault cluster
that runs on a set of hardened servers,
a Postgres cluster,
Apache Airflow,
[monitoring and alerting services](#monitoring-and-alerting),
loadbalancers and ingress servers,
and a Kubernetes cluster.

## Flexible configuration layer

At Chorus One we configure our servers and workloads using infrastructure as code.
We use configuration management tools such as Ansible and Terraform
to configure hosts and cloud resources.
Because [workload placement is a complex problem](workload-placement.md),
we have tools that enable us to reconfigure systems quickly.
We leverage Python to parametrize and validate repetitive configurations,
and to get a holistic view of which workloads run on which host.

To support moving workloads around,
we also have internal systems to take and move snapshots of data directories,
so we can start new nodes without having to sync from genesis,
and without having to blindly trust external snapshots.

## Build and deployment automation

We operate more than 200 pieces of node software and related tools,
many of which release multiple times per month,
sometimes per week.
Often there is time pressure to roll out a new version.
[We build this software from source where possible.](../node-software/build-process.md)
To manage all this,
we have automation that watches upstream repositories for new tags,
and automatically builds and packages new versions.
As of June 2025, this automation handles dozens of upstream releases per day.
Automation ensures that the process is quick, consistent, traceable,
and eliminates room for human error.
This is especially valuable in case of chain-wide emergencies.

After we build a new release,
we need to deploy it to the right hosts and restart any daemons.
Where possible,
we avoid restarting validating nodes,
and we fail over to a hot spare first,
or we build a highly available remote signing setup.
To catch issues before they affect validating nodes,
we do staged rollouts.
Depending on the node software,
even a normal restart can be non-trivial:
the node can take time to catch up to the rest of the network,
and we need to keep enough capacity online at all times during the rollout.
To eliminate room for human error,
and to reduce downtime to mere seconds,
we have internal automation that can ochestrate
complex deployments across nodes.

## Monitoring and alerting infrastructure {#monitoring-and-alerting}

To be confident that all our nodes are running as expected,
and to be able to alert [our 24/7 oncall rotation](oncall.md) in case of anomalies,
we invest a lot of time in monitoring.
We monitor both on short timescales needed for incident response,
and on longer timescales for performance optimization.
As blockchains are distributed systems,
understanding the state of the network is an interesting problem,
and we monitor both node-local and network-wide metrics.
See the [monitoring and alerting chapter](monitoring-alerting.md) for more details.

## The platforms engineering team {#platforms-engineering}

Our platform is built and operated by several platforms engineering teams.
Each team is responsible for a specific set of blockchains,
as well as parts of the shared infrastructure.
The teams consist of a mix of _platforms engineers_ and _infrastructure software engineers_.
We treat these roles as a spectrum rather than dev/ops silos:
all our platforms engineers can code,
and all our software engineers have
hands-on operational experience.
Our platforms engineering teams participate in our [24/7 oncall rotation](oncall.md).
In short,
the people who build our infrastructure are also responsible for operating it,
including incident response.
This ensures that our people have deep expertise about the software we run,
and they are empowered to decide where automating things has the greatest impact.

Our engineering organization
consists of more teams than just our platforms engineering teams,
but the scope of this book is limited to platforms engineering.
