# Release engineering

As described in the [open source chapter](open-source.md),
we only run software for which the source code is available.
Communicating clearly about where to get the source code,
and when to run which version,
is part of _release engineering_.
Solid release engineering can mean the difference
between a mainnet halt and a smooth uneventful upgrade.
In this chapter we share our experience
with what makes for a smooth release process.

## Git

There exists a plethora of version control systems,
but nowadays,
the entire blockchain industry is using Git.
So far we’ve never encountered a project that we considered operating
that was not using Git,
so this guide is focused solely on Git.

#### Publish the source code in a public Git repository. {.p1 #public-git-repo}
See also the [open source chapter](open-source.md).
As for Git specifically,
our build automation has good support for Git,
a publicly hosted repository (e.g. on GitHub or Codeberg)
is easy for us to integrate.

#### Mark releases with a Git tag. {.p1 #use-git-tags}

Every Git commit points to a _tree_,
a particular revision of your source code that we could build and deploy.
To know which revision we are expected to run,
ultimately we need to know this commit.
You could announce a commit hash out of band,
for example in an announcement post.
However, this is hard to discover,
it’s hard to locate historical versions,
and there is no standard tooling for it.

Fortunately there is a standard solution.
To mark some commits as special,
Git has the concept of _tags_:
human-friendly names that point to commits.
This data is first-class,
embedded in the repository,
machine-friendly,
and has wide support from e.g. GitHub and `git tag` itself.

We have build automation that will automatically discover new tags in your repository.
When you tag your releases,
they are easy for us to integrate.
Therefore, please tag **all** commits that you expect us to run,
even if they are only for a testnet.

#### Use _annotated_ Git tags. {.p1 #use-annotated-tags}

There are two kinds of tag in Git:
_lightweight_ tags,
and [_annotated_][annotated] tags.
Lightweight tags are a bit of a historical mistake in Git;
they do not carry metadata like the creation time and author of the tag.
Knowing the creation time of a tag is very valuable,
therefore always use annotated tags.

[annotated]: https://git-scm.com/docs/git-tag#Documentation/git-tag.txt---annotate

#### Do not — never ever — re-tag. {.p1 #no-retagging}

Re-tagging
— deleting a tag, and then creating a new, _different_ tag with the same name —
creates confusion about which revision of the source code
truly corresponds to that version number.
When you re-tag,
two different parties can both think they are running v1.3.7,
but they will be running different software.
This situation is unexpected, and therefore very difficult to debug.
Sidestepping such confusion is easy:
do not re-tag, ever.
[See also the section on re-tagging in the Git manual][retag].

What if you accidentally tagged the wrong commit, and already pushed the tag?

1. **Do not delete and re-tag it.**
   We (and probably other node operators as well) have automation
   watching your repository for new tags.
   Automation can fetch bad tags faster than humans can realize that the tag is bad.
   Once published, there is no going back.
2. Create a _new_ tag, with a _different_ version number, pointing to the correct commit.
3. Announce through your regular channels that the bad version should not be used,
   and which version to use instead.
4. Do not delete the bad tag.
   Automation will have discovered it anyway.
   What is more confusing than encountering a bad tag,
   is finding the bad tag in your local checkout,
   but not being able to find any trace of it upstream.
   Instead, clarify externally that the tag should not be used,
   for example on its release page when using GitHub releases.

If this sounds like a big hassle, well, it is.
The best way to avoid this hassle is to not publish bad tags in the first place.
What helps with that is to have a standardized release process,
test it thoroughly,
and to not deviate from it.
Especially under pressure,
such as when releasing a hotfix for a critical bug,
it may be tempting to skip checks built into the process.
This is risky.
Those checks exist for a reason,
and under pressure is when humans make the most mistakes.
Sticking to an established process is often better
than trying to save a few minutes.

[retag]: https://git-scm.com/docs/git-tag#_on_re_tagging

#### When using submodules, use `https` transport urls. {.p1 #submodule-use-https-transport}
Git supports two [transfer protocols][git-transfer]: `https` and `ssh`.
On GitHub, `https` requires no authentication for public repositories,
but `ssh` by design always requires authentication,
even for public repositories.

When you as a developer clone a public repository using an `ssh://`-url,
you likely have your SSH key loaded and authentication to GitHub is transparent to you.
However, when automation such as a CI server tries to clone from an `ssh://`-url,
it typically does not have the appropriate SSH keys loaded,
and so it will fail to clone,
even if the repository is public and can be cloned from an `https://`-url.

This matters especially for submodules,
because with `git clone --recurse-submodules`,
we do not get to choose which transport to use.
The urls are determined by the `.gitmodules` file in the top-level repository.

[git-transfer]: https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols


## Release metadata

When we learn about a new release,
for example because our automation picked up a new Git tag,
we triage it:

 * Does this release apply to us at all?
   Is there a change in the software we run?
 * Is it a stable release intended for mainnet,
   or a pre-release intended for testing?
 * Do we need to update at all?
   For example, if there is a bugfix in a feature we don’t use,
   it makes no sense for us to restart our nodes and incur downtime,
   when our nodes will not be doing anything new.
 * What is the priority?
   Does this fix a critical bug that impacts the network or our operations?
   Are assets at risk if we don’t update soon?
 * Is there an associated deadline (for example, for a hard fork)?

To be able to do this triage,
it is helpful to publish this metadata together with the release.

#### Publish metadata about the release in an easily discoverable location. {.p2 #publish-release-metadata}
Examples of easily discoverable locations are the Git tag itself,
an associated release page on GitHub,
or a dedicated releases page on a website.
An example of a location that is not easily discoverable
is an invite-only Discord channel
where many kinds of announcements are being shared
in addition to just release announcements.

#### Keep a changelog. {.p3 #keep-a-changelog}
For us node operators,
the first thing we wonder when we see a new release is:
what changed, how does this affect us?
Ideally, we can find that in a changelog.

Do not mistake Git’s commit log for a changelog.
The target audience of commit messages
are the software engineers working on the project.
The target audience of a changelog are the users of the software (us, node operators).
Commit messages are typically more detailed and fine-grained
than the summary of the changes in a changelog.
While we do read through the Git log when needed,
we appreciate having a handwritten summary of the changes.

## Versioning scheme

We don’t have strong opinions on how you version your software,
but please pick one versioning scheme and stick with it.

#### Use the same number of parts in every version number. {.p2 #version-number-parts}

For example, have `v1.0.0` and `v1.0.1` in the same repository,
but do not put `v1.0` and `v1.0.1` in the same repository.
_Definitely_ do not put `v1.0` and `v1.0.0` in the same repository,
as it is confusing which one is supposed to be used.
Adding a suffix for release candidates is fine,
e.g. `v1.5.7-rc.3` and `v1.5.7` can happily coexist.

#### Use consistent suffixes to mark pre-release versions. {.p2 #consistent-suffixes}

For example, publish `v1.2.0-beta.1` and later `v1.7.0-beta.1`,
but do not switch to `v1.7.0b1` later on.

We have build automation that watches new tags.
In most cases we do not run pre-release versions,
so we exclude tags that match certain patterns from our update notifications.
If you keep changing the naming scheme,
then we have to keep adjusting our patterns.

## Timing

A big part of solid release engineering is _when_ to release a new version.
As a professional node operator we employ people,
and most of those people don’t work on weekends or holidays.
The majority of network-wide outages happen because of an update,
so you want the update to land
at a time when as many people as possible can act quickly.
While [we do have a 24/7 oncall rotation](../chorus-one/oncall.md),
their job is to deal with emergencies,
not routine updates.

#### Publish a release at least one week before an update deadline. {.p2 #publish-headroom}
When an update is mandatory and has a hard deadline
(for example, for a hard fork),
ensure that the release is ready with ample time before the deadline.
We plan most of our work on a weekly schedule.
When changes are known ahead of time it’s easy to fit them in and everything runs smoothly.
When changes come up last-minute,
it ends up being disruptive,
and deviating from standard procedures is what causes outages.

#### Do not release on Fridays. {.p2 #no-release-friday}
At least, do not ask people to update on Fridays.
Most outages happen because of a change,
and while we trust that you extensively test releases
before recommending them for mainnet,
bugs do slip in.
Our 24/7 oncall team is ready to respond in case a release contains a bug,
but they still prefer a relaxing uninterrupted weekend over dealing with an outage.

#### Do not release just before a holiday. {.p2 #no-release-holiday}
While we have an oncall team to deal with emergencies,
we are not operating at full capacity during holidays.
In case of a network-wide outage,
it will be much harder for you to reach people to coordinate an update or restart,
especially when a fraction of node operators are not professionals with a 24/7 oncall team.

Most of our engineers are based in Europe,
we observe more holidays than what is common in the US.
It is common for people in Europe to be off in the weeks of Christmas and New Year.
