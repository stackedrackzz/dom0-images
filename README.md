# dom0-images

`qubes-builderv2` configuration and a podman-based build container for
producing Qubes OS ISOs, templates, and components.

**Status: general infrastructure scaffold.** `builder.yml`'s `components`/
`templates` lists are placeholders -- the actual guest VM templates/components
to build are specified separately; extend `builder.yml` once they are.

**`builder.yml` is a best-effort reconstruction**, not verified against a live
checkout of https://github.com/QubesOS/qubes-builderv2 (no internet access
from the environment this was written in). Diff it against that project's own
`example-configs/` for the Qubes release you're targeting before relying on it
for a real build.

## Layout

- `builder.yml` -- qubes-builderv2 config. `executor: type: podman` sandboxes
  each component's build in its own container, against the podman socket
  mounted into `build-container/` (see below) -- not a nested/self-hosted
  podman, the *host's* real one.
- `build-container/Containerfile` -- the outer container that runs `qb`
  itself. Does **not** install podman -- that's a host-level requirement
  (`packaging/dom0-images.spec`'s `Requires: podman`), not something this
  image bundles; the container reaches the host's podman exclusively through
  the mounted socket.
- `podman-compose.yml` -- not a long-running stack; `builder` is meant to be
  invoked per-command, not brought up with `up -d`.
- `artifacts/`, `cache/` -- qubes-builderv2's own output/cache dirs, mounted
  into the container.
- `packaging/dom0-images.spec` -- RPM spec, built with `mock` (same pipeline
  as this project's other packages). Installs everything under
  `/usr/share/dom0-images/` as a plain data package -- it does not start or
  run anything itself.

## Usage

```sh
cd dom0-images
podman-compose run --rm builder -c builder.yml package fetch
podman-compose run --rm builder -c builder.yml package build
podman-compose run --rm builder -c builder.yml package build-iso
```

(Subcommands above are qubes-builderv2's own, per its `qb --help` --
unverified against a live checkout for the same reason as `builder.yml`
itself.)

`PODMAN_SOCKET` in `podman-compose.yml` defaults to
`/run/user/1000/podman/podman.sock` (rootless); override it in the
environment if the actual UID or socket path differs, or if this needs to run
against a rootful podman instead.

## Known gaps

- `conf/iso-online-testing.ks` (referenced by `builder.yml`'s `iso.kickstart`)
  does not exist yet -- an ISO kickstart is specific enough to the actual
  target release/templates that it wasn't worth fabricating a placeholder
  before those are specified. `conf/` exists as an empty directory for it.
- No signing key configured (`sign-key: {}` in `builder.yml`) -- builds are
  unsigned/local-only until one is provided.
- Whether `qb`'s podman executor shells out to a `podman` CLI binary or talks
  to the socket directly (e.g. via podman-py) is unverified -- if the former,
  the container needs that binary bind-mounted in from the host too (it isn't
  currently), since it isn't installed in the image on purpose.
- Nothing in this repo has been run against a real build yet -- no ISO, no
  template, nothing has actually been produced. This is infrastructure only.
