%define name    vpnc
%define version 0.3.3
%define release %mkrel 7

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A free vpn client for the Cisco 3000 concentrators
Source0:        %{name}-%{version}.tar.bz2
Source1:        http://www.unix-ag.uni-kl.de/~massar/soft/cisco-decrypt.c
Source2:    	%{name}.bash-completion
Patch0:		    vpnc-0.3.3-iproute.patch
Patch1:		    vpnc-0.3.3-localdecrypt.patch
Patch2:		    vpnc-0.3.3-resolvconf.patch
License:        GPL
Group:          Networking/Other
Url:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Requires:       iproute2
Requires:       initscripts >= 8.48-4mdv2007.1
BuildRequires:  libgcrypt-devel
Provides: 	    kvpnc-backend
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
A free vpn client for cisco3000 VPN Concentrator, completly in userspace,
require Universal TUN/TAP device driver support compiled in the kernel 
or as module

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
cp %{SOURCE1} cisco-decrypt.c

perl -pi -e 's|/var/run/vpnc/|%{_localstatedir}/%{name}/|' vpnc-script
perl -pi -e 's|/var/run/vpnc/pid|/var/run/vpnc.pid|' config.c vpnc-disconnect
perl -pi -e 's|CFLAGS=|CFLAGS+=|' Makefile

%build
export CFLAGS="%{optflags}"
%make
gcc -o cisco-decrypt cisco-decrypt.c $(libgcrypt-config --libs --cflags)

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man8/
install -d -m 755 %{buildroot}%{_localstatedir}/%{name}
install -m 755 {vpnc,vpnc-script,vpnc-disconnect} %{buildroot}%{_sbindir}
install -m 755 {pcf2vpnc,cisco-decrypt} %{buildroot}%{_bindir}
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
%{_localstatedir}/%{name}
%{_sysconfdir}/%{name}
%{_sysconfdir}/bash_completion.d/%{name}


