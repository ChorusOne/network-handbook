# The unique challenges of bare metal

Given that we run on bare metal,
we face a class of challenges that does not exist in the cloud.

* **Hardware lead time.**
For popular server configurations,
our vendors tend to have these pre-assembled,
and we can get a machine in hours.
For more specialized configurations,
our vendors themselves are dealing with lead times on the components,
and it can take weeks before a machine is delivered.

* **Flash memory wears out.**
SSDs are consumables, they are rated for a limited number of writes.
Many workloads never exhaust the writes, and the hardware is obsolete before it ever reaches its rated lifespan.
But if there is one class of applications that is write-heavy,
then it’s blockchains that are continuously writing new blocks and indexes.
We do observe disks wearing out, and we routinely need to get them replaced.

* **Other hardware can fail too.**
Although disk failures are the most common hardware issue we observe
(not only due to wear),
other hardware components can and do fail.

* **Maintenance downtime.**
In the cloud, a virtual machine can migrate to another host
so the original machine can be serviced with minimal impact to the user.
On bare metal, we have to turn off the machine,
and a technician has to walk to the rack and take the server out to service it.
This takes minutes at best, sometimes hours.

* **Limited storage capacity per machine.**
The amount of storage we can put in a single machine is limited.
While there exist dedicated storage servers that can hold petabytes worth of data,
that is not the kind of fast NVMe storage that blockchains demand nowadays.
8 TB of NVMe storage per server is pretty standard.
More than this is possible,
but might not be available in every location
or with every CPU model or network card,
so this may limit our ability to provide geographic redundancy
or best-in-class hardware.

* **Commitment periods.**
A high-end server is a serious investment for our vendors,
and some of these machines are specialized enough
that they may not be able to easily repurpose them after we no longer need the hardware.
This means that when we order a machine,
we often have to commit to renting it for a period of months to years.

The general theme is: we have to deal with unreliable components,
and when they fail, we may not be able to order a replacement quickly. 
