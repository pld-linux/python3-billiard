#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	billiard
Summary:	Multiprocessing Pool Extensions
Summary(pl.UTF-8):	Rozszerzenia puli procesów
Name:		python3-%{module}
Version:	4.2.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/billiard/
Source0:	https://files.pythonhosted.org/packages/source/b/billiard/%{module}-%{version}.tar.gz
# Source0-md5:	67dfb22a28126cfdbfe9f8e0bcdc177d
URL:		https://github.com/celery/billiard
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 1:40.0.0
%if %{with tests}
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-psutil >= 5.8.0
BuildRequires:	python3-pytest
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
billiard is a fork of the Python 2.7 multiprocessing package. The
multiprocessing package itself is a renamed and updated version of R
Oudkerk's pyprocessing package. This standalone variant draws its
fixes/improvements from python-trunk and provides additional bug fixes
and improvements.

%description -l pl.UTF-8
billiard to odgałęzienie pakietu multiprocessing z Pythona 2.7. Pakiet
multiprocessing to uaktualniona wersja pakietu pyprocessing R Oudkerka
ze zmienioną nazwą. Samodzielny wariant czerpie poprawki i
usprawnienia z najświeższego Pythona, ponadto zawiera dodatkowe
poprawki błędów i ulepszenia.

%package apidocs
Summary:	API documentation for billiard module
Summary(pl.UTF-8):	Dokumentacja API modułu billiard
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for billiard module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu billiard.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest t/unit
%endif

%if %{with doc}
cd Doc
PYTHONPATH=$(pwd)/../build-3/lib \
sphinx-build-3 -b html -d .build/doctrees . .build/html
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/.build/html/{_static,library,*.html,*.js}
%endif
