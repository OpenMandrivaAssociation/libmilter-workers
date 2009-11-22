%define realversion 8.14.3-1

%define name libmilter-workers
%define version %(echo %realversion | sed 's/-/_/g')
%define release %mkrel 1
%define libnamestatic %mklibname milter static-devel

Summary: Libmilter and a pool of threads
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://j-chkmail.ensmp.fr/libmilter/%{name}-%{realversion}.tgz
Source1: http://j-chkmail.ensmp.fr/libmilter/README
License: GPL
Group: Development/C
Url: http://j-chkmail.ensmp.fr/
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
Under original libmilter each connection generates one thread
on the filter. These threads remain alive during the connection
lifetime. So, one connection equals one thread.

For huge servers, handling many simultaneous connections (say, a 
hundred and more), this may be an issue.

Most of the time, these threads are idle waiting for sendmail
commands (which come from remote clients). Tests at some domains
shows that this hold for more than 95 % of the time.

This libmilter version creates a fixed number of threads (workers)
and distribute tasks when it receives commands from sendmail.

%package -n %libnamestatic
Summary: Libmilter and a pool of threads
Group: Development/C

%description -n %libnamestatic
Under original libmilter each connection generates one thread
on the filter. These threads remain alive during the connection
lifetime. So, one connection equals one thread.

For huge servers, handling many simultaneous connections (say, a
hundred and more), this may be an issue.

Most of the time, these threads are idle waiting for sendmail
commands (which come from remote clients). Tests at some domains
shows that this hold for more than 95 % of the time.

This libmilter version creates a fixed number of threads (workers)
and distribute tasks when it receives commands from sendmail.

%prep
%setup -q -n %{name}-%{realversion}
cp -f %{SOURCE1} ./

perl -pi -e "s/-O2/%optflags/" devtools/OS/Linux

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot%_includedir/milter/
cp include/libmilter/*.h %buildroot%_includedir/milter/

mkdir -p %buildroot/%_libdir
cp obj.`uname -s`.`uname -r`.`uname -m`/libmilter/libmilter.a %buildroot/%_libdir

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %libnamestatic
%defattr(-,root,root)
%doc README
%_includedir/milter/*.h
%_libdir/*.a

