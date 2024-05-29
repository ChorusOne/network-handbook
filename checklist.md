# Checklist

This checklist summarizes the recommendations in all the chapters.
The main purpose of this page is to have a markdown checklist that
we can copy into an issue for internal due diligence processes. It
is not part of the book itself. Rebuild with `export_checklist.py`.

## P0

#### Software development best practices
 - [ ] [Respect licenses of upstream software.](https://handbook.chorus.one/node-software/development-practices.html#respect-licenses)
 - [ ] [Break down changes into logical parts and write a clear commit message for each change.](https://handbook.chorus.one/node-software/development-practices.html#good-commits)
 - [ ] [Use comments to clarify non-obvious code.](https://handbook.chorus.one/node-software/development-practices.html#use-comments)

#### Open source software
 - [ ] [Be transparent about the provenance of your source code.](https://handbook.chorus.one/node-software/open-source.html#provenance-transparency)

## P1

#### Release engineering
 - [ ] [Publish the source code in a public Git repository.](https://handbook.chorus.one/node-software/release-engineering.html#public-git-repo)
 - [ ] [Mark releases with a Git tag.](https://handbook.chorus.one/node-software/release-engineering.html#use-git-tags)
 - [ ] [Use _annotated_ Git tags.](https://handbook.chorus.one/node-software/release-engineering.html#use-annotated-tags)
 - [ ] [Do not — never ever — re-tag.](https://handbook.chorus.one/node-software/release-engineering.html#no-retagging)
 - [ ] [When using submodules, use `https` transport urls.](https://handbook.chorus.one/node-software/release-engineering.html#submodule-use-https-transport)

#### Software development best practices
 - [ ] [Write automated tests that are included in the repository.](https://handbook.chorus.one/node-software/development-practices.html#automated-tests)
 - [ ] [Have a code review process.](https://handbook.chorus.one/node-software/development-practices.html#code-review)
 - [ ] [Write clear pull request, merge request, or changelist descriptions.](https://handbook.chorus.one/node-software/development-practices.html#write-clear-pr-descriptions)
 - [ ] [Set up continuous integration.](https://handbook.chorus.one/node-software/development-practices.html#continuous-integration)

#### Open source software
 - [ ] [Release the project under an open source license.](https://handbook.chorus.one/node-software/open-source.html#publish-open-source)

#### Monitoring
 - [ ] [Expose Prometheus metrics.](https://handbook.chorus.one/node-software/monitoring.html#expose-prometheus-metrics)
 - [ ] [Expose metrics privately.](https://handbook.chorus.one/node-software/monitoring.html#expose-metrics-privately)

#### Build process
 - [ ] [Ensure your software can be built on a stock Ubuntu LTS installation.](https://handbook.chorus.one/node-software/build-process.html#builds-on-ubuntu)
 - [ ] [Don’t require Docker as part of your build process.](https://handbook.chorus.one/node-software/build-process.html#no-docker)
 - [ ] [Don’t fetch untrusted binaries from the Internet as part of your build scripts.](https://handbook.chorus.one/node-software/build-process.html#no-fetch-untrusted-binaries)
 - [ ] [Include a `rust-toolchain.toml` file in your repository.](https://handbook.chorus.one/node-software/build-process.html#use-rust-toolchain)

## P2

#### Release engineering
 - [ ] [Publish metadata about the release in an easily discoverable location.](https://handbook.chorus.one/node-software/release-engineering.html#publish-release-metadata)
 - [ ] [Use the same number of parts in every version number.](https://handbook.chorus.one/node-software/release-engineering.html#version-number-parts)
 - [ ] [Use consistent suffixes to mark pre-release versions.](https://handbook.chorus.one/node-software/release-engineering.html#consistent-suffixes)
 - [ ] [Publish a release at least one week before an update deadline.](https://handbook.chorus.one/node-software/release-engineering.html#publish-headroom)
 - [ ] [Do not release on Fridays.](https://handbook.chorus.one/node-software/release-engineering.html#no-release-friday)
 - [ ] [Do not release just before a holiday.](https://handbook.chorus.one/node-software/release-engineering.html#no-release-holiday)

#### Software development best practices
 - [ ] [Write fuzz tests for code that deals with user input (network or user data).](https://handbook.chorus.one/node-software/development-practices.html#fuzz-tests)
 - [ ] [Set up a bug bounty program.](https://handbook.chorus.one/node-software/development-practices.html#bug-bounty-program)
 - [ ] [Set up a responsible disclosure policy.](https://handbook.chorus.one/node-software/development-practices.html#responsible-disclosure-policy)

#### Open source software
 - [ ] [Ensure that node operators can build security fixes from source.](https://handbook.chorus.one/node-software/open-source.html#security-fixes-source)

#### Monitoring
 - [ ] [Ensure telemetry can be disabled.](https://handbook.chorus.one/node-software/monitoring.html#telemetry-can-be-disabled)

## P3

#### Release engineering
 - [ ] [Keep a changelog.](https://handbook.chorus.one/node-software/release-engineering.html#keep-a-changelog)

#### Open source software
 - [ ] [Build in the open.](https://handbook.chorus.one/node-software/open-source.html#build-in-the-open)

#### Monitoring
 - [ ] [Respect Prometheus metric and label naming standards.](https://handbook.chorus.one/node-software/monitoring.html#respect-prometheus-standards)

