# The cloud computing vs. bare metal trade-off

TODO: Intro should probably go here, not on the top level.

Two undeniable strengths of cloud computing are reliability and flexibility.
You can spin up a virtual machine in seconds,
and the virtual machine essentially never fails.
Clouds have the freedom to live-migrate VMs on scheduled host maintenance,
and even detect unhealthy hosts early and migrate VMs away
before customers notice any impact.
Virtual disks can be backed by redundant network storage.
The cloud provider is doing the hard work
of presenting virtually infallible disks to the customers.
Behind the scenes there are still fallible disks,
but to the guest operating system, IO failures are a relic of the past.
Virtual disks can also be resized on demand
to sizes well beyond the capacity of a single physical server.

These advantages of cloud computing come at a cost.
There are literal costs:

 * **Resources are more expensive.**
   Cloud compute, memory, and storage can be 2 to 10 times as expensive as the bare-metal equivalent.

 * **Cloud bandwidth is metered.**
   The cost of a month of 10 Gbps egress is in “contact sales” territory,
   and at public prices costs about 200× as much
   as an unmetered 10 Gbps connection at a bare metal provider.
   For a web application that processes a few small requests per second
   the egress cost is manageable,
   but for bandwidth-hungry applications such as video streaming
   or chatty peer-to-peer blockchain networks,
   cloud egress is prohibitively expensive.

Aside from financial costs,
running in the cloud also means sacrificing performance and control:

 * **Performance can vary wildly between different CPU models.**
   A 5 GHz latest generation AMD CPU can finish some single-core workloads
   in 1/5th of the time it takes an 8-year old 2.4 GHz Intel CPU.
   In the cloud, compute is measured in virtual CPU cores,
   and you get only very indirect control over what CPU family that is
   (“performance-optimized” vs. “best price-performance”).
   For many web applications that are IO-bound anyway,
   single-core performance is not a decisive factor and cloud vCPUs are more than adequate,
   but for compute-intensive workloads,
   having access to the fastest CPU on the market is a clear advantage.

 * **Networked storage is reliable, but at a latency and throughput cost.**
   The fastest durable storage technology available today
   are SSDs that connect directly to the CPU’s PCI bus: NVMe drives.
   Virtualized network storage, although more reliable,
   will never be able to match this in performance.
   Read throughput in clouds [tops out around a GB/s][gce-disk],
   while an array of local NVMe drives [can reach 20× that][intel-d7].
   Again, for most web applications this is hardly relevant,
   but for storage-intensive applications such as databases and blockchains,
   this can mean an order of magnitude performance difference.

 * **There is overhead to CPU virtualization.**
   Fortunately this overhead is small nowadays,
   but for performance-oriented networks, every little bit helps.

 * **Public clouds do not support custom hardware.**
   For some blockchains, we work with hardware security modules.
   These are small USB devices that we prepare,
   and then plug in to the physical server at the data center.
   This means we need a dedicated server, and even then,
   not all vendors are willing to do this (for understandable reasons).

These trade-offs mean that while cloud computing is a great default choice for many applications,
the specialized requirements of the blockchain networks that we run
mean that cloud is either not cost-effective,
or doesn’t offer adequate performance to meet the demands of performance-oriented networks.
At Chorus One we use cloud where it makes sense,
but the vast majority of our workload runs on bare metal.

[gce-disk]: https://cloud.google.com/compute/docs/disks/performance
[intel-d7]: https://www.anandtech.com/show/15860/intel-announces-d7-series-pcie-40-enterprise-ssds
