%define name    vpnc
%define version 0.5.1
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A free vpn client for the Cisco 3000 concentrators
License:        GPL
Group:          Networking/Other
Url:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        http://www.unix-ag.uni-kl.de/~massar/vpnc/%{name}-%{version}.tar.gz
Source2:    	%{name}.bash-completion
Requires:       iproute2
BuildRequires:  libgcrypt-devel
Provides: 	    kvpnc-backend
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
A free vpn client for cisco3000 VPN Concentrator, completly in userspace,
require Universal TUN/TAP device driver support compiled in the kernel 
or as module

%prep
%setup -q

perl -pi -e 's|/var/run/vpnc/|%{_localstatedir}/lib/%{name}/|' vpnc-script
perl -pi -e 's|/var/run/vpnc/pid|/var/run/vpnc.pid|' config.c vpnc-disconnect

%build
%make

# lower MTU, some vpn concentrators have MTU problems
perl -pi -e s/1412/1000/ vpnc-script

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man8/
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m 755 {vpnc,vpnc-script,vpnc-disconnect} %{buildroot}%{_sbindir}
install -m 755 pcf2vpnc %{buildroot}%{_bindir}
install -m 755 vpnc.8 %{buildroot}%{_mandir}/man8
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_sbindir}/vpnc-script %{buildroot}%{_sysconfdir}/%{name}/vpnc-script

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README TODO VERSION
%{_mandir}/man8/vpnc.8*
%{_sbindir}/*
%{_bindir}/*
%{_localstatedir}/lib/%{name}
%{_sysconfdir}/%{name}
%{_sysconfdir}/bash_completion.d/%{name}


