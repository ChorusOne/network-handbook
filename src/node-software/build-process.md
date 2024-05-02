# Build process

At Chorus One we strongly prefer to build all node software that we operate from source.
We generally do not run prebuilt binaries or upstream container images.
We do this for multiple reasons:

* **Transparency.**
As described in [the open source chapter](open-source.md),
access to the source code is a prerequisite for users and node operators
to be able to trust the network.
However, just access to the source code is meaningless
when everybody runs pre-built binaries.
How do we know that the source code is really the source code
for the software that’s running in practice?
The easiest way to be sure, is to build it from that source code.

* **Security.**
Most node software we operate is written by reputable parties,
and the risk that they are actively trying to hide malware in binary releases is low.
However, as organizations grow, insider risk grows with it.
Furthermore, when we don’t have full control over the build environment and build process,
we cannot rule out supply chain attacks that might be trying to mess with the build process.
The recent [liblzma backdoor][xzgate] (CVE-2024-3094) illustrates
that supply chain attacks are a real concern,
and with the upwards trend in number of dependencies
(thousands of dependencies is now commonplace for Rust projects),
we cannot just dismiss this as a hypothetical risk.

* **Performance.**
For performance-oriented chains,
we compile software with the compiler optimization flags
tuned for the specific CPU microarchitecture that we deploy the software on.

[xzgate]: https://www.openwall.com/lists/oss-security/2024/03/29/4

Aside from [access to the source code](open-source.md)
and a working build process,
we don’t have strict requirements on how to set up your build.
The more standard a build process is
(e.g. `cargo build` after a clone just works),
the easier it is for us to integrate,
but if the build process is well-documented,
we can usually find a way to make it work.
Still, there are some trends that we can use to give general recommendations.

In general, software written in Go or Rust is easy for us to build.
C/C++ are usually acceptable too.
Javascript is generally impossible to package except as a container image,
and impossible to secure due to an ecosystem where depending on tens of thousands of microlibraries is commonplace.

## General recommendations

#### Ensure your software can be built on a stock Ubuntu LTS installation.

Ubuntu Linux is the common denominator that is supported by almost any software project.
[We run Ubuntu LTS][c1-ubuntu] on our servers to minimize surprises specific to our setup,
and for consistency,
we also prefer to use it as the base image for applications deployed in containers.

[c1-ubuntu]: /chorus-one/the-hardware-layer.html#operating-system

#### Don’t require Docker as part of your build process.
While Docker is convenient for less experienced users,
depending on external images has the same security implications as downloading untrusted binary blobs,
and therefore we cannot allow this.
When your official build process involves Docker,
this forces us to reverse-engineer your Dockerfile,
and if our build process deviates too much from yours,
it’s more likely to break.
It is of course fine if you offer official pre-built container images
for node operators who have less stringent security practices.
You can achieve that by running your regular build process inside a Dockerfile.

#### Don’t fetch untrusted binaries from the Internet as part of your build scripts.
Aside from security implications,
flaky third-party webservers are a common source of failing builds.
These types of flakes are rare enough
that it’s difficult to get the time-outs and retries right,
but at scale are common enough to be a nuisance.
Language package managers and system package managers
that download from official registries are of course fine.

## Golang recommendations

#### Include a `go.mod` file that specifies which version of the Go toolchain your project should be built with.
TODO.

## Rust recommendations

#### Include a `rust-toolchain.toml` file in your repository.
The official standard way to encode which Rust toolchain to use,
in a machine-readable form that is automatically picked up by `rustup`,
is to specify the version in a [`rust-toolchain.toml`][rust-toolchain] file.

Rust is evolving rapidly,
and code that was tested with one version of the Rust toolchain
often does not compile with an older toolchain.
Furthermore,
we have seen cases where the code compiled fine,
but the binary behaved differently depending on the compiler version,
leading to segfaults.

Projects that include a `rust-toolchain.toml`
are easy for us to integrate with our build automation.
When you specify the version in a non-standard location
(for instance, as part of configuration of some CI workflow),
we have to write custom scripts to extract it from there,
which is more fragile,
and duplicating a feature that `rustup` already does perfectly well.
When you don’t specify a version as part of the repository at all,
we have to guess,
and it will be harder for people in the future to build older releases of your software,
because they will not know what toolchain to use.

[rust-toolchain]: https://rust-lang.github.io/rustup/overrides.html#the-toolchain-file
