# Configuration

Node software needs configuration. We generally run multiple nodes, with similar
but slightly different configuration.

#### Use a configuration file. {.p3 #config-file}
We don’t have a very strong opinion on how to configure software.
Command-line flags, [environment variables][12factor],
or a configuration file are all fine.
However, we found that as software matures and grows more complex,
it needs more configuration options,
and putting everything on the command line can become unwieldy.
Furthermore,
in command-line arguments and environment variables,
everything is a string,
while configuration files enable more structured data.
We recommend using [TOML][toml] over YAML,
as TOML contains fewer footguns and implementation ambiguities.

[12factor]: https://12factor.net/config
[toml]:     https://toml.io/en/

#### Do not embed private keys in a configuration file. {.p1 #keys-not-in-config}
We do not treat configuration as sensitive data.
Configuration is internal,
we don’t expose it to the Internet,
but operators don’t expect configuration to contain sensitive secrets
such as private keys.
We store configuration unencrypted in internal Git repositories,
and we write configuration files to disk.
For private keys and other secrets,
those we store in Hashicorp Vault,
and we never write them unencrypted to persistent storage.
(If your node software loads keys from a file,
we put them on a ramdisk.)
To configure private keys,
either read them from a file at a configurable location,
or load them from an environment variable.

#### Ensure data directories are configurable. {.p1 #datadir-configurable}
We work with machines that have multiple disks,
with multiple filesystems.
If you store files in hard-coded places,
or if you accidentally write to undocumented directories
(such as a hidden directory in `HOME`),
that makes it harder for us to ensure that IO hits the right disk,
and to back up and replicate all relevant data.
Prefer to only write inside one directory,
and make that directory configurable explicitly.
