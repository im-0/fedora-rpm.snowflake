# TODO: Enable debuginfo (disabled for f35).
%global debug_package %{nil}

Name:       snowflake
Version:    2.11.0
Release:    1%{?dist}
Summary:    Pluggable Transport for Tor using WebRTC, inspired by Flashproxy

License:    BSD
URL:        https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/snowflake/
Source0:    https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/snowflake/-/archive/v%{version}/%{name}-v%{version}.tar.gz

# $ GOPROXY=https://proxy.golang.org go mod vendor -v
# Contains snowflake-v%{version}/vendor/*.
Source1:    %{name}-v%{version}.go-mod-vendor.tar.xz

Patch0:     shuffle-curves.patch

BuildRequires:  golang >= 1.17


%description
Pluggable Transport for Tor using WebRTC, inspired by Flashproxy.


# TODO: Build and package other binaries.
%package client
Summary: Pluggable Transport for Tor using WebRTC (client)


%description client
Pluggable Transport for Tor (client) using WebRTC, inspired by Flashproxy.


%package server
Summary: Pluggable Transport for Tor using WebRTC (server)


%description server
Pluggable Transport for Tor (server) using WebRTC, inspired by Flashproxy.


%prep
%setup -q -D -T -b0 -n %{name}-v%{version}
%setup -q -D -T -b1 -n %{name}-v%{version}

%patch -P 0 -p1


%build
export GO111MODULE="on"
export CGO_ENABLED=0

BUILD_ID=$(head -c20 /dev/urandom | od -An -tx1 | tr -d ' \n')

cd ./client/
go build -mod=vendor -v \
        -ldflags "-B 0x${BUILD_ID}"
cd ..

cd ./server/
go build -mod=vendor -v \
        -ldflags "-B 0x${BUILD_ID}"
cd ..


%install
mkdir -p %{buildroot}/%{_bindir}

mv client/client %{buildroot}/%{_bindir}/snowflake-client
mv server/server %{buildroot}/%{_bindir}/snowflake-server


%files client
%{_bindir}/snowflake-client


%files server
%{_bindir}/snowflake-server


%changelog
* Fri Mar 28 2025 Ivan Mironov <mironov.ivan@gmail.com> - 2.11.0-1
- Update to v2.11.0

* Fri Mar 22 2024 Ivan Mironov <mironov.ivan@gmail.com> - 2.9.2-1
- Update to v2.9.2

* Mon Sep 25 2023 Ivan Mironov <mironov.ivan@gmail.com> - 2.6.1-1
- Update to v2.6.1

* Thu Mar 30 2022 Ivan Mironov <mironov.ivan@gmail.com> - 2.5.1-1
- Update to v2.5.1

* Wed Dec 07 2022 Ivan Mironov <mironov.ivan@gmail.com> - 2.4.1-1
- Update to v2.4.1

* Wed Jun 29 2022 Ivan Mironov <mironov.ivan@gmail.com> - 2.3.0-1
- Update to v2.3.0
- https://github.com/pion/dtls/pull/474

* Thu Jun 23 2022 Ivan Mironov <mironov.ivan@gmail.com> - 2.2.0-1
- Update to v2.2.0

* Fri May 13 2022 Ivan Mironov <mironov.ivan@gmail.com> - 2.1.0-1
- Initial packaging
