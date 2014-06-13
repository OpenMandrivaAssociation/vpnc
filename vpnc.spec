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
BuildRoot:      %{_tmppath}/%{name}-%{version}

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
%make CFLAGS="%optflags" LFLAGS="%{?ldflags}"

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


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README TODO VERSION
%{_mandir}/man8/vpnc.8*
%{_mandir}/man1/cisco-decrypt.1*
%{_sbindir}/*
%{_bindir}/*
%{_localstatedir}/lib/%{name}
%{_sysconfdir}/%{name}



%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5.3-6mdv2011.0
+ Revision: 670776
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.3-5mdv2011.0
+ Revision: 608148
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.3-4mdv2010.1
+ Revision: 524313
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.5.3-3mdv2010.0
+ Revision: 427533
- rebuild

* Tue Feb 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.3-2mdv2009.1
+ Revision: 337118
- keep bash completion in its own package

* Sun Jan 04 2009 Funda Wang <fwang@mandriva.org> 0.5.3-1mdv2009.1
+ Revision: 324529
- build with server flags
- New version 0.5.3

* Tue Sep 09 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.1-3mdv2009.0
+ Revision: 283115
- add missing cisco-decrypt binary

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.5.1-2mdv2009.0
+ Revision: 225922
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Nov 28 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.1-1mdv2008.1
+ Revision: 113769
- drop resolvconv patch, useless now
- new version

* Sun Aug 05 2007 Couriousous <couriousous@mandriva.org> 0.4.0-2mdv2008.0
+ Revision: 58993
- fix #32291

* Mon Jul 23 2007 Couriousous <couriousous@mandriva.org> 0.4.0-1mdv2008.0
+ Revision: 54777
- 0.4.0
- Rediff resolvconf patch


* Tue Jan 16 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.3-7mdv2007.0
+ Revision: 109450
- use the correct source for bash completion...

* Tue Jan 16 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.3-6mdv2007.1
+ Revision: 109433
- add bash completion
- add bash completion
- redifff resolvconf patch, and don't forget to apply it

* Fri Jan 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.3-5mdv2007.1
+ Revision: 108052
- resolvconf integration

* Fri Jan 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.3-4mdv2007.1
+ Revision: 107826
- decompress patch
- don't send password to an unknown remote script for decryption whereas it might be done locally
- Import vpnc

* Sat Oct 01 2005 Couriousous <couriousous@mandriva.org> 0.3.3-3mdk
- Add Jan Ciger patch to fix vpnc with lastest iproute ( #18940 )

* Wed May 25 2005 Couriousous <couriousous@mandriva.org> 0.3.3-2mdk
- Add vpnc-disconnect
- Fix pid file

* Sun May 15 2005 Couriousous <couriousous@mandriva.org> 0.3.3-1mdk
- 0.3.3 :
	- fix amd64
	- some fix
	- use vpnc-script instead vpnc-connect/vpnc-disconnect
	  now, to connect use "vpnc configfile" and to disconnect
	  simply send a TERM signal to vpnc process.

* Sun Jan 16 2005 Couriousous <couriousous@mandrake.org> 0.3.2-3mdk
- From Viorxus <viorxus at gmx.net>:
  - Fix disconnect script with new bash

* Sun Dec 26 2004 Couriousous <couriousous@mandrake.org> 0.3.2-2mdk
- Provide kvpnc-backend
- Better disconnection handling ( add --end-script option to vpnc )

* Mon Nov 22 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.3.2-1mdk 
- Couriousous <couriousous@zarb.org> :
 - 0.3.2

* Sun Nov 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.3.1-1mdk 
- Couriousous <couriousous@zarb.org> :
 - Patch vpnc to reset the old dns on sigterm 
 - Patch vpnc-disconnect to send sighup on disconnect
 - Set vpnc temp dns file to /var/lib/vpnc/resolv.conf
 - 0.3.1

* Wed Jul 28 2004 Götz Waschk <waschk@linux-mandrake.com> 0.2.1-5mdk
- add buildrequires

* Mon Jul 26 2004 Couriousous <couriousous@zarb.org> 0.2.1-4mdk
- Patch vpnc-{connect,disconnect} to handle the dns correctly

* Mon Jul 19 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.2.1-3mdk 
- Couriousous <couriousous@zarb.org> :
 - Use CFLAGS correctly
 - Patch vpnc-connect to load the tun module when needed

* Fri Jul 02 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.2.1-2mdk 
- dropped patch, install manually
- use /var/lib/vpnc for state files

* Sat Jun 26 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.2.1-1mdk 
- contributed by Couriousous <couriousous@sceen.net>

