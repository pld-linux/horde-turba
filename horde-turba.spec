# TODO:
# - move configs to /etc
# - trigger to move configs
#
%include	/usr/lib/rpm/macros.php
Summary:	TURBA - Adress book for IMP
Summary(pl):	TURBA - Ksi±¿ka adresowa dla IMP-a
Name:		turba
Version:	1.2.2
Release:	1.2
License:	LGPL
Vendor:		The Horde Project
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}
Source0:	http://ftp.horde.org/pub/turba/turba-%{version}.tar.gz
# Source0-md5: 27d9ebbe6723dcb0e4aa61045feb60b0
Source1:	%{name}.conf
URL:		http://www.horde.org/turba/
BuildRequires:  rpm-php-pearprov >= 4.0.2-98
PreReq:         apache
Requires(post):	grep
Requires:       horde >= 2.0
Requires:	php-xml >= 4.1.0
Obsoletes:	horde-addons-turba
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		hordedir	/usr/share/horde

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
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{apachedir}
install -d $RPM_BUILD_ROOT%{hordedir}/turba/{config,graphics,lib,locale,templates,scripts}

install %{SOURCE1} $RPM_BUILD_ROOT%{apachedir}

cp -pR	*.php			$RPM_BUILD_ROOT%{hordedir}/turba
cp -pR  config/*.dist           $RPM_BUILD_ROOT%{hordedir}/turba/config
cp -pR  graphics/*              $RPM_BUILD_ROOT%{hordedir}/turba/graphics
cp -pR  lib/*                   $RPM_BUILD_ROOT%{hordedir}/turba/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{hordedir}/turba/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{hordedir}/turba/templates

cp -p   config/.htaccess        $RPM_BUILD_ROOT%{hordedir}/turba/config
cp -p   locale/.htaccess        $RPM_BUILD_ROOT%{hordedir}/turba/locale
cp -p   templates/.htaccess     $RPM_BUILD_ROOT%{hordedir}/turba/templates

ln -fs $RM_BUILD_ROOT%{hordedir}/turba/config $RPM_BUILD_ROOT%{apachedir}/turba

# bit unclean..
cd $RPM_BUILD_ROOT%{hordedir}/turba/config
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
%doc README docs/* scripts/*.reg scripts/drivers scripts/ldap

%dir %{hordedir}/turba
%attr(640,root,http) %{hordedir}/turba/*.php
%attr(750,root,http) %{hordedir}/turba/graphics
%attr(750,root,http) %{hordedir}/turba/lib
%attr(750,root,http) %{hordedir}/turba/locale
%attr(750,root,http) %{hordedir}/turba/templates

%attr(750,root,http) %dir %{hordedir}/turba/config
%attr(640,root,http) %{hordedir}/turba/config/*.dist
%attr(640,root,http) %{hordedir}/turba/config/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/turba.conf
%attr(640,root,http) %config(noreplace) %{hordedir}/turba/config/*.php
%{apachedir}/turba
