Summary:	Script to help thwart SSH server attacks
Summary(pl):	Skrypt do blokowania ataków na serwery SSH
Name:		DenyHosts
Version:	0.5.5
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/denyhosts/%{name}-%{version}.tar.gz
# Source0-md5:	e5b49f8e949d3afd3bbd9d4611267dae
Source1:	%{name}.cron
Source2:	%{name}.cfg
Patch0:		%{name}-kodos.patch
URL:		http://denyhosts.sourceforge.net/
BuildRequires:	python
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
DenyHosts jest skryptem dla administratorów systemów Linux, którego
zadaniem jest odparcie ataków na serwery SSH.

W logach SSH mo¿na znale¼æ wiele informacji o próbach uzyskania
dostêpu do serwera poprzez us³ugê SSH. Dobrze jest zapobiec kolejnym
próbom w³amania przez odciêcie w³amywaczom dostêpu do serwera.

%prep
%setup -q
%patch0 -p1

%build
echo 'VERSION="%{version}"' > version.py
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d}

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(755,root,root) %{_bindir}/*
