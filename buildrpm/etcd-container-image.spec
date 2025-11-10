
%global with_debug 0

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%{!?registry: %global registry container-registry.oracle.com/olcne}

%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%global _name       etcd

Name:           %{_name}-container-image
Version:        3.5.23 
Release:        1%{?dist}
Summary:        A highly-available key value store for shared configuration
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/etcd-io/etcd
Source:         %{name}-%{version}.tar.bz2
Vendor:	        Oracle America

%description
A highly-available key value store for shared configuration.

%prep
%setup -q -n %{name}-%{version}

%build
%global rpm_name %{_name}-%{version}-%{release}.%{_build_arch}
yum clean all && yumdownloader --destdir=${PWD}/rpms %{rpm_name}
%global docker_tag %{registry}/%{_name}:%{version}

docker build --squash \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_tag} -f ./olm/builds/Dockerfile .
docker save -o %{_name}.tar %{docker_tag}

%install
%__install -D -m 644 %{_name}.tar %{buildroot}/usr/local/share/olcne/%{_name}.tar


%files
%license LICENSE
/usr/local/share/olcne/%{_name}.tar

%changelog
* Tue Sep 23 2025 Olcne-Builder Jenkins <olcne-builder_us@oracle.com> - 3.5.23-1
- Added Oracle specific build files
