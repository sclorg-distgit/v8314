%global scl_name_base v8
%global scl_name_version 314
 
%global scl %{scl_name_base}%{scl_name_version}
%scl_package %scl

%global install_scl 1

# do not produce empty debuginfo package
%global debug_package %{nil}

Name:		%scl_name
Version:	2.1
Release:	1%{?dist}
Summary:	%scl Software Collection
License:	MIT
Source0: 	LICENSE
Source1:	README

%if %{?install_scl} > 0
Requires: %{scl_prefix}gyp
Requires: %{scl_prefix}v8
Requires: %{scl_prefix}v8-devel
Requires: %{scl_prefix}runtime
%endif

BuildRequires:	scl-utils-build
BuildRequires:  python-devel
BuildRequires:  help2man

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.
 
%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build
 
%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl
Provides: scldevel(%{scl_name_base})

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -T -c
# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE0} .

%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF

chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7

%install
rm -rf %{buildroot}
%scl_install

mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}} 
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export PYTHONPATH=%{_scl_root}%{python_sitelib}\${PYTHONPATH:+:\${PYTHONPATH}}
export MANPATH=%{_mandir}:\$MANPATH
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
export CPATH=%{_includedir}\${CPATH:+:\${CPATH}}
export LIBRARY_PATH=%{_libdir}\${LIBRARY_PATH:+:\${LIBRARY_PATH}}
EOF

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF


# scl doesn't include this directory
mkdir -p %{buildroot}%{_scl_root}%{python_sitelib}
mkdir -p %{buildroot}%{_libdir}/pkgconfig

# install generated man page
mkdir -p %{buildroot}%{_mandir}/man7/
install -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%files

%files runtime
%scl_files
%doc README LICENSE
%{_mandir}/man7/%{scl_name}.*
 
%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Tue Jul 21 2015 Tomas Hrcka <thrcka@redhat.com> - 2.1-1
- RHSCL 2.1 release

* Mon Jan 05 2015 Tomas Hrcka <thrcka@redhat.com> - 2.0-11
- RHSCL 2.0 release

* Thu Apr 03 2014 Tomas Hrcka <thrcka@redhat.com> - 1.1-10
- Fix white space typo in README generation

* Mon Mar 31 2014 Honza Horak <hhorak@redhat.com> - 1.1-9
- Fix path typo in README
  Related: #1061462

* Mon Mar 24 2014 Tomas Hrcka <thrcka@redhat.com> - 1.1-8
- Add python_sitelib to the package
- Enable %files -f filesystem to fix manpages ownership

* Thu Feb 13 2014 Tomas Hrcka <thrcka@redhat.com> - 1.1-7
- Added Provides: scldevel(%{scl_name_base}) to scldevel subpackage

* Wed Feb 12 2014 Tomas Hrcka <thrcka@redhat.com> - 1.1-6
- Define scl_name_base and scl_name_version macros

* Wed Feb 12 2014 Honza Horak <hhorak@redhat.com> - 1.1-5
- Some more grammar fixes in README
  Related: #1061462

* Wed Feb 12 2014 Tomas Hrcka <thrcka@redhat.com> - 1.1-4
- Add README and LICENSE files
- Add man page
- Bump version to 1.1 

* Mon Jan 27 2014 Tomas Hrcka <thrcka@redhat.com> - 1-4
- Add -scldevel sub-package.

* Mon Dec 16 2013 Tomas Hrcka <thrcka@redhat.com> - 1-3
- Install collection packages as dependency

* Tue Nov 26 2013 Honza Horak <hhorak@redhat.com> - 1-2
- Provide CPATH and LIBRARY_PATH in the enable scriptlet

* Tue Oct 29 2013 thrcka@redhat.com - 1-1
- Initial version of the V8 Software Collection
