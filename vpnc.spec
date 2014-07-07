%define name    vpnc
%define version 0.5.3
%define release 16

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A free vpn client for the Cisco 3000 concentrators
License:        GPLv2+
Group:          Networking/Other
Url:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        http://www.unix-ag.uni-kl.de/~massar/vpnc/%{name}-%{version}.tar.gz
Patch0:		vpnc-0.5.3-linkage.patch
Requires:       iproute2
BuildRequires:  libgcrypt-devel
Provides: 	    kvpnc-backend

%description
A free vpn client for cisco3000 VPN Concentrator, completly in userspace,
require Universal TUN/TAP device driver support compiled in the kernel 
or as module

%prep
%setup -q
%patch0 -p0

perl -pi -e 's|/var/run/vpnc/|%{_localstatedir}/lib/%{name}/|' vpnc-script
perl -pi -e 's|/var/run/vpnc/pid|/var/run/vpnc.pid|' config.c vpnc-disconnect

%build
%serverbuild
%make CC=%{__cc} CFLAGS="%optflags" LFLAGS="%{?ldflags}"

# lower MTU, some vpn concentrators have MTU problems
perl -pi -e s/1412/1000/ vpnc-script

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man8
install -d -m 755 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m 755 {vpnc,vpnc-script,vpnc-disconnect,cisco-decrypt} \
    %{buildroot}%{_sbindir}
install -m 755 pcf2vpnc %{buildroot}%{_bindir}
install -m 755 vpnc.8 %{buildroot}%{_mandir}/man8
install -m 755 cisco-decrypt.1 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_sbindir}/vpnc-script %{buildroot}%{_sysconfdir}/%{name}/vpnc-script

%files
%doc COPYING README TODO VERSION
%{_mandir}/man8/vpnc.8*
%{_mandir}/man1/cisco-decrypt.1*
%{_sbindir}/*
%{_bindir}/*
%{_localstatedir}/lib/%{name}
%{_sysconfdir}/%{name}
