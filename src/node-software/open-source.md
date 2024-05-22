# Open source software

At Chorus One we believe that decentralized networks have the potential
to create freedom, innovation, efficiency, and individual ownership.
Users of those networks need to be able to trust that:

 * The network does what it promises to do, without back doors, special cases,
   security vulnerabilities, or artificial limits.
 * The network can continue to operate even when its original authors are no longer around.

A prerequisite for both is that the source code for the network is publicly available.
A prerequisite for the second point
is that the source code is available under a license
that allows users to make changes if needed.
At Chorus One we therefore strive to only validate networks whose node software
is publicly released under an [OSI-approved license][osi].

[osi]: https://opensource.org/

#### Release the project under an open source license. {.p1 #publish-open-source}
Ensure that source code for the project is publicly available,
released under an [OSI-approved license][osi].
See below for how to handle [stealth launches](#stealth-launches).

## Transparent history

While access to the source code
in theory allows anybody to review it for back doors and other issues,
almost any successful software project quickly grows so large
that it is no longer feasible for a single person to review all of it.[^smart-contract]
How then, could anybody trust a large project?
Large projects don’t appear out of nowhere,
they were built over time by making many small changes,
and these changes can and should have been reviewed.

To establish trust in a large project,
it is not enough for the source code to be available,
it is important that users can verify its history,
and check how it was built and by who.
That doesn’t mean that authors need to disclose their identity
— it is possible for a pseudonymous author to establish a track record over time.
However, when there is a code dump that adds half a million lines of code in a single commit,
then it’s impossible to establish the provenance of that code,
which makes the project difficult to trust.

In addition to trust reasons,
having good source control history is simply good practice for any software project.
A good history is a valuable tool for developers,
both for debugging (e.g. with `git bisect`) and understanding the context of a piece of code
(e.g. with `git log` and `git blame`).
We as node operators occasionally have to dive into the source code of a network as well,
and access to the history is very helpful for us
to understand why a piece of code works in a certain way.

[^smart-contract]: One notable exception to this are smart contracts,
which for many reasons have to be kept deliberately small.

#### Be transparent about the provenance of your source code. {.p0 #provenance-transparency}
Even when a project is developed in stealth at first,
when the time comes to go public,
do not merely publish a source code dump
which destroys valuable metadata.
Publish the full revision control history.

#### Build in the open. {.p3 #build-in-the-open}
Building behind closed doors and periodically publishing new versions
is not technically incompatible with open source.
However,
in the true spirit of open source and crypto ethos,
developing in the open builds trust and helps to foster a community.

## Stealth launches

We understand that some teams prefer to build privately,
even if they have the intention to release all software publicly at a later stage.
When there is a clear path towards making the source code public,
we are happy to join a network at an early stage
if it is possible for us to get access to the source code.
Of course, we treat your privacy with utmost integrity,
and we can sign an NDA if needed.

## Dealing with zero-day vulnerabilities

Handling vulnerabilities in a project that is developed in the open is tricky,
because publishing the fix might draw attention to the vulnerability
before users of the software have had a chance to update.
There are two ways of handling this:

* **Pre-announce the existence of the vulnerability.**
In the announcement, include date and time at which a new version will be published.
This ensures that we can have an engineer standing by 
to act quickly at the time of the release.

* **Privately distribute a patch to node operators.**
While it is not feasible to have contact details
for all node operators in an open-membership network,
reaching a superminority of stake is often feasible.
We are happy to work with you to establish a private communication channel,
and if needed we can provide you with a way to reach
[our 24/7 oncall team](../chorus-one/oncall.md)
who are able to get back to you within minutes
(for _severe emergencies only_). 

These two options can be combined for maximum impact.

While distributing patched binaries
is a tempting way of dealing with vulnerabilities,
that approach puts node operators between a rock and a hard place:

 * We have uniform build and deployment automation that is optimized and battle-tested.
   Going through our regular process eliminates room for human error.
   If we have to deploy a binary from a different source in an ad-hoc way,
   we have to bypass protocols that are established for good reasons,
   at the risk of introducing misconfigurations.
 * We build all software from source for reasons described in
   [the build process chapter](build-process.md).
   When we are asked to run an untrusted binary blob on our infrastructure,
   we have to weigh the risk of continuing to run the vulnerable version
   against the risk of the untrusted binary being built in a way
   that is incompatible with our infrastructure,
   and the risk of the binary blob unintentionally introducing new vulnerabilities
   through e.g. a supply chain attack.
 * Although it is certainly more difficult for bad actors
   to identify the vulnerability from a binary diff than from a source code diff,
   this is only a small roadblock for somebody versed in reverse-engineering.
   Releasing patched binaries still starts a race against the clock.

Given these downsides,
we strongly urge authors to make source code available for security updates.
Patched binaries can of course still be helpful for node operators
who have less stringent requirements around what they run on their infrastructure.
This solution can be complementary,
but it’s not appropriate as the _only_ solution.

#### Ensure that node operators can build security fixes from source. {.p2 #security-fixes-source}
As described in the [build process chapter](build-process.md),
we build all software that we operate from source.
Making an exception for security fixes is a difficult trade-off that we do not make lightly.
We prefer to not have to make that trade-off.
