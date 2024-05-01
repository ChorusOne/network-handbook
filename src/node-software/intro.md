# Node Software Guide

Validator node software is built by skilled software engineering teams,
but the developers do not always have as much visibility
into the operational side of things as we do as node operators.
Some challenges only become visible at a certain scale.
For example, disk failures are rare enough that most software engineers
can go an entire career without ever personally experiencing their workstation failing,
but in a fleet of hundreds of servers, disks fail routinely.
By sharing our perspective,
we aim to help networks build better software for more stable mainnets.

In this chapter we share insights that we’ve learned
from operating more than 50 networks for many years.
We explain what the bare minimum is for us to consider running a piece of software on our infrastructure,
and we give guidance for what enables us to reliably operate that software at scale.

TODO: Should we make some ranking of what is non-negotiable and what is nice-to have?
We could mark requirements P0 through P4 or something?
