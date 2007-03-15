%define	_hordeapp turba
#define	_snap	2005-10-17
#define	_rc		rc2
%define	_rel	1
#
%include	/usr/lib/rpm/macros.php
Summary:	Turba - Address book for IMP
Summary(pl.UTF-8):	Turba - Książka adresowa dla IMP-a
Name:		horde-%{_hordeapp}
Version:	2.1.4
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	ASL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/turba/%{_hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	950b5645ee75ed0df7a0f594c5e7d285
#Source0:	ftp://ftp.horde.org/pub/turba/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
#Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
Source1:	%{_hordeapp}.conf
Source2:	%{_hordeapp}-trans.mo
Patch0:		%{_hordeapp}-attrcache.patch
URL:		http://www.horde.org/turba/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.304
BuildRequires:	tar >= 1:1.15.1
Requires(triggerpostun):	sed >= 4.0
Requires:	horde >= 3.0
Requires:	php(xml)
Requires:	php-common >= 3:4.1.0
Requires:	webapps
Obsoletes:	%{_hordeapp}
Obsoletes:	horde-addons-turba
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)' 'pear(Net/IMSP.php)' 'pear(Net/IMSP/Utils.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		schemadir	/usr/share/openldap/schema
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Turba is a complete basic contact management application. SQL, LDAP,
and Horde Preferences backends are available and are well tested. You
can define the fields in your address books in a very flexible way,
just by changing the config files. You can import/export from/to Pine,
Mulberry, CSV, TSV, and vCard contacts. You can create distribution
lists from your addressbooks, which are handled transparently by IMP
and other Horde applications. And there are Horde API functions to add
and search for contacts.

%description -l pl.UTF-8
Turba to kompletna aplikacja do podstawowego zarządzania kontaktami.
Dostępne i dobrze przetestowane są backendy ustawień SQL, LDAP i
Horde. Można definiować pola książki adresowej w bardzo elastyczny
sposób, po prostu zmieniając pliki konfiguracyjne. Kontakty można
importować/eksportować z/do Pine, Mulberry, CSV, TSV i vCard. Można
tworzyć listy dystrybucyjne z książek adresowych, które są obsługiwane
w sposób przezroczysty przez IMP-a i inne aplikacje Horde. Są także
funkcje API Horde do dodawania i wyszukiwania kontaktów.

%package -n openldap-schema-rfc2739
Summary:	LDAP schema for freebusy information
Summary(pl.UTF-8):	Schemat LDAP do informacji freebusy
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-rfc2739
This package contains rfc2739.schema for openldap.

To store freebusy information in the LDAP directory, you'll need the
rfc2739.schema from <http://www.whitemiceconsulting.com/node/42>.

%description -n openldap-schema-rfc2739 -l pl.UTF-8
Ten pakiet zawiera schemat rfc2739.schema dla openldap.

Aby przechowywać informacje freebusy w bazie LDAP potrzebny jest
schemat rfc2739.schema z <http://www.whitemiceconsulting.com/node/42>.

%prep
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1

rm */.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

install %{SOURCE2} 		$RPM_BUILD_ROOT%{_appdir}/locale/pl_PL/LC_MESSAGES/turba.mo

install -d $RPM_BUILD_ROOT%{schemadir}
install scripts/ldap/rfc2739.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You may need to
create the Turba database tables. Look into directory
%{_docdir}/%{name}-%{version}/sql
to find out how to do this for your database.

For LDAP backend you need php-ldap package.
If you want to store freebusy information in LDAP database, also
install openldap-schema-rfc2739 package.

EOF
fi

%post -n openldap-schema-rfc2739
%openldap_schema_register %{schemadir}/rfc2739.schema
%service -q ldap restart

%postun -n openldap-schema-rfc2739
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/rfc2739.schema
	%service -q ldap restart
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- turba <= 1.2.2-2
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e '/^Include.*turba.conf/d' /etc/httpd/httpd.conf
fi

if [ -f /etc/httpd/turba.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f /etc/httpd/turba.conf.rpmsave %{_sysconfdir}/apache.conf
fi

%service -q httpd restart

%triggerpostun -- horde-%{_hordeapp} < 2.1-1.rc2.0.2, %{_hordeapp}
for i in attributes.php conf.php menu.php prefs.php sources.php; do
	if [ -f /etc/horde.org/%{_hordeapp}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/%{_hordeapp}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

if [ -L /etc/apache/conf.d/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register apache %{_webapp}
	rm -f /etc/apache/conf.d/99_horde-%{_hordeapp}.conf
	%service -q apache reload
fi
if [ -L /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	rm -f /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README docs/* scripts/*.reg scripts/ldap scripts/sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

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
