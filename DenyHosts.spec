Summary:	Script to help thwart SSH server attacks
Summary(pl):	Skrypt do blokowania atak�w na serwery SSH
Name:		DenyHosts
Version:	2.5
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/denyhosts/%{name}-%{version}.tar.gz
# Source0-md5:	b33f0cdae6448ae559c5f22dbffe59f2
Source1:	%{name}.cron
Source2:	%{name}.cfg
Source3:	%{name}.init
URL:		http://www.denyhosts.net/
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	python
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DenyHosts is a script intended to be run by Linux system
administrators to help thwart SSH server attacks.

If you've ever looked at your SSH log (/var/log/secure on Redhat,
/var/log/auth.log on Mandrake, etc...) you may be alarmed to see how
many hackers attempted to gain access to your server. Hopefully, none
of them were successful (but then again, how would you know?).
Wouldn't it be better to automatically prevent that attacker from
continuing to gain entry into your system?

%description -l pl
DenyHosts jest skryptem dla administrator�w system�w Linux, kt�rego
zadaniem jest odparcie atak�w na serwery SSH.

W logach SSH mo�na znale�� wiele informacji o pr�bach uzyskania
dost�pu do serwera poprzez us�ug� SSH. Dobrze jest zapobiec kolejnym
pr�bom w�amania przez odci�cie w�amywaczom dost�pu do serwera.

%prep
%setup -q

%build
echo 'VERSION="%{version}"' > version.py
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d,/etc/rc.d/init.d,%{_sbindir},/var/lib/%{name}}

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/denyhosts/daemon-control-dist $RPM_BUILD_ROOT%{_sbindir}/%{name}ctl
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/*.py
rm -r $RPM_BUILD_ROOT%{_datadir}/denyhosts
echo "127.0.0.1" > $RPM_BUILD_ROOT/var/lib/%{name}/allowed-hosts

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service DenyHosts restart

%preun
if [ "$1" = "0" ]; then
	%service DenyHosts stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README.txt CHANGELOG.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.cfg
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir /var/lib/%{name}
%config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/allowed-hosts
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
