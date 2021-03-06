Name:           yumdaemon
Version:        0.9.2
Release:        5%{?dist}
Summary:        DBus daemon for yum package actions

License:        GPLv2+
URL:            https://github.com/timlau/yum-daemon
Source0:        https://fedorahosted.org/releases/y/u/yumex/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       dbus-python
Requires:       yum >= 3.4.0
Requires:       polkit

Requires(post):     policycoreutils-python
Requires(postun):   policycoreutils-python

%description
Dbus daemon for yum package actions

%prep
%setup -q


%build
# Nothing to build

%install
make install DESTDIR=$RPM_BUILD_ROOT DATADIR=%{_datadir} SYSCONFDIR=%{_sysconfdir}

%package -n python3-%{name}
Summary:        Python 3 api for communicating with the yum-daemon DBus service
Group:          Applications/System
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}
Requires:       python3-gobject

%description -n python3-%{name}
Python 3 api for communicating with the yum-daemon DBus service


%files -n  python3-%{name}
%{python3_sitelib}/%{name}/

%package -n python-%{name}
Summary:        Python 2 api for communicating with the yum-daemon DBus service
Group:          Applications/System
BuildRequires:  python2-devel
Requires:       %{name} = %{version}-%{release}
Requires:       pygobject3

%description -n python-%{name}
Python 2 api for communicating with the yum-daemon DBus service


%files -n  python-%{name}
%{python_sitelib}/%{name}/

# apply the right selinux file context
# http://fedoraproject.org/wiki/PackagingDrafts/SELinux#File_contexts

%post
semanage fcontext -a -t rpm_exec_t '%{_datadir}/%{name}/%{name}-system' 2>/dev/null || :
restorecon -R %{_datadir}/%{name}/%{name}-system || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t rpm_exec_t '%{_datadir}/%{name}/%{name}-system' 2>/dev/null || :
fi

%files
%doc README.md examples/ ChangeLog COPYING
%{_datadir}/dbus-1/system-services/*
%{_datadir}/dbus-1/services/*
%{_datadir}/%{name}/
%{_datadir}/polkit-1/actions/*
# this should not be edited by the user, so no %%config
%{_sysconfdir}/dbus-1/system.d/*


%changelog
* Wed Oct 23 2013 Tim Lauridsen <timlau@fedoraproject.org> 0.9.2-5
- removed %%config from %%{_sysconfdir}/dbus-1/system.d/*

* Wed Oct 23 2013 Tim Lauridsen <timlau@fedoraproject.org> 0.9.2-4
- dont own %%{_datadir}/polkit-1/actions/ dir

* Wed Oct 23 2013 Tim Lauridsen <timlau@fedoraproject.org> 0.9.2-3
- added DATADIR=%%{_datadir} SYSCONFDIR=%%{_sysconfdir} to make install

* Wed Oct 23 2013 Tim Lauridsen <timlau@fedoraproject.org> 0.9.2-2
- converted tab to spaces

* Wed Oct 23 2013 Tim Lauridsen <timlau@fedoraproject.org> 0.9.2-1
- bumped release to 0.9.2

* Mon Nov 5 2012 Tim Lauridsen <timlau@fedoraproject.org> 0.9.1-1
- both python2 & python3 uses same sources

* Sat May 26 2012 Tim Lauridsen <timlau@fedoraproject.org> 0.9.0-1
- Initial rpm for yum-daemon
