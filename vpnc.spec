Summary:	A free vpn client for the Cisco 3000 concentrators
Name:		vpnc
Version:	0.5.3
Release:	27
License:	GPLv2+
Group:		Networking/Other
Url:		http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:	http://www.unix-ag.uni-kl.de/~massar/vpnc/%{name}-%{version}.tar.gz
# taken from https://gitlab.com/openconnect/vpnc-scripts
Source1:	vpnc-script
Patch0:		vpnc-0.5.3-linkage.patch
Requires:	iproute2
BuildRequires:	pkgconfig(libgcrypt)
Provides:	kvpnc-backend

%description
A free vpn client for cisco3000 VPN Concentrator, completly in userspace,
require Universal TUN/TAP device driver support compiled in the kernel 
or as module

%package pcf2vpnc
Summary:	Conversion tool for VPN-config files to vpnc-format
Group:		Networking/Other
Requires:	%{name} = %{EVRD}
Obsoletes:	%{name} < 0.5.3-25

%description pcf2vpnc
This tool converts VPN-config files from pcf to vpnc-format

%prep
%setup -q
%patch0 -p0

perl -pi -e 's|/var/run/vpnc/|%{_localstatedir}/lib/%{name}/|' vpnc-script
perl -pi -e 's|/var/run/vpnc/pid|/var/run/vpnc.pid|' config.c vpnc-disconnect

%build
%make CC=%{__cc} CFLAGS="%{optflags}" LFLAGS="%{build_ldflags}"

# lower MTU, some vpn concentrators have MTU problems
perl -pi -e s/1412/1000/ vpnc-script

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man8
install -d -m 755 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m 755 {vpnc,vpnc-disconnect,cisco-decrypt} \
    %{buildroot}%{_sbindir}
install -m 755 pcf2vpnc %{buildroot}%{_bindir}
install -m 755 vpnc.8 %{buildroot}%{_mandir}/man8
install -m 755 cisco-decrypt.1 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 755 %{SOURCE1} %{buildroot}%{_sbindir}/vpnc-script
ln -s %{_sbindir}/vpnc-script %{buildroot}%{_sysconfdir}/%{name}/vpnc-script

%files
%doc COPYING README TODO VERSION
%{_mandir}/man8/vpnc.8*
%{_mandir}/man1/cisco-decrypt.1*
%{_sbindir}/*
%{_localstatedir}/lib/%{name}
%{_sysconfdir}/%{name}

%files pcf2vpnc
%{_bindir}/pcf2vpnc
