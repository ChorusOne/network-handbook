# The hardware layer

At Chorus One we specialize in everything above the hardware layer,
and we outsource the physical infrastructure.
Our economy of scale is automation to administer servers across many providers,
and automation to operate many different blockchain networks.
In terms of hardware footprint,
we are not so large that it makes sense for us to own the hardware layer of the stack.

### Physical infrastructure

We work with multiple providers who offer servers for rent,
together with the rackspace, installation services, Internet connectivity, etc.
In some cases these providers are vertically integrated and have their own data centers,
in other cases they lease the base infrastructure but own the servers and networking equipment.
Often providers work with a mix of both depending on the location.
We do not own any server hardware;
sourcing and assembling the parts is done by the provider.
For us this is the sweet spot that is more flexible and hands-off than building and servicing our own servers,
while also being several times cheaper than virtual resources in the cloud.

### Hardware configuration

The servers we work with are most suitable for applications
that require a balanced mix of CPU cycles, memory, storage space, and network bandwidth.
This is the case for most blockchains,
but not for some more specialized peer-to-peer networks.
For example, we don’t try to offer competitive pricing per gigabyte for storage networks,
as that requires very different purpose-built server types.
A few terabytes per blockchain is fine,
but our price-per-gigabyte is not competitive compared to parties who build and own purpose-built storage servers.

### CPU Architecture

All our servers use x86-64 CPUs,
as this is still the standard architecture that all software can run on,
and in the server market, the top performing CPUs
(in terms of instructions per second, not performance per Watt) are still x64 CPUs.

### Operating system

Our production systems run long-term support versions of Ubuntu Linux,
because this is the greatest common denominator that most software tries to be compatible with.
