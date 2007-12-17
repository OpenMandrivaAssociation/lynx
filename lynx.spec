%define version 2.8.6
%define versio_ 2-8-6
#%define subver pre.4
%define rel	2
%define	release	%mkrel %{rel}

Summary:	Text based browser for the world wide web
Name:		lynx
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://lynx.isc.org
Group:		Networking/WWW
BuildRequires:	gettext
BuildRequires:	openssl-devel
BuildRequires:	ncurses-devel
Source0:	http://lynx.isc.org/current/%name%{version}.tar.bz2
Patch0:		lynx2-8-5-adapt-to-modern-file-localizations.patch
Patch1:		lynx2-8-6-default-config.patch
Patch2:		lynx2-8-6-fix-ugly-color.patch
# fix segfault with -crawl -width -dump options (#29785)
Patch3:		lynx2-8-6-typo-fix-from-upstream.patch
Patch10:	lynx2-8-6-tmp_dir.patch
Patch11:	lynx2-8-6-don-t-accept-command-line-args-to-telnet.patch
Provides:	webclient lynx-ssl
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel libncursesw-devel
Obsoletes:	lynx-ssl

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
%patch3 -p1
%patch10 -p1
%patch11 -p1
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


