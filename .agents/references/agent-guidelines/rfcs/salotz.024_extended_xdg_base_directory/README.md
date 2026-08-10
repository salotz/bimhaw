# Extended XDG Base Directory Specification

- nexp :: `salotz.024_extended_xdg_base_directory`
- long name :: Extended XDG Base Directory Specification
- executive summary :: This RFC extends the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir/latest/) with additional user-local directories and environment variables (prefixed `XDGX_`) for common use cases not covered by the base spec. It defines `~/.local/opt` (or `XDGX_OPT_HOME`) for ad-hoc user-managed software installs, `~/.local/tmp` (`XDGX_TMP_HOME`) as a user-local temporary directory distinct from the system `/tmp`, `~/.local/scratch` (`XDGX_SCRATCH_HOME`) for ephemeral batch-process scratch space, and `~/.local/var` for variable/persistent data akin to the FHS `/var`. Includes recommendations for snapshotting, cleanup policies, and usage to improve system organization, backup strategies, and performance.

This RFC adds some minor extensions to the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir/latest/) to cover a wider variety of use cases.

## XDG Specification Summary

The XDG Base Directory Specification covers the definition of the
following (not a complete description):

- `XDG_DATA_HOME` -> `~/.local/share`
- `XDG_CONFIG_HOME` -> `~/.config`
- `XDG_CACHE_HOME` -> `~/.cache`

Additionally the `~/.local/bin` is specified as the location of user
installed executables and is expected to be on `$PATH`.

In no case does this RFC diverge from this specification. Instead we
add some more expected behaviors, environment variables, and defaults
for additional kinds of data.

For environment variables we prefix them with `XDGX_` to distinguish
them but also have them show up in common queries like `env | grep XDG`.

## Extensions

### opt

In the root directory the `/opt` directory is commonly used for the
installation of software not managed by the system package manager.

For a user's home they may use user managed software with various
package managers (that should obey the XDG specification for packages
and caching).

However, there is another class of software installations which don't
fit into package managers and are completely ad hoc. For instance a
project may only support direct downloads or require compilation.

For user managed software installations of this style the
`~/.local/opt` folder should be used by default.

This can be overridden with the environment variable `XDGX_OPT_HOME`.

The structure of this directory is left completely unspecified and is
up to the user to manage.

If executables in this folder should be on `$PATH` they should be
copied or symlinked into `~/.local/bin`, rather than paths to
`~/.local/opt` on `$PATH`.

#### Recommendations

When setting up system partitions we recommend snapshotting this directory.

### tmp

The root directory `/tmp` is used for temporary files used in programs.

This RFC introduces a user-local equivalent to this temporary
directory under `~/.local/tmp` by default.

Overridden by the environment variable `XDGX_TMP_HOME`.

This does not affect other ad hoc standards like `TMPDIR` etc. which
specify to programs which temporary directory to use.

The reason for this distinction is that the system managed `/tmp` is
necessarily used for system processes. These processes can influence
system performance and stability. On many systems this is a RAMFS
partition which improves speed.

#### Recommendations

It is not recommended to snapshot the tmp directory.

This directory is suitable for user spawned long-running processes. Applications should manage their own files here and short lived processes should be responsible for cleanup before exit.

This directory can be cleared on every new boot up, since services will need to reinstantiate data here in any case on reboot.

### scratch

There is no equivalent standard to generic UNIX-like systems for scratch space. However, it is a common pattern in batch oriented computing to have one or more directories available to batch processes to write ephemeral data during execution.

This is typically called a "scratch space" and can be node-local (for high latency) or not.

There can be multiple scratch directories for processes that have different filesystem requirements as well. (e.g. node-local NVME and parallel filesystems).

In a standard UNIX-like system the `/tmp` is often used for this use case, which is unsatisfactory for the same reasons elaborated in the [tmp](#tmp) standard.

What distinguishes scratch from tmp, is that scratch is solely for the use of ephemeral data of short-lived batch processes.

Applications like software test suites, for which this data may be useful for post-mortem examination, but is typically cleaned up with tear-down fixtures after generation.

This RFC introduces the `~/.local/scratch` directory for this use case and the overriding environment variable `XDGX_SCRATCH_HOME`.

For multiple filesystems mounted for different scratch purposes use subdirectories of this directory.

#### Recommendations

It is not recommended to snapshot the scratch directory.

This directory is suitable for batch processes, not suitable for long running processes.

All files can be deleted at any time and it is recommended to have scheduled cleanups during batch downtimes.

This directory can be cleaned on system reboot.
