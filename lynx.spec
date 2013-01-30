%define versio_ %(echo %version |sed -e 's,\\\.,-,g')
#define subver pre.4

Summary:	Text based browser for the world wide web
Name:		lynx
Version:	2.8.7
Release:	7
License:	GPL
URL:		http://lynx.isc.org
Group:		Networking/WWW
BuildRequires:	gettext
BuildRequires:	openssl-devel
BuildRequires:	ncurses-devel
Source0:	http://lynx.isc.org/current/%name%{version}.tar.bz2
Patch0:		lynx2-8-7-adapt-to-modern-file-localizations.patch
Patch1:		lynx2-8-7-default-config.patch
Patch2:		lynx2-8-6-fix-ugly-color.patch
Patch10:	lynx2-8-7-tmp_dir.patch
Patch11:	lynx2-8-6-don-t-accept-command-line-args-to-telnet.patch
Patch13:	lynx2-8-6-format_not_a_string_literal_and_no_format_arguments.diff
Provides:	webclient lynx-ssl
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel 
BuildRequires:  pkgconfig(ncursesw)
Obsoletes:	lynx-ssl < %EVRD

%description
This a terminal based WWW browser. While it does not make any attempt
at displaying graphics, it has good support for HTML text formatting,
forms, and tables.

This version includes support for SSL encryption.

WARNING: In some countries, it is illegal to export this package. In some
countries, it may even be illegal to use it.


%prep
%setup  -q -n %{name}%{versio_}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch10 -p1
%patch11 -p1
%patch13 -p0 -b .format_not_a_string_literal_and_no_format_arguments
perl -pi -e 's,^#LOCALE_CHARSET:.*,LOCALE_CHARSET:TRUE,' lynx.cfg

%build

debian_options=`cat << DEBIAN
	--enable-warnings
	--enable-8bit-toupper
	--enable-externs
	--enable-cgi-links
	--enable-persistent-cookies --enable-nls
	--enable-prettysrc --enable-source-cache
	--enable-charset-choice
	--enable-default-colors
	--enable-ipv6
	--enable-nested-tables --enable-read-eta
	--with-zlib
DEBIAN`
# removed --enable-exec-links --enable-exec-scripts,
# it goes together with LOCAL_EXECUTION_LINKS_* in lynx.cfg


redhat_options=`cat << REDHAT
	--with-screen=ncursesw 
	--enable-internal-links
	--enable-libjs
	--enable-scrollbar
	--enable-file-upload
	--enable-locale-charset
	--with-ssl
	--enable-addrlist-page
	--enable-justify-elts
REDHAT`

other_options=`cat << OTHER
	--enable-color-style
	--enable-nsl-fork
OTHER`

# (cf INSTALLATION file for more about the options)
# --with-included-gettext  is the default
# --enable-kbd-layout not useful enough
# --enable-cjk not needed for CJK and may go away in a future release

CFLAGS="$RPM_OPT_FLAGS -I/usr/include/openssl" \
%configure --libdir=/usr/share/lynx $debian_options $redhat_options $other_options
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std install-help

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat >$RPM_BUILD_ROOT%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang lynx

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- lynx < 2.8.5-0.13mdk.dev.12
# handle lynx.cfg move from /etc to /usr/share/lynx
if [ -e %{_sysconfdir}/lynx.cfg.rpmsave ]; then
  echo "migrating saved %{_sysconfdir}/lynx.cfg.rpmsave to %{_datadir}/lynx/lynx.cfg"
  mv -f %{_datadir}/lynx/lynx.cfg %{_datadir}/lynx/lynx.cfg.rpmnew
  mv -f %{_sysconfdir}/lynx.cfg.rpmsave %{_datadir}/lynx/lynx.cfg
fi

%files -f lynx.lang
%defattr(-,root,root)
%doc README
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg
%config(noreplace) %{_sysconfdir}/lynx.cfg
%config(noreplace) %{_sysconfdir}/lynx.lss
%{_mandir}/*/*
%{_bindir}/*
%{_datadir}/lynx_help




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.8.7-5mdv2011.0
+ Revision: 666114
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.7-4mdv2011.0
+ Revision: 606451
- rebuild

* Mon Apr 05 2010 Eugeni Dodonov <eugeni@mandriva.com> 2.8.7-3mdv2010.1
+ Revision: 531867
- Rebuild for openssl 1.0.0.

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.7-2mdv2010.1
+ Revision: 511591
- rebuilt against openssl-0.9.8m

* Sun Jan 03 2010 Funda Wang <fwang@mandriva.org> 2.8.7-1mdv2010.1
+ Revision: 485949
- rediff tmp_dir patch
- new version 2.8.7

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.8.6-5mdv2010.0
+ Revision: 426021
- rebuild

* Sun Dec 21 2008 Oden Eriksson <oeriksson@mandriva.com> 2.8.6-4mdv2009.1
+ Revision: 317055
- fix build with -Werror=format-security (P13)

* Thu Oct 30 2008 Pixel <pixel@mandriva.com> 2.8.6-3mdv2009.1
+ Revision: 298758
- patch12: security fix for CVE-2008-4690

* Wed Jul 02 2008 Oden Eriksson <oeriksson@mandriva.com> 2.8.6-2mdv2009.0
+ Revision: 230792
- fix build

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 2.8.6-2mdv2008.1
+ Revision: 140934
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed May 09 2007 Pixel <pixel@mandriva.com> 2.8.6-2mdv2008.0
+ Revision: 25767
- fix segfault with -crawl -width -dump options (#29785)


* Thu Nov 16 2006 Pixel <pixel@mandriva.com> 2.8.6-1mdv2007.0
+ Revision: 84986
- new relase
- adapt to lynx.cfg and lynx.lss now in /etc (they were in /usr/share/lynx)
- adapt to lynx_help now in /usr/share (instead of /usr/share/lynx)
- adapt patches or remove patches applied upstream (patch12 & patch13)

  + Oden Eriksson <oeriksson@mandriva.com>
    - Import lynx

* Tue Sep 26 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.8.5-9mdv2007.0
- rebuild for new ncurses

* Mon Nov 14 2005 Pixel <pixel@mandriva.com> 2.8.5-8mdk
- P13: security fix for CVE-2005-2929 (Vincent Danen)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.8.5-7mdk
- rebuilt against openssl-0.9.8a

* Thu Nov 03 2005 Pixel <pixel@mandriva.com> 2.8.5-6mdk
- fix bug in P12 for CAN-2005-3120 (Stew Benedict)

* Wed Oct 19 2005 Pixel <pixel@mandriva.com> 2.8.5-5mdk
- security update for CAN-2005-3120 (P12) (Stew Benedict)

* Tue Aug 23 2005 Pixel <pixel@mandriva.com> 2.8.5-4mdk
- switch default page to www.mandrivalinux.com (bugzilla #17712)

* Fri Apr 29 2005 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.8.5-3mdk
- fix buildrequires
- %%mkrel

* Thu Apr 28 2005 Pixel <pixel@mandriva.com> 2.8.5-2mdk
- build with --enable-locale-charset and enable LOCALE_CHARSET by default
- build with ncursesw to handle utf8

* Fri Feb 06 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.8.5-1mdk
- 2.8.5 final:)

* Thu Jan 29 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.5-0.15mdk.pre.4
- new release
- rediff patch 1

