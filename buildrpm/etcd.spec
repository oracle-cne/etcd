
%if 0%{?fedora}
%global with_devel 0
%global with_bundled 1
%global with_debug 1
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%endif

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# etcd release version major.minor

%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com

%global system_name		etcd

Name:		etcd
Version:	3.6.7	
Release:	1%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
Group:		System/Management
URL:		https://github.com/coreos/etcd
Vendor:		Oracle America
Source0:        etcd-%{version}.tar.bz2
Patch0:         build_lib.sh.patch

BuildRequires:  	golang
BuildRequires:  	libpcap-devel
BuildRequires:		systemd
Requires(pre):		shadow-utils
Requires(post): 	systemd
Requires(preun): 	systemd
Requires(postun): 	systemd

%description
A highly-available key value store for shared configuration.

%package -n %{system_name}-docker-image
Summary: etcd docker image for Oracle Linux

%description -n %{system_name}-docker-image
etcd docker image for Oracle Linux

%prep
%setup -q -n %{name}-%{version}
%patch0

%build
unset GOPROXY
go version
export ETCD_SETUP_GOPATH=1
GOENV_GOARCH=$(go env | grep GOARCH | sed 's/"//g' | tr -d "'")
export ${GOENV_GOARCH}
echo $GOARCH
GO_BUILD_FLAGS="-X main.VERSION=v%{version}" scripts/build.sh

%install
install -D -p -m 0755 bin/%{system_name} %{buildroot}%{_bindir}/%{system_name}
install -D -p -m 0755 bin/%{system_name}ctl %{buildroot}%{_bindir}/%{system_name}ctl
install -D -p -m 0755 bin/%{system_name}ctl %{buildroot}%{_bindir}/%{system_name}utl

# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{system_name}

%files
%license LICENSE THIRD_PARTY_LICENSES.txt
%{_bindir}/%{system_name}
%{_bindir}/%{system_name}ctl
%{_bindir}/%{system_name}utl

%changelog
* Wed Dec 17 2025 Oracle Cloud Native Environment Authors <noreply@oracle.com> - 3.6.7-1
- Added Oracle specific build files
