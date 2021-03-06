# %global gitcommit_full a1cc110c8fb8ba7cae4ef4814fbdde6a13e69d3e
# %global gitcommit %(c=%{gitcommit_full}; echo ${c:0:7})
# %global gitdate 20170517

Name:           rutracker-proxy
Version:        0.2.0
Release:        1%{?dist}
Summary:        Proxy for rutracker

License:        MIT
URL:            https://github.com/zhulik/rutracker-proxy
Source0:        %{url}/archive/%{version}.tar.gz
Source1:        %{name}.service
Source2:        https://github.com/elazarl/goproxy/tarball/master#/goproxy.tar.gz
Source3:        https://github.com/golang/net/tarball/master#/net.tar.gz
Source4:        %{name}.conf
#Patch0:         %{name}-1.5-1.8build.patch

BuildRequires:  golang
BuildRequires:  go-compilers-golang-compiler
BuildRequires:  systemd

ExclusiveArch:  %{go_arches}

%description
Tool for proxying client's announces to blocked tracker servers.

%prep
%autosetup
mkdir -p src/github.com/zhulik/rutracker-proxy
mv selector src/github.com/zhulik/rutracker-proxy/

mkdir -p src/github.com/elazarl
tar -xvf %{SOURCE2}
mv elazarl-goproxy* src/github.com/elazarl/goproxy

mkdir -p src/golang.org/x/
tar -xvf %{SOURCE3}
mv golang* src/golang.org/x/net

%build
export GOPATH=$(pwd):%{gopath}
%gobuild


%install
install -p -D -m 755 %{name}-%{version} %{buildroot}%{_bindir}/%{name}
install -p -D -m 644 %{SOURCE1}  %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Wed Jul 05 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.2.0-1
- Update to 0.2.0

* Thu Jun 01 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.1.0-1
- Update to 0.1.0

* Tue May 23 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.1-0.4.20170517gita1cc110
- Added config file

* Thu May 18 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.1-0.3.20170517gita1cc110
- Update sources

* Tue May 16 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.1-0.2.20170517gitfd888d5
- Update sources and improve spec

* Tue May 16 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.1-0.1.20170517gita15e53d
- Initial packaging
