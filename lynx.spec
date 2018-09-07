%define versio_ %(echo %{version} |sed -e 's,\\\(dev\\\|pre\\\|rel\\\).*,,;s,\\\.,-,g')

Summary:	Text based browser for the world wide web
Name:		lynx
Version:	2.8.9dev.19
Release:	1
License:	GPLv2
Group:		Networking/WWW
Url:		http://lynx.isc.org
Source0:	https://invisible-mirror.net/archives/lynx/tarballs/%{name}%{version}.tar.bz2
#Source0:	http://lynx.isc.org/current/%{name}%{version}.tar.bz2
Patch0:		lynx2-8-7-adapt-to-modern-file-localizations.patch
Patch1:		lynx2-8-7-default-config.patch
Patch2:		lynx2-8-6-fix-ugly-color.patch
Patch10:	lynx2-8-7-tmp_dir.patch
Patch11:	lynx2-8-6-don-t-accept-command-line-args-to-telnet.patch
BuildRequires:	gettext
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(zlib)
Provides:	webclient
Provides:	lynx-ssl

%description
This a terminal based WWW browser. While it does not make any attempt
at displaying graphics, it has good support for HTML text formatting,
forms, and tables.

This version includes support for SSL encryption.

WARNING: In some countries, it is illegal to export this package. In some
countries, it may even be illegal to use it.

%prep
%setup  -qn %{name}%{version}
%autopatch -p1
sed -i -e 's,^#LOCALE_CHARSET:.*,LOCALE_CHARSET:TRUE,' lynx.cfg

%build
debian_options=`cat << DEBIAN
	--enable-warnings
	--enable-8bit-toupper
	--enable-externs
	--enable-cgi-links
	--enable-persistent-cookies
	--enable-nls
	--enable-prettysrc
	--enable-source-cache
	--enable-charset-choice
	--enable-default-colors
	--enable-ipv6
	--enable-nested-tables
	--enable-read-eta
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
%configure2_5x \
	--libdir=/usr/share/lynx \
	$debian_options \
	$redhat_options \
	$other_options
%make

%install
%makeinstall_std install-help

install -d %{buildroot}%{_sysconfdir}
cat >%{buildroot}%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang lynx

%files -f lynx.lang
%doc README
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg
%config(noreplace) %{_sysconfdir}/lynx.cfg
%config(noreplace) %{_sysconfdir}/lynx.lss
%{_mandir}/*/*
%{_bindir}/*
%{_datadir}/lynx_help

