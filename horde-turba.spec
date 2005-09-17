%define	_hordeapp turba
%define	_snap	2005-08-25
#define	_rc		rc1
%define	_rel	1
#
%include	/usr/lib/rpm/macros.php
Summary:	TURBA - Address book for IMP
Summary(pl):	TURBA - Ksi±¿ka adresowa dla IMP-a
Name:		%{_hordeapp}
Version:	2.1
Release:	%{?_rc:1.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	ASL
Vendor:		The Horde Project
Group:		Applications/WWW
#Source0:	ftp://ftp.horde.org/pub/turba/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
# Source0-md5:	dedab86cf74caf49f786f914f49ea8aa
Source1:	%{_hordeapp}.conf
Source2:	%{_hordeapp}-trans.mo
URL:		http://www.horde.org/turba/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.177
BuildRequires:	tar >= 1:1.15.1
Requires(triggerpostun):	sed >= 4.0
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-xml >= 3:4.1.0
Obsoletes:	horde-addons-turba
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)' 'pear(Net/IMSP.php)' 'pear(Net/IMSP/Utils.php)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		schemadir	/usr/share/openldap/schema

%description
Turba is a complete basic contact management application. SQL, LDAP,
and Horde Preferences backends are available and are well tested. You
can define the fields in your address books in a very flexible way,
just by changing the config files. You can import/export from/to Pine,
Mulberry, CSV, TSV, and vCard contacts. You can create distribution
lists from your addressbooks, which are handled transparently by IMP
and other Horde applications. And there are Horde API functions to add
and search for contacts.

%description -l pl
Turba to kompletna aplikacja do podstawowego zarz±dzania kontaktami.
Dostêpne i dobrze przetestowane s± backendy ustawieñ SQL, LDAP i
Horde. Mo¿na definiowaæ pola ksi±¿ki adresowej w bardzo elastyczny
sposób, po prostu zmieniaj±c pliki konfiguracyjne. Kontakty mo¿na
importowaæ/eksportowaæ z/do Pine, Mulberry, CSV, TSV i vCard. Mo¿na
tworzyæ listy dystrybucyjne z ksi±¿ek adresowych, które s± obs³ugiwane
w sposób przezroczysty przez IMP-a i inne aplikacje Horde. S± tak¿e
funkcje API Horde do dodawania i wyszukiwania kontaktów.

%package -n openldap-schema-rfc2739
Summary:	LDAP schema for freebusy information
Summary(pl):	Schemat LDAP do informacji freebusy
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-rfc2739
This package contains rfc2739.schema for openldap.

To store freebusy information in the LDAP directory, you'll need the
rfc2739.schema from
<ftp://kalamazoolinux.org/pub/projects/awilliam/ldap/schema/>.

%description -n openldap-schema-rfc2739 -l pl
Ten pakiet zawiera schemat rfc2739.schema dla openldap.

Aby przechowywaæ informacje freebusy w bazie LDAP potrzebny jest
schemat rfc2739.schema z
<ftp://kalamazoolinux.org/pub/projects/awilliam/ldap/schema/>.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes} \
	$RPM_BUILD_ROOT%{schemadir}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

install %{SOURCE2} 		$RPM_BUILD_ROOT%{_appdir}/locale/pl_PL/LC_MESSAGES/turba.mo
install scripts/ldap/rfc2739.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
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
	sed -i -e '/^Include.*turba.conf/d' /etc/httpd/httpd.conf
fi

if [ -f /etc/httpd/turba.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{_hordeapp}.conf{,.rpmnew}
	mv -f /etc/httpd/turba.conf.rpmsave %{_sysconfdir}/apache-%{_hordeapp}.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc LICENSE README docs/* scripts/*.reg scripts/ldap scripts/sql
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

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
