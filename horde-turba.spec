%include	/usr/lib/rpm/macros.php
Summary:	TURBA - Address book for IMP
Summary(pl):	TURBA - Ksi±¿ka adresowa dla IMP-a
Name:		turba
Version:	2.0.2
Release:	2.1
License:	LGPL
Vendor:		The Horde Project
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Source0:	http://ftp.horde.org/pub/turba/%{name}-h3-%{version}.tar.gz
# Source0-md5:	e3b04476d9d18f4c9774f5da76a03f22
Source1:	%{name}.conf
Source2:	%{name}-trans.mo
URL:		http://www.horde.org/turba/
BuildRequires:	rpmbuild(macros) >= 1.177
Requires(triggerpreun):	sed >= 4.0
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-xml >= 4.1.0
Obsoletes:	horde-addons-turba
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)' 'pear(Net/IMSP.php)' 'pear(Net/IMSP/Utils.php)'

%define		hordedir	/usr/share/horde
%define		schemadir	/usr/share/openldap/schema
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{name}
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

%description
Turba is a complete basic contact management application. SQL, LDAP,
and Horde Preferences backends are available and are well tested. You
can define the fields in your address books in a very flexible way,
just by changing the config files. You can import/export from/to Pine,
Mulberry, CSV, TSV, and vCard contacts. You can create distribution
lists from your addressbooks, which are handled transparently by IMP
and other Horde applications. And there are Horde API functions to add
and search for contacts.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit <http://www.horde.org/>.

%description -l pl
Turba to kompletna aplikacja do podstawowego zarz±dzania kontaktami.
Dostêpne i dobrze przetestowane s± backendy ustawieñ SQL, LDAP i
Horde. Mo¿na definiowaæ pola ksi±¿ki adresowej w bardzo elastyczny
sposób, po prostu zmieniaj±c pliki konfiguracyjne. Kontakty mo¿na
importowaæ/eksportowaæ z/do Pine, Mulberry, CSV, TSV i vCard. Mo¿na
tworzyæ listy dystrybucyjne z ksi±¿ek adresowych, które s± obs³ugiwane
w sposób przezroczysty przez IMP-a i inne aplikacje Horde. S± tak¿e
funkcje API Horde do dodawania i wyszukiwania kontaktów.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP-a) zajrzyj na stronê <http://www.horde.org/>.

%package -n openldap-schema-rfc2739
Summary:	LDAP schema for freebusy information
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-rfc2739
This package contains rfc2739.schema for openldap.

To store freebusy information in the LDAP directory, you'll need the
rfc2739.schema from
<ftp://kalamazoolinux.org/pub/projects/awilliam/misc-ldap/>.

%prep
%setup -q -n %{name}-h3-%{version}

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes} \
	$RPM_BUILD_ROOT%{schemadir}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
cp -pR  config/*.xml            $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

install %{SOURCE2} 		$RPM_BUILD_ROOT%{_appdir}/locale/pl_PL/LC_MESSAGES/turba.mo

install scripts/ldap/rfc2739.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You may need to
create the TURBA database tables. Look into directory
/usr/share/doc/%{name}-%{version}/sql
to find out how to do this for your database.

For LDAP backend you need php-ldap package.
If you want to store freebusy information in LDAP database, also
install openldap-schema-rfc2739 package.

EOF
fi

%postun
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

%post -n openldap-schema-rfc2739
if ! grep -q %{schemadir}/rfc2739.schema /etc/openldap/slapd.conf; then
	sed -i -e '
		/^include.*local.schema/{
			i\
include		%{schemadir}/rfc2739.schema
		}
	' /etc/openldap/slapd.conf
fi

if [ -f /var/lock/subsys/ldap ]; then
    /etc/rc.d/init.d/ldap restart >&2
fi

%postun -n openldap-schema-rfc2739
if [ "$1" = "0" ]; then
	if grep -q %{schemadir}/rfc2739.schema /etc/openldap/slapd.conf; then
		sed -i -e '
		/^include.*\/usr\/share\/openldap\/schema\/rfc2739.schema/d
		' /etc/openldap/slapd.conf
	fi

	if [ -f /var/lock/subsys/ldap ]; then
		/etc/rc.d/init.d/ldap restart >&2 || :
	fi
fi

%triggerpostun -- turba <= 1.2.2-2
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e '/^Include.*%{name}.conf/d' /etc/httpd/httpd.conf
fi

if [ -f %{_apache2dir}/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f %{_apache2dir}/%{name}.conf.rpmsave %{_sysconfdir}/apache-%{name}.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*.reg scripts/ldap scripts/sql
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes

%files -n openldap-schema-rfc2739
%defattr(644,root,root,755)
%{schemadir}/*.schema
