Summary:	TURBA - Adress book for IMP
Summary(pl):	TURBA - Ksi±¿ka adresowa dla IMP-a
Name:		turba
Version:	2.0
Release:	1
License:	LGPL
Vendor:		The Horde Project
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}
Source0:	http://ftp.horde.org/pub/turba/%{name}-h3-%{version}.tar.gz
# Source0-md5:	23f143958fb72b9bf94a04a14e1cfd92
Source1:	%{name}.conf
Source2:	%{name}-trans.mo
URL:		http://www.horde.org/turba/
PreReq:		apache
Requires(post):	grep
Requires:	horde >= 3.0
Requires:	php-xml >= 4.1.0
Obsoletes:	horde-addons-turba
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		hordedir	/usr/share/horde
%define		confdir		/etc/horde.org

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
with Horde and its modules) please visit http://www.horde.org/ .

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
do IMP-a) zajrzyj na stronê http://www.horde.org/ .

%prep
%setup -q -n %{name}-h3-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachedir},%{confdir}/turba} \
	$RPM_BUILD_ROOT%{hordedir}/turba/{lib,locale,templates,themes,scripts}

cp -pR	*.php			$RPM_BUILD_ROOT%{hordedir}/turba
cp -pR  config/*.dist           $RPM_BUILD_ROOT%{confdir}/turba
cp -pR  config/*.xml            $RPM_BUILD_ROOT%{confdir}/turba
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{confdir}/turba/conf.php
cp -pR  lib/*                   $RPM_BUILD_ROOT%{hordedir}/turba/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{hordedir}/turba/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{hordedir}/turba/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{hordedir}/turba/themes

cp -p   config/.htaccess        $RPM_BUILD_ROOT%{confdir}/turba
cp -p   locale/.htaccess        $RPM_BUILD_ROOT%{hordedir}/turba/locale
cp -p   templates/.htaccess     $RPM_BUILD_ROOT%{hordedir}/turba/templates

install %{SOURCE1} 		$RPM_BUILD_ROOT%{apachedir}
ln -fs %{confdir}/%{name} 	$RPM_BUILD_ROOT%{hordedir}/%{name}/config

install %{SOURCE2} 		$RPM_BUILD_ROOT%{hordedir}/turba/locale/pl_PL/LC_MESSAGES/turba.mo

# bit unclean..
cd $RPM_BUILD_ROOT%{confdir}/turba
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

cat <<_EOF2_
IMPORTANT:
If you are installing for the first time, you must now
create the TURBA database tables. Look into directory
/usr/share/doc/%{name}-%{version}/drivers
to find out how to do this for your database.
_EOF2_

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
	    rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
	    /usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*.reg scripts/ldap
%dir %{hordedir}/%{name}
%attr(640,root,http) %{hordedir}/%{name}/*.php
%attr(750,root,http) %{hordedir}/%{name}/lib
%attr(750,root,http) %{hordedir}/%{name}/locale
%attr(750,root,http) %{hordedir}/%{name}/templates
%attr(750,root,http) %{hordedir}/%{name}/themes

%attr(750,root,http) %dir %{confdir}/%{name}
%dir %{hordedir}/%{name}/config
%attr(640,root,http) %{confdir}/%{name}/*.dist
%attr(640,root,http) %{confdir}/%{name}/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/%{name}.conf
%attr(660,root,http) %config(noreplace) %{confdir}/%{name}/*.php
%attr(640,root,http) %config(noreplace) %{confdir}/%{name}/*.xml
