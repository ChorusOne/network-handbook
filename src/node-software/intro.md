# Node Software Guide

With more than half a decade of experience operating more than 50 blockchain networks,
we’ve noticed some patterns that make a network easy to operate reliably,
and also some pitfalls that less mature networks might not be aware of.
In this section we describe what from our point of view is the ideal way
to build a blockchain network that can be operated reliably.
By sharing our perspective,
we aim to help networks build better software and more stable mainnets.

TODO: Should we make some ranking of what is non-negotiable and what is nice-to have?
We could mark requirements P0 through P4 or something?

## Classification

Throughout this guide we classify our best practices from P0 to P3,
ranging from essential to nice to have.
We use this classification internally as a guiding principle
to decide whether a network is suitable to onboard.
We take context into account when we work with new networks to onboard,
and we understand that no network can respect all recommendations from day one.
However,
when a network fails too many of our recommendations,
the operational overhead will likely outweigh the financial benefit
of becoming a node operator on that network.

#### Essential { .p0 }

An _essential_ practice is something we expect from a network
regardless of maturity level.
These should be addressed as soon as possible
by any network that aims to one day launch a mainnet.

#### Important { .p1 }

An _important_ practice is something we expect from a network
that is launching a public testnet.
Implementing these recommendations signals readiness
to engage with a wider group of node operators,
and will ensure a smooth testnet.

#### Recommended { .p2 }

A _recommended_ practice is something that we expect a network to implement
before or shortly after launching a public mainnet.
These become important at a maturity level
where mistakes start to have serious financial consequences.

#### Desirable { .p3 }

A _desirable_ practice is something that makes our life as a node operator easier,
but which is not otherwise essential.
We understand that node software authors
sometimes have more important issues to tackle than making node operators happy.
Projects that implement our P3 recommendations are exemplary,
and set the benchmark for other projects to strive for.
