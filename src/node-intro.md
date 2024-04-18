# Node Software Best Practices

While validator node software is built by skilled software engineering teams,
the developers do not have as much visibility
into the operational side of things as we do as node operators.
Some challenges only become visible at a certain scale.
For example, disk failures are rare enough that most software engineers
can go an entire career without ever personally experiencing their workstation failing,
but in a fleet of hundreds of servers, disks fail routinely.
In this document we explain what goes into reliably operating nodes at scale,
and what we expect from node software to make this possible.
