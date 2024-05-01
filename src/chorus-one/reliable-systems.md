# Building reliable systems from unreliable parts

When you operate enough machines for a long enough time,
unlikely events become routine,
and the unthinkable becomes a serious risk.
At Chorus One we’ve dealt with data centers catching fire,
data centers flooding,
blockchain networks unintentionally causing DDoS attacks,
and vendors blocking traffic without notice.

Although we work with enterprise-grade hardware
that is more reliable than consumer hardware,
all hardware fails at some point.
At a certain scale, hardware failure becomes inevitable.
If a disk has a 1.2% probability of failing in a given year,
then across a fleet of 500 machines with two disks each,
there’s about a ⅔ probability that at least one disk fails in a given month.
The solution to this is redundancy.

There are a few levels at which we can implement redundancy,
but we choose to do it at the node software level,
by running multiple instances of the same software on different machines.
This is the most general, and a good fit for blockchain software.
Let’s look at why other levels are inadequate.

* **RAID-style redundant storage.**
While redundancy at the block device level ensures
that we still have a copy of the data if a disk fails, 
the faulty disk needs to be replaced, which causes downtime.
Furthermore, while RAID protects against disk failures,
it does not protect against other types of hardware failure,
natural disaster, or software bugs that cause corruption.
When there is a single source of truth for the data,
RAID may be the only option.
But for blockchains, we have better options.
 
* **Redundant network storage.**
We could run our own multi-node storage cluster that can tolerate single nodes going offline,
such that we can service one machine without impacting storage.
This incurs a performance overhead and is operationally complex.
To keep performance overhead manageable,
the nodes must also be geographically close
(preferably at the same site, probably not in different cities).
This means it doesn’t protect against natural disasters.

* **Block device-level replication is not needed.**
By their nature, every node in a blockchain network stores the same data.[^erasure-coding]
This means we do not need to have replication at the block device or file system layer:
we can simply run multiple instances of the node software instead.

For the non-public data that we cannot afford to lose
(in particular, cryptographic keys)
we do use redundant storage clusters such as Hashicorp Vault,
but this data is tiny in comparison to the blockchain data we handle,
and IO performance is not a concern.

To summarize,
our approach to redundancy is to run multiple instances of the node software,
on different machines, in different geographic locations, with different vendors.
This protects us against a wide variety of disasters:

 * Hardware failure
 * Failure on the data center level, including natural disaster
 * A vendor or internet service provider going offline completely, for whatever reason
 * Software bugs that trigger nondeterministically
 * Operator error (through staged rollouts)

Our approach to reliability is not to try and mitigate individual components failing.
We take it as a given that some components are going to fail, and through redundancy,
we build systems that are reliable regardless of the reliability of the underlying components.

[^erasure-coding]: This is changing with the advent of erasure-coded data sharding and so-called _blobspace_.
Fortunately, if the choice about what data to store is deterministic,
we can still configure multiple machines to store the same data. 

