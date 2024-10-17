%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define realversion 8.14.3-1

%define version %(echo %{realversion} | sed 's/-/_/g')
%define sdevdname %mklibname milter -d -s

Summary:	Libmilter and a pool of threads
Name:		libmilter-workers
Version:	%{version}
Release:	5
License:	Sendmail
Group:		Development/C
Url:		https://j-chkmail.ensmp.fr/
Source0:	http://j-chkmail.ensmp.fr/libmilter/%{name}-%{realversion}.tgz
Source1:	http://j-chkmail.ensmp.fr/libmilter/README

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

#----------------------------------------------------------------------------

%package -n %{sdevdname}
Summary:	Libmilter and a pool of threads
Group:		Development/C
Provides:	milter-devel = %{EVRD}

%description -n %{sdevdname}
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

%files -n %{sdevdname}
%doc README
%{_includedir}/libmilter/*.h
%{_libdir}/*.a

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{realversion}
cp -f %{SOURCE1} ./

perl -pi -e "s/-O2/%{optflags}/" devtools/OS/Linux

%build
%make

%install
mkdir -p %{buildroot}%{_includedir}/libmilter/
cp include/libmilter/*.h %{buildroot}%{_includedir}/libmilter/

mkdir -p %{buildroot}%{_libdir}
cp obj.`uname -s`.`uname -r`.`uname -m`/libmilter/libmilter.a %{buildroot}%{_libdir}

