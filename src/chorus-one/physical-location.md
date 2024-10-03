# Physical location

We often get asked “Where do your validators run?”

 * The short but not very useful answer is: _on planet Earth_.
 * The slightly more specific answer is: _mostly in Europe, with some exceptions_.
 * The longer answer is: _it’s complicated_.

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
we can’t really answer the question of “where” the blockchain network is
more specifically than “everywhere where people run nodes”,
which might be as broad as “everywhere on Earth”.

A blockchain network as a whole does not have a clearly defined location,
but at Chorus One we operate validators that are part of the network.
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

* Failover.
