Name:           dom0-images
Version:        0.1.0
Release:        1%{?dist}
Summary:        qubes-builderv2 config + podman stack for building Qubes ISOs/templates
License:        MIT
URL:            https://example.invalid/dom0-images
BuildArch:      noarch

Source0:        %{name}-%{version}.tar.gz

Requires:       podman >= 5.0
Requires:       podman-compose
Requires:       git

%description
Lays down a qubes-builderv2 (https://github.com/QubesOS/qubes-builderv2)
configuration (builder.yml) and a podman-compose stack
(build-container/, podman-compose.yml) that runs `qb` itself in a
container, driving qubes-builderv2's own per-component podman executor
against the host's podman via a mounted socket -- podman is a host
requirement (see Requires above), not something this package or its
container image bundles.

builder.yml's components/templates lists are placeholders: this
package only provides the general build infrastructure. Actual guest
VM templates/components to build are specified separately -- extend
builder.yml once they are, rather than restructuring it.

builder.yml itself is a best-effort reconstruction of qubes-builderv2's
schema from training knowledge, not verified against a live checkout --
see the warning comment at its top. Diff it against
qubes-builderv2's own example-configs/ before relying on it for a real
build.

This package only installs files under %{_datadir}/%{name}/ -- it does
not start or run anything itself. See README.md in that directory for
usage.

%prep
%setup -q

%build
# nothing to compile

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a . %{buildroot}%{_datadir}/%{name}/
rm -rf %{buildroot}%{_datadir}/%{name}/packaging
rm -rf %{buildroot}%{_datadir}/%{name}/artifacts
rm -rf %{buildroot}%{_datadir}/%{name}/cache
mkdir -p %{buildroot}%{_datadir}/%{name}/artifacts
mkdir -p %{buildroot}%{_datadir}/%{name}/cache

%files
%{_datadir}/%{name}/

%changelog
* Wed Jul 29 2026 stackedrackzz <noreply@users.noreply.github.com> - 0.1.0-1
- Initial packaging: builder.yml + podman-compose build container
  scaffold. Placeholders pending actual guest VM template/component
  specification.
