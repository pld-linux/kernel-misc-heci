#
# Conditional build:
%bcond_without  dist_kernel     # allow non-distribution kernel
%bcond_without  kernel          # don't build kernel modules
%bcond_without  userspace       # don't build userspace programs
%bcond_with     verbose         # verbose build (V=1)
#
Summary:	Linux kernel module for Intel AMT ME Interface
Summary(pl.UTF-8):	Moduł jądra Linuksa dla interfejsu Intel AMT ME
Name:		kernel%{_alt_kernel}-misc-heci
Version:	2.1.21.1032
Release:	1
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/openamt/heci-%{version}.tar.gz
# Source0-md5:	5432336addc51c534637b91505d30c0a
Patch0:		heci-%{version}-2.6.20.dif
URL:		http://www.openamt.org/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains Linux kernel module for Intel AMT ME Interface.

%description -l pl.UTF-8
Ten pakiet zawiera moduł jądra Linuksa do interfejsu Intel AMT ME.

%prep
%setup -q -n heci-%{version}
%patch -P0 -p1
cat > src/Makefile << EOF
obj-m += heci.o
heci-objs := heci_init.o interrupt.o heci_interface.o io_heci.o heci_main.o
%{?debug:CFLAGS += -DCONFIG_MODULE_NAME_DEBUG=1} 
EOF

%build
%build_kernel_modules -C src -m heci

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/heci -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README scripts/*
/lib/modules/%{_kernel_ver}/misc/*.ko*
