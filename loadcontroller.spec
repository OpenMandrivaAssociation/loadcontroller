%define name loadcontroller
%define version 0.11
%define rel %mkrel 4
%define release 0.BETA.%rel

Summary: A daemon which checks process
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}.src.tar.bz2
Source1: %name.initscript.bz2
License: GPL
Group: Monitoring
Url: http://www.virtualworlds.de/Download
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
A daemon which checks the load of an server in defineable
periods. If the load exceeds a defineable limit during a
defined time and if this was caused by a process of a 
defined user which exceeds a defined cpu-usage, the process
is killed and the user is informed by mail. This daemon can
be used on server systems where processes or scripts can be
executed by users e.g. on servers of webspace providers
which allow PHP / Perl / Shell-access. 

%prep
%setup -q

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# Setting default option in config file
perl -pi -e 's/^LANGUAGE=.*/LANGUAGE=en/' etc/loadctrl.config
cat >> etc/loadctrl.config <<EOF
CHECKUSER root root@localhost.localdomain
EOF

mkdir -p %buildroot{%_sysconfdir/sysconfig,%_initrddir}

# install initscript:
bzcat %SOURCE1 > %buildroot%_initrddir/%name
chmod 755 %buildroot%_initrddir/%name

# The config file
cp etc/loadctrl.config %buildroot/%_sysconfdir

# Our options for initscript
cat >  %buildroot/%_sysconfdir/sysconfig/%name <<EOF
OPTIONS=""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %name

%preun
%_preun_service %name

%files
%defattr(-,root,root)
%doc README TODO INSTALL AUTHORS
%config(noreplace) %_sysconfdir/loadctrl.config
%config(noreplace) %_sysconfdir/sysconfig/%name
%config(noreplace) %_initrddir/%name
%_bindir/%name

