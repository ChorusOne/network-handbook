# Identity and key management

A validator on a blockchain network has an identity.
The identity should have an associated key pair
which we can use to prove ownership of that identity.
Often there is on-chain metadata associated with a validator identity,
such as a name, website, icon, commission percentage, etc.

A validator identity should fundamentally be tied to a cryptographic key
that we can independently generate.
Since such keys are random and not human-meaningful,
an optional name system can help,
although in our experience,
impersonation of validators is not (yet) a concern in practice.
A validator identity should be independent
of where we happen to run the node software;
it should be possible to migrate a validator workload between machines.
In other words,
a validator identity is a long-term stable identifier,
distinct from a short-term session identifier.

## Key management

#### Enable node operators to generate private keys. {.p1 #generate-private-keys}
It should go without saying that a private key needs to be kept _private_.
This means that we as node operator must be able to generate a key pair on our end,
and we never share the private key with any other party.
We cannot accept externally generated keys,[^1]
as the privacy prerequisite has been violated.
Even for testnets, we cannot accept externally generated keys
— it means we wouldn’t be able to test the parts that matter for a mainnet.
We need to be 100% sure that if anything is signed with our private key,
that was _our_ doing,
so no other party can be allowed to have a copy of the private key.
Private keys shared between multiple parties are not private,
and should be considered compromised.

#### Ensure keys used for routine operations can be rotated. {.p2 #key-rotation}
As the our identity is tied to our private key,
this key is extremely sensitive.
If it is compromised,
we lose our entire validator,
and all delegators are at risk.
We prefer to keep access to such sensitive keys very tightly controlled,
ideally in a cold hardware wallet.
A sensitive key that is locked down like that,
is unsuitable for day to day operations:
signing is secure,
but slow and inconvenient.

However, our validator identity has duties on the network.
At the very least,
it needs to sign consensus votes and blocks
on a regular basis,
which means that the private key for that needs to be hot:
in the memory of the machine where the node software runs.
Ideally,
that consensus key is a *different* one than the one that represents our identity.
This leads to a more secure network,
because the consensus key can be rotated using the main identity key.
Unlike compromise of the main identity key,
compromise of the consensus key is not fatal.

Support for hardware security modules,
as well as a remote signing protocol,
can help to mitigate the risk of having keys in memory.
This is an additional layer of security,
but does not remove the need for key rotation.

Some node software generates an ephemeral session key at startup.
If that key must be signed with the main identity key,
that still means that we need access to the main identity key
for routine operations like a software update or reboot,
which means the identity key is exposed to more risk than necessary.
Therefore,
even when nodes use ephemeral session keys,
an intermediate key that can be rotated is still useful.

Finally,
there are other operations that require our signature,
such as participation in governance.
It is nice if those can be performed using a separate key as well,
for the same reasons as described above:
so that we can segregate responsibilities,
and we don’t need to expose the sensitive identity key to unnecessary risk.

#### Allow the main identity key to be rotated. {.p3 #main-key-rotation}
Blockchains and node operators come and go.
It happens occasionally that a node operator no longer wishes to operate their node,
but shutting down the validator entirely can be disruptive for the network.
For example,
the validator may have delegations from many anonymous people on the Internet,
and many of them do not follow announcements on websites and social media,
and will not redelegate in time.
To ensure continuity,
a different node operator may be willing to adopt the node.
We as Chorus One have adopted nodes from other parties in the past.
To support a cryptographically secure transfer of a validator identity,
it must be possible to rotate the main identity key:
the new node operator generates a new key pair,
and the old one signs a rotation message with the old pair.

A key rotation mechanism is also helpful in cases of a security breach,
where a key compromise cannot be ruled out.
Out of an abundance of caution,
we would prefer to be able to rotate keys in such a situation.
Of course, it is our responsibility as a node operator
to ensure that keys are not compromised in the first place,
but you build secure and resilient systems
not by assuming that everything goes right,
but by having layers of defense for when things inevitably do go wrong.

## Meaningful identities and vanity addresses

Key pairs should be generated randomly,
and are therefore not human-meaningful.
Validators are identified by public key,
so these long random strings pop up everywhere.
Humans are bad at remembering long random strings.
This creates friction.

The proper way to deal with this,
is to adopt and integrate a _name system_:
a registry that maps unique human-meaningful names to public keys.
Make sure that it is widely supported
— that names can be used instead of public keys in virtually all places,
but most of all,
that they are _displayed_ alongside public keys.

When there is no official well-integrated way of having human-meaningful names,
people will find workarounds.
In particular,
it is possible to grind a _vanity address_:
a keypair whose text-encoded public key has a meaningful prefix or suffix.
The longer such affix,
the more difficult such addresses are to grind,
but finding a 5–6-character affix is inexpensive.
Such addresses seem convenient:
now you can tell from the public keys what they identify,
or who they belong to … or can you?

Unfortunately, vanity affixes do not authenticate anybody.
Any random person with a little compute to spare,
can search for a vanity key with the same prefix or suffix as yours.
**Vanity addresses fundamentally do not identify an entity.**

Okay, so vanity addresses do not identify an entity,
but as long as we don’t use them for authentication,
they are not exactly harmful either,
right?
Well, in practice they are.
Humans are inherently lazy,
they _will_ rely on those affixes even when they should not.
Exploiting this weakness is also called an _address poisoning attack_.
On the one hand,
that’s an operator error
— the human is at fault, it’s not a bug in the system —
but certainly we can design systems to protect against,
rather than encourage human error.

Aside from the social danger of vanity addresses,
an improperly seeded random number generator
that reduces the effective keyspace
is a common class of fatal mistake in cryptographic code.
Vanity address generators are not without risk!

#### Discourage the use of vanity addresses. {.p3 #no-vanity}

As the node software author,
you can’t stop others from building programs that search for vanity addresses,
but you can certainly help to build better alternatives:
a well-integrated name system;
interfaces that do not rely on humans to manually compare long strings,
etc.
Furthermore,
you can educate your users about the risks of vanity addresses.[^2]

## Reliability and failover

As we describe in the [_reliable systems_ chapter](../chorus-one/reliable-systems.md),
we run multiple instances of the node software for redundancy,
to remain available during maintenance windows,
and to ensure reliability in the case of hardware failure or network disruptions.
These instances run on different machines,
in different locations,
with different IP addresses,
they have their own independent data directory, etc.
To build a highly available system out of multiple less available instances,
[and to optimize performance](../chorus-one/physical-location.md#machine-roles-are-dynamic),
we need to be able to reconfigure instances at short notice.

The details of how and what to reconfigure vary from chain to chain.
Often the same software can be configured to either be actively validating,
or act as a passive RPC node.
In that case we work with a _primary_ and one or more _secondary_ instances.
Some node software follows a more modular approach,
with external signer daemons,
or validators that are shielded from the p2p network through sentry nodes.
Either way,
we need to be able to move workloads between machines,
and move our validator identity around.

#### Build for redundancy. {.p3 #build-for-redundancy}
No node software runs indefinitely.
Hardware fails,
the network fails,
or maybe we just need to reboot the host machine to pick up a kernel security update.
However, we have a duty to vote in consensus and produce blocks,
so we can’t be offline too long.
Therefore, we need a mechanism to support high availability.
There are multiple ways of achieving this,
but in our experience,
simpler systems are more reliable.
Turning the validator itself into a distributed system with internal consensus
is rarely worth the complexity and hardware overhead;
good support for simple primary/secondary failover is more valuable.
Fast restarts,
and storing identity-specific state (e.g. a database of past votes)
separately from global state,
can help with that.
<!-- TODO: I feel there is much more to write here, maybe even a separate
chapter. -->

Decoupling signing from the rest of the node software
in principle only exacerbates the problem
(now the signer _also_ needs to be highly available),
though making a signer highly available is generally more tractable,
as it requires fewer resources than a full validator node.

#### An IP address is not an identity. {.p1 #ip-is-not-identity}
[We run node software on machines that we do not own](../chorus-one/the-hardware-layer.md),
with vendors whose network setup we do not control.
We get assigned an IP address by the vendor,
and that address is not our property.
Therefore, it cannot be used as a long-term identity.
It may be used in a peer to peer network
to identify a particular session of running the node software on a machine,
but we may need to move the workload to a different machine
[to ensure reliability](../chorus-one/reliable-systems.md).
That machine is likely with a different vendor,
where we cannot easily migrate the IP address along.

If you need a way to discover the endpoint (IP address and port)
from which our identity (determined by our public key) is currently operating,
there are several ways to achieve that:

 1. **Keep a mapping from identity to endpoint in your p2p layer.**
    This is the preferred approach: as long as a peer has an entry point
    to the p2p network, it will be able to discover our endpoint.
    If we move the workload to a different machine,
    the address info will automatically be up to date.
 2. **Use DNS.**
    If the above approach is unsuitable,
    for example when we are one of the entry nodes of the p2p network,
    then accept a domain name rather than IP address.
    This ensures that we can point the domain to a different machine
    when we need to migrate the workload.
    Do not hard-code an IP address.
 3. **Track endpoints on-chain.**
    DNS is convenient, but it has weaknesses.
    It poses centralization risks and may be subject to censorship.
    An on-chain mapping of identity to endpoint
    provides a decentralized alternative.
    Furthermore, unlike DNS, it can natively incorporate port numbers.
    For this mechanism,
    ideally the node software registers itself on-chain automatically at startup.
    If a separate step is needed to submit the registration transaction,
    it should be possible to sign with a [separate key that can be rotated](#key-rotation),
    so that we are not dependent on the sensitive identity key
    for routine maintenance operations.
    Because failover cannot always be planned,
    such on-chain changes need to be effective immediately,
    and not at e.g. the next epoch.

#### Avoid IP whitelisting. {.p2 #no-ip-whitelisting}

Because an IP address is not an identity,
IP whitelisting is not authentication.
IP whitelisting creates inconvenience and risk for both parties involved:
for the whitelisted it makes it harder to move workloads,
and for the whitelister it creates a risk
when the original user abandoned a whitelisted IP address,
and that address is now in the hands of a new, untrusted tenant.
Instead of IP whitelisting,
rely on public key cryptography for authentication.

#### Enable runtime reconfiguration. {.p3 #runtime-reconfiguration}
If the node software takes more than a few seconds to fully start
— for example because it needs to load a lot of data from disk,
or because it needs to re-establish connections with peers —
then restarting the node software with a new configuration causes downtime.
Ideally in that case,
there is a way to reconfigure the instance’s role and identity at runtime,
so we can perform failover with virtually zero downtime.

[^1]: There is one exception to this:
when we adopt a validator identity from a node operator
who no longer wishes to operate that node,
on a network that does not support key rotation.
We only do this when we _have_ to.
Some implementations don’t offer any alternatives.
In this case,
the private keys are no longer guaranteed to be private,
and a mere legal agreement is the best guarantee we can get.
We judge on a case-by-case basis whether we can stake our reputation
on the counterparty’s word,
and we don’t do this lightly.

[^2]: We should admit that our main Solana validator uses a vanity address.
What can we say? We were young once&nbsp;…
This handbook consolidates our learnings as a node operator,
and we learned these best practices over time,
many of them the hard way.
Unfortunately, the key in question cannot be rotated.
