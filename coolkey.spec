# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       coolkey

# >> macros
# << macros

Summary:    CoolKey PKCS
Version:    1.1.0
Release:    1
Group:      System/Libraries
License:    LGPLv2
URL:        http://directory.fedora.redhat.com/wiki/CoolKey
Source0:    %{name}-%{version}.tar.gz
Source100:  coolkey.yaml
Patch0:     coolkey-cache-dir-move.patch
Patch1:     coolkey-gcc43.patch
Patch2:     coolkey-latest.patch
Patch3:     coolkey-simple-bugs.patch
Patch4:     coolkey-thread-fix.patch
Patch5:     coolkey-cac.patch
Patch6:     coolkey-cac-1.patch
Patch7:     coolkey-pcsc-lite-fix.patch
Patch8:     coolkey-fix-token-removal-failure.patch
Requires:   nss-tools
Requires:   pcsc-lite
Requires:   ccid
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(nss)
BuildRequires:  autoconf
BuildRequires:  pcsc-lite-devel

%description
Linux Driver support for the CoolKey and CAC products. 


%package devel
Summary:    CoolKey Applet libraries
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Linux Driver support to access the CoolKey applet.


%prep
%setup -q

# coolkey-cache-dir-move.patch
%patch0 -p1
# coolkey-gcc43.patch
%patch1 -p1
# coolkey-latest.patch
%patch2 -p1
# coolkey-simple-bugs.patch
%patch3 -p1
# coolkey-thread-fix.patch
%patch4 -p1
# coolkey-cac.patch
%patch5 -p1
# coolkey-cac-1.patch
%patch6 -p1
# coolkey-pcsc-lite-fix.patch
%patch7 -p1
# coolkey-fix-token-removal-failure.patch
%patch8 -p1
# >> setup
# << setup

%build
# >> build pre
autoconf
# << build pre

%configure --disable-static \
    --with-debug \
    --disable-dependency-tracking \
    --enable-pk11install


# >> build post
make %{?_smp_mflags} CFLAGS="$CFLAGS -g -O2 -fno-strict-aliasing $CFLAGS " CXXFLAGS="$CXXFLAGS -g -O2 -fno-strict-aliasing $CFLAGS"
# << build post

%install
rm -rf %{buildroot}
# >> install pre
make install DESTDIR=$RPM_BUILD_ROOT
# << install pre

# >> install post
ln -s pkcs11/libcoolkeypk11.so $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/var/cache/coolkey
# << install post

%post
/sbin/ldconfig
# >> post
isThere=`modutil -rawlist -dbdir %{nssdb} | grep %{coolkey_module} || echo NO`
if [ "$isThere" == "NO" ]; then
if [ -x %{_bindir}/pk11install ]; then
pk11install -p %{nssdb} 'name=%{coolkey_module} library=libcoolkeypk11.so' ||:
fi
fi
# << post

%postun
/sbin/ldconfig
# >> postun
if [ $1 -eq 0 ]; then
modutil -delete %{coolkey_module} -dbdir %{nssdb} -force || :
fi
# << postun

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE 
%{_bindir}/pk11install
%{_libdir}/libcoolkeypk11.so
%{_libdir}/pkcs11
%{_libdir}/libckyapplet.so.1
%{_libdir}/libckyapplet.so.1.0.0
# >> files
# << files

%files devel
%defattr(-,root,root,-)
%{_libdir}/libckyapplet.so
%{_libdir}/pkgconfig/libckyapplet.pc
%{_includedir}/*.h
# >> files devel
# << files devel
