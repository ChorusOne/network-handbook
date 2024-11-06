# Physical location

We often get asked “Where do your validators run?”

 * The short but not very useful answer is: _on planet Earth_.
 * The slightly more specific answer is: _mostly in Europe, with some exceptions_.
 * An answer to a slightly different question is:
   _validation services are performed by Chorus One AG,
   a Swiss stock corporation incorporated in Zug, Switzerland_.
 * The longer answer is: _it depends_ and _it’s complicated_.

To give a more complete answer,
we have to explain some things about how validation works,
and what goes into picking a location.
The impatient can jump straight to [the summary](#summary),
but for the full details,
let’s dive in!

## Where is software located?

While the question “where does it run?” sounds simple enough,
it is not always clear what “it” is.

Software consists of computer programs that get executed by a chip.
In our case,
that chip is inside a server,
which is in a rack,
which is in a building,
which is part of a data center facility.
That facility has a clear physical location.
It’s located in a country, and it has an address.
We can say that the program is running in that particular location.

Blockchains are _distributed systems_.
They don’t consist of a single program running on a single machine,
they are emergent systems that arise
from many instances of a program interacting with each other.
These instances can run on different machines,
in different physical locations.
While a particular instance has a well-defined location,
we can’t really answer the question of “where” the blockchain network is,
more specifically than “everywhere where people run nodes”,
which might be as broad as “everywhere on Earth”.[^1]

A blockchain network as a whole does not have a clearly defined location then,
but at Chorus One we don’t operate the entire blockchain network,
we operate validators that are _part_ of the network.
Don’t these validators at least have a clearly defined location?

 * **In simple cases, yes, validators have a clear location.**
   When the validator node software consists of a single program,
   we can point at the machine where that program runs,
   and say “this is where validation happens”.
   At least, at that particular point in time!
 * **In other cases, it’s more complex.**
   For many blockchains, the node software is itself a distributed system.
   Different components can run on different machines.
   Often these machines are in the same data center,
   so we can still give a fairly precise location.
   In other cases, the components may on purpose be geographically distributed.

Let’s go over a few examples to illustrate the subtleties.

[^1]: Probably except for Antarctica.
Antarctica doesn’t have a very stable high-bandwidth Internet connection.

### Simple example: Ethereum anno 2015

Prior to September 2022,
Ethereum was powered by Proof of Work.
In Proof of Work there are _miners_ rather than _validators_.
In broad terms,
the node software consisted of a single program
(Go-Ethereum, _Geth_ for short, being the most popular one).
Even this is an oversimplification,
but for the purpose of this illustration it’s close enough.
You could run the node software on a computer,
and when it mined a new block,
wherever that computer was located,
is where the block was mined.

### Intermediate example: Cosmos SDK networks

Cosmos SDK is an SDK for building Proof of Stake blockchains.
At Chorus One we employ the _Sentry Node Architecture_ for Cosmos-based blockchains.
This means that we run multiple instances of the node software,
on different machines:

 * Multiple **sentries**.
   These nodes connect to peers in the network
   to receive and broadcast blocks and votes.
 * A single **validator**.
   The validator node does not connect directly to other peers in the network.
   To shield it from abuse, it connects only to our own sentry nodes.
   For redundancy,
   we ensure that we have multiple machines that are _capable_ of being a validator at any time,
   but at a given moment,
   only a single instance is validating.

While one could argue that validation happens at the validator machine,
it is opaque to other peers in the network where our validator machine is located.
Externally, only the sentry nodes are visible,
and we can promote different machines to being validator without externally visible effects.
Arguably,
validation is the combination of a validator node and sentry nodes:
without sentry nodes, the validator node is useless.

To complicate matters further,
while the validator node software produces blocks and votes,
it does not sign them directly.
At Chorus One we use hardware security modules (HSMs) for signing where possible.
The hardware security modules we work with are external USB devices
connected to a server.
In the past we connected them directly to the machine
where the validator node software runs,
but this has a major downside:
it makes it difficult to move workloads around.
We have to ask data center personnel to unplug the HSM,
and attach it to a different machine,
which can take hours,
or even weeks when shipping to a different country.

To mitigate this, we use _remote signing_.
We designate some machines as **signers**,
and connect the HSMs to them.
Validators then connect to the signers
over a secure internal network to request a signature.
For stability and performance reasons,
the signer machines need to be reasonably close to validators,
but they need not be in the same data center,
and we have cases where they are not even in the same city.

Because signing is essential for validation,
we cannot allow signer machines to be a single point of failure,
so we have multiple signers
that are able to sign for a particular validator identity.
When multiple signers are online,
a signing request may be serviced by any of them.
While a particular signature is always created by a particular signer,
it might be that the vote for block _n_ and block _n_ + 1
are signed by different signers.
Therefore,
even over a short time period,
the question “where was the signer?”
may not have a more precise answer than “in all of these cities”.

To summarize,
our setup for validating Cosmos-based networks involves three types of machines:
**sentries**, **validators**, and **signers**.
All of them play an essential role in the validation process.
These machines can be located in different cites,
and even in different countries.

### Complex example: Ethereum anno 2024

Since Ethereum moved to Proof of Stake in September 2022,
operating a basic Ethereum validator requires _two_ pieces of node software:

 * An **execution layer client**, such as Geth.
 * A **consensus layer client**, such as Lighthouse.

These nodes can run on different machines in different geographic locations.
As of October 2024,
our execution layer clients and consensus layer clients
are located in different data centers
(the consensus layer runs in a public cloud,
while execution layer clients run on bare metal).
In one case,
while these data centers are geographically close,
they are located in different countries.

The split into an execution layer and consensus layer is far from the only complication.
As Ethereum matured,
and MEV (value that the block proposer can extract due to its privileged position) emerged,
different parties specialized in different parts of the block production pipeline.
At this point,
_Proposer-Builder Separation_ (PBS) is commonplace on Ethereum.
With PBS,
most blocks are not built by the validator node software;
the role of the validator is reduced to merely _proposing_ a block.
Constructing the block itself is outsourced to third party _block builders_.
While these builders are ultimately responsible for building a block,
their role is more akin to that of an integrator than a true builder:
block builders receive bundles
(groups of transactions that together make up the block)
from _searchers_.
To top things off,
the validator node software and block builders
do not communicate directly with one another:
this involves yet another intermediary called the _relay_.
To summarize,
block production on Ethereum involves
_searchers_, _block builders_, _relays_ (all external third parties),
and an _execution client_ and _consensus client_ (both operated by Chorus One).
All of these generally run on different machines,
in different locations.

On top of Proposer-Builder Separation,
_Distributed Validator Technology_
is an emerging trend in the Ethereum ecosystem
that adds a new layer of complexity.
While Ethereum is a distributed system
that remains available even when individual validators fail,
the network penalizes validators that forfeit their duties,
so from the point of view of the validator,
downtime is a severe problem.
If the machine running the consensus client fails,
the validator identity will stop validating.
One way to mitigate this scenario
is by having secondary nodes standing by,
with a process to fail over quickly when the primary fails.
A different way is to replace the node software
with a distributed system that internally runs a consensus algorithm,
turning the validator into a _distributed validator_.
For example, a 3-node system can tolerate one node failing,
and a 5-node system can tolerate two nodes failing.
We could run those nodes on different machines in the same data center.
In this case, the physical location is still a meaningful concept.
Distributing validation over multiple machines in the same data center
protects against some kinds of hardware failure,
but not against e.g. natural disasters that might affect the entire facility.
Therefore,
we might distribute a single validator identity over multiple cities,
and even multiple countries.

<!-- This section has a named anchor to avoid a clash with the Summary h2 -->
### Summary {#summary-location}

While in simple cases it is possible to point to a single machine
with a clear location and say
“this is where validation happens”,
in reality many blockchains consist of multiple pieces of software
that all play an essential role in the validation process,
and these pieces of software can and often do run on different machines,
in different physical locations.
This means that it is not always possible
to give a simple answer to the question of “where does the validator run?”.

## How we pick locations

As we explain in [the hardware layer chapter](the-hardware-layer.md),
we work with multiple providers
who offer servers in various locations.
So how do we decide where to run particular node software?
There are many considerations that factor into this:

 * **Hardware availability.**
   Some chains are not especially demanding on hardware resources,
   and they can run well on most types of servers,
   which are widely available.
   Other chains have more specific requirements.
   For example, some chains are quite sensitive to single-core performance.
   If we have a faster CPU than network average,
   our validator runs well.
   If we would use a CPU that is slower than network average,
   validator performance metrics start to deteriorate,
   and if the CPU is too slow,
   the node software may not be able to keep up with the network at all.
   To run well,
   we use the latest generation CPUs,
   and these are typically scarce.
   Providers get them in limited batches,
   and they may only be available in specific data centers.
   Lead time can also differ from location to location
   — sometimes we can get a server provisioned in a day in one location,
   but it would take two weeks elsewhere
   (the provider has to ship the parts there,
   they may be dealing with supply chain challenges on their end, etc.).
   As a different example,
   some chains require a high-bandwidth network card.
   These are less widely available, so this again restricts where we can run.
 * **Location relative to peers.**
   In general, the further a network packet has to travel,
   the more room there is for something to go wrong.
   Distributed systems are more stable and more performant
   when nodes are located close to each other,
   where latency and packet loss are low.
   Of course there is a trade-off with the next point about centralization.
   For example, nodes in South America and Australia
   are often at a disadvantage stability-wise,
   but they are making a valuable contribution to network resiliency.
 * **Centralization.**
   While being close to peers is good for stability,
   being _too_ close is also risky:
   if too many validators are in the same data center,
   then if anything happens there
   (e.g. a misconfiguration of critical network equipment,
   fire or natural disaster at the site,
   or legal pressure),
   it could be a hazard to the blockchain network as a whole.
   We try to avoid running from data centers
   that already have a large concentration of stake.
 * **Redundancy.**
   As explained in [the reliability chapter](reliable-systems.md),
   for any node software we operate,
   we generally run it on at least two different machines,
   so that if the primary fails,
   a secondary that is standing by can take over.
   For maximum reliability,
   we want failures to be uncorrelated.
   That means that the secondary should be with a different provider,
   in a different geographic location
   — though again, there is a trade-off.
   Although we can be a bit more lenient with a secondary,
   because it’s not used as often,
   it still needs to be close to peers while avoiding centralization risk.
 * **Cost.**
   Even if multiple locations are available that satisfy the above criteria,
   not all of them may be cost-effective.
 * **Preference for Europe.**
   We spread our presence to avoid critical dependencies on a single location,
   but spreading our infrastructure brings challenges of its own.
   As we observed before,
   distributed systems tend to become slower and less stable
   when they are spread out further.
   Although we have a global team,
   and we operate servers worldwide,
   the majority of our infrastructure is located in Europe
   (including the UK and Switzerland).
   Europe is diverse enough in terms of geography, jurisdictions, and providers,
   to avoid creating single points of failure.
   It is small enough that latency between servers is acceptable for most purposes,
   and globally it is well-connected to both the US and Asia.
   We do operate servers in other continents,
   in particular we have a small footprint in Asia,
   but the vast majority of our servers are located in Europe.

To summarize,
there are many factors that constrain where we can run a particular piece of software.
We are able to operate servers worldwide,
but the majority of our infrastructure is in Europe.
Within Europe,
we make a trade-off between
the performance of our own node,
network centralization,
and cost-effectiveness.

## The optimal location is dynamic

When we onboard a new network,
we use the considerations listed above to pick a location.
However, these considerations are not static;
the optimal location changes over time!

 * **Newer, faster CPUs get released regularly.**
   A machine that is at the cutting edge of performance today,
   which enables us to outperform other node operators,
   may be too slow to even keep up with the network two years from now.
   We migrate our most demanding workloads several times per year
   as new hardware options become available,
   and those new options
   may be in a different data center than where the workload currently runs.
   Even when performance is not an issue,
   when hardware reaches the end of its lifespan,
   its replacement will not necessarily be in the same location.
 * **The set of peers changes, and peers move.**
   We move our workloads around, and so do other node operators.
   In addition to that, stake distributions change,
   and this can affect how valuable certain peers are.
   It’s good to be close to a peer who proposes many blocks,
   because then you get to see many blocks quickly,
   but if that peer loses stake and starts to propose fewer blocks,
   that can make the location less attractive.
   We constantly have to re-evaluate what the most effective location is,
   while avoiding centralization risks for the network.
 * **Networks evolve, trends change.**
   As networks mature,
   the node software tends to become more operationally complex,
   with more parameters but also more constraints.
   For example, following
   [the introduction of PBS on Ethereum](#complex-example-ethereum-anno-2024),
   it’s not just the location relative to peers that matters,
   but also the location relative to the _relay_.

Because Chorus One works with multiple providers in many locations,
we have the ability to move workloads around and _test_ where they perform best.
Our infrastructure is set up to be distributed,
and it is relatively easy for us to move workloads around,
and try out new locations and machine types.

## Machine roles are dynamic

The set of machines that we use for running node software changes over time,
to optimize the location as explained in the previous sections.
These changes happen on a timescale of weeks to months.
Because we operate many different blockchain networks,
our fleet is large enough that we add and remove machines on a weekly basis,
but for a given network,
the set of locations where we run the node software is generally stable
for weeks to months.

Even though we don’t move the node software around that quickly,
we can change the _role_ that a node performs much faster.
As explained before,
we generally run multiple instances of the node software for redundancy.
The details vary from network to network,
but typically one instance will be actively validating
(participating in consensus and proposing blocks),
other nodes download and validate a copy of the chain,
so they are ready to take over validator duties at any time,
but they are not participating in consensus or proposing blocks.
From the point of view of the network,
they are just unstaked peers.
When needed
(in the case of hardware problems,
but also to e.g. perform a software update),
we can stop validation at the current instance,
and promote a secondary instance to start validating.
This process is called _failover_.
To peers in the network,
it looks like our validator identity
suddenly jumping from one location to another.
Our validator identity may be “located” in one city at one moment,
and in a city several thousand kilometers away the next.

The details of the failover process
(and whether it is possible at all)
vary from network to network,
but it generally takes seconds to minutes,
and we can perform it multiple times per day,
and even per hour if needed.
We do not just use this process to perform zero-downtime updates,
and to guarantee reliability.
We can also use this process to experiment,
and measure the impact of location on performance.
This means that the location of our validator identity
can move around between locations,
sometimes multiple times per day.

## Summary

 * The vast majority of the servers that we operate are located in Europe,
   distributed over multiple providers and data centers in various countries.
   As of October 2024 we do not operate node software in the United States,
   although we have done so in the past,
   and we may do so again in the future.
 * Blockchain node software often consists of multiple components
   that each play an essential role in validation.
   These components can run on different machines,
   which may be located in different cities or even countries.
 * When we choose where to run a piece of software,
   we have to consider many factors,
   including hardware availability,
   location relative to peers,
   network decentralization,
   redundancy, and cost effectiveness.
 * Because the optimal location changes over time,
   the set of machines that we use for a particular blockchain network
   is not static,
   it evolves on a timescale of weeks to months.
 * In order to guarantee high uptime,
   we run multiple instances of the node software.
   The particular instance that is validating on behalf of our validator identity
   can vary from one moment to the next.
   In some cases, this can change several times per hour.

## Sure, but where do your validators run?

Validation services are performed by Chorus One AG,
a Swiss stock corporation incorporated in Zug, Switzerland.
[You can find our address at chorus.one](https://chorus.one/contact-us).

### Available locations for white-label validators

If you are interested in white-label validation services
and you have a preference for a particular region,
please let us know what you have in mind.
We likely already work with providers in that region
(even if it’s not in Europe),
and we can very likely find a solution that accommodates your needs.
Having said that,
[there are many factors that affect how we decide where to run a piece of software](#how-we-pick-locations),
and adding constraints limits our ability to provide the best service.
Restricting locations may come at the expense of increased cost and lead time,
and can impact the performance of your validator.

If you have regulatory or legal requirements that put restrictions on the region,
we can work with you to clarify the interpretation of such requirements
in the context of a particular blockchain network.
[As we explained above](#where-is-software-located),
distributed systems do not always have a clearly defined location,
and in a software system that is ultimately the result
of an interaction between many programs that run on many servers,
it is not always clear where to draw the boundary
of what is considered part of the validator.

### Location snapshots

If you need a point-in-time snapshot of the locations
where we currently operate node software for a particular blockchain network,
we can provide this on request.
As explained in this chapter,
the set of locations where we run node software changes over time,
so this snapshot is likely to become outdated in a few weeks to months.
Furthermore,
the role of the different nodes that are involved
can change on even shorter timescales.
