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

#### Publish the source code in a public Git repository.
See also the [open source chapter](open-source.md).
As for Git specifically,
our build automation has good support for Git,
a publicly hosted repository (e.g. on GitHub or Codeberg)
is easy for us to integrate.

#### Mark releases with a Git tag.

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

#### Use _annotated_ Git tags.

There are two kinds of tag in Git:
_lightweight_ tags,
and [_annotated_][annotated] tags.
Lightweight tags are a bit of a historical mistake in Git;
they do not carry metadata like the creation time and author of the tag.
Knowing the creation time of a tag is very valuable,
therefore always use annotated tags.

[annotated]: https://git-scm.com/docs/git-tag#Documentation/git-tag.txt---annotate

#### Do not — never ever — re-tag.

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
