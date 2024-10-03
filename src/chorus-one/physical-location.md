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
and what goes into choosing a location.
Let’s dive in!

## Where is software located?

While the question “where does it run?” sounds simple enough,
it is not always a meaningful question to ask,
primarily because of ambiguity about what “it” is.

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

### Simple example: Ethereum anno 2022

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
In some cases we connect them directly to the machine
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
Validators then connect to the signers over an internal network to request a signature.
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

[^1]: Probably except for Antarctica.
      Antarctica doesn’t have a very stable high-bandwidth Internet connection.
