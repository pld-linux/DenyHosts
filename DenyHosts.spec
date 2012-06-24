#
Summary:	Script to help thwart ssh server attacks.
Summary(pl):	Skrypt do blokowania atak�w na serwery SSH.
Name:		DenyHosts
Version:	0.5.5
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/DenyHosts/%{name}-%{version}.tar.gz
# Source0-md5:	e5b49f8e949d3afd3bbd9d4611267dae
Source1:	%{name}.cron
Source2:	%{name}.cfg
Patch0:		%{name}-kodos.patch
URL:		http://denyhosts.sourceforge.net/
BuildRequires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DenyHosts is a script intended to be run by Linux system
administrators to help thwart ssh server attacks.

If you've ever looked at your ssh log (/var/log/secure on Redhat,
/var/log/auth.log on Mandrake, etc...) you may be alarmed to see how
many hackers attempted to gain access to your server. Hopefully, none
of them were successful (but then again, how would you know?).
Wouldn't it be better to automatically prevent that attacker from
continuing to gain entry into your system?

%description -l pl
DenyHosts jest skryptem dla administrator�w system�w Linux, kt�rego
zadaniem jest odparcie atak�w na serwery ssh.

W logach ssh mo�na znale�� wiele informacji o pr�bach uzyskania
dost�pu do serwera poprzez us�ug� ssh. Dobrze jest zapobiec kolejnym
pr�bom w�amiania przez odci�cie w�amywaczom dost�pu do serwera.

%prep
%setup -q
%patch0 -p1

%build

echo 'VERSION="%{version}"' > version.py
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cron.d/%{name}
%attr(755,root,root) %{_bindir}/*
