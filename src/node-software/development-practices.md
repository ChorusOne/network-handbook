# Software development best practices

There are many ways to build software,
and we don’t want to force a workflow onto anybody.
However, there are some practices that are good to respect
regardless of workflow or structure.
We understand that especially for early-stage projects,
it doesn’t always make sense to follow all the best practices,
but when a mainnet launch is approaching we expect all of these to be in place.

## Basics

We mention these basics for completeness.
They should be self-evident for any project regardless of maturity level.

#### Respect licenses of upstream software. {.p0 #respect-licenses}
When including code that is not owned by you in your repository,
respect the license and clarify the origins of this code,
even when not strictly required by the license.
Even in cases where third-party code is not directly part of your repository
(e.g. dependencies pulled in through a package manager),
its license may place restrictions on derived works that you need to respect.

#### Break down changes into logical parts and write a clear commit message for each change. {.p0 #good-commits}
As we described before,
[the history of a project becomes an important asset later on][transparency],
and the history is one of the few things that you cannot fix after the fact.

[transparency]: open-source.md#transparent-history

#### Use comments to clarify non-obvious code. {.p0 #use-comments}
Any non-trivial project will contain parts that are not obvious.
Use comments to explain why a piece of code is there.
Furthermore, while temporarily commenting out pieces of code can be helpful during development,
code that is commented out should not end up merged into the main branch.

## Testing

Two types of software that are notoriously among the hardest to get right
are cryptography code and distributed systems.
Blockchain node software combines those two.
An automated testing strategy (unit tests, integration tests) is a minimum,
but given that blockchains are under more scrutiny from malicious parties
than most software,
actively hunting for bugs with e.g. fuzzers or even model checkers
is not always a nice-to-have for ensuring mainnet stability.

#### Write automated tests that are included in the repository. {.p1 #automated-tests}
There should be a way to have basic confidence in the correctness of the code.
Furthermore, when bugs are discovered through other means,
regression tests can prevent future developers from re-introducing a similar bug.

#### Write fuzz tests for code that deals with user input (network or user data). {.p2 #fuzz-tests}
If _you_ don’t write (and run) a fuzzer, a security researcher will write one,
and you’d better hope it’s a white hat when they do.
In practice, few projects have this level of testing from the start
— security is rarely a priority,
until it’s suddenly top priority because somebody is attacking your system.

## Quality assurance

#### Have a code review process. {.p1 #code-review}
For personal projects it is normal that developers write code and push it without review.
For node software written in a professional setting
with the intent of being adopted by commercial node operators,
the bar is higher:
there should be a process for reviewing changes.
Ideally that process includes a real review,
and not just a rubber stamp acknowledging that some change was made.

#### Write clear pull request, merge request, or changelist descriptions. {.p1 #write-clear-pr-descriptions}
Descriptions are useful not only for the reviewer,
also for people following along (like us as node operators),
and especially for future readers who want to understand why a change was introduced.

#### Set up continuous integration. {.p1 #continuous-integration}
Any checks that are not mechanically enforced will be violated sooner or later.

## Security

These are nice-to-haves early on in the project,
but start to become important when mainnet attracts significant value.

#### Set up a bug bounty program. {.p2 #bug-bounty-program}
You want security researchers to have a viable honest alternative
to selling or exploiting a vulnerability.

#### Set up a responsible disclosure policy. {.p2 #responsible-disclosure-policy}
Clarify to security researchers how they can report discoveries to you,
and publish this in places where security researchers tend to look,
like your website and Git repository.
