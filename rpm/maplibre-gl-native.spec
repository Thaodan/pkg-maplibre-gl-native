%undefine __cmake_in_source_build

Summary: Maplibre GL Native Qt version
Name: qmaplibregl
Version: 2.1.0+git.23.12.28.0
Release: 1
License: BSD-2-Clause
Group: Libraries/Geosciences
URL: https://github.com/maplibre/maplibre-gl-native

Source: %{name}-%{version}.tar.gz
Patch1: 0001-Use-CURL-for-downloads.patch
Patch2: 0002-Fixes-for-compilation-on-SFOS.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(icu-uc)
Conflicts: qmapboxgl
Obsoletes: qmapboxgl

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A library for embedding interactive, customizable vector maps into native applications on multiple platforms.
It takes stylesheets that conform to the Mapbox Style Specification, applies them to vector tiles that
conform to the Mapbox Vector Tile Specification, and renders them using OpenGL.

MapLibre GL Native is a community led fork derived from mapbox-gl-native.

PackageName: Maplibre GL Native Qt
PackagerName: rinigus
Categories:
  - Library
  - Maps
  - Science
Icon: https://raw.githubusercontent.com/maplibre/maplibre.github.io/main/img/maplibre-logo-dark.svg

%package devel
Summary:        Development files for %{name}
License:        Open Source
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the development headers for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/maplibre-native-qt

%build
%if 0%{?cmake_build}
%define _vpath_builddir %{_target_platform}
mkdir -p %{_vpath_builddir}
%endif

# Workaround https://github.com/maplibre/maplibre-native/issues/906
# error: ignoring attributes on template argument 'mbgl::gfx::Vertex<mbgl::TypeList<mbgl::attributes::fade_opacity> >' {aka 'mbgl::gfx::detail::VertexType<mbgl::gfx::AttributeType<float, 1> >'} [-Werror=ignored-attributes]
export CXXFLAGS="${CXXFLAGS} -Wno-error=ignored-attributes"

%cmake -DMLN_QT_WITH_WIDGETS=OFF \
       -DMLN_QT_WITH_LOCATION=OFF \
       -DCMAKE_INSTALL_PREFIX:PATH=/usr \
       -DMLN_QT_WITH_INTERNAL_ICU=OFF

%if 0%{?cmake_build}
%cmake_build
%else
%{__make} %{?_smp_mflags} -C %{_vpath_builddir}
%endif

%install
%if 0%{?cmake_install}
%cmake_install
%else
%define _vpath_builddir %{_target_platform}
%{__make} %{?_smp_mflags} -C %{_vpath_builddir} install DESTDIR=%{buildroot}
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_libdir}/libQMapLibre.so.*

%files devel
%{_includedir}/mbgl
%{_includedir}/QMapLibre
#{_libdir}/libQMapbox.a
%{_libdir}/libQMapLibre.so
%{_libdir}/cmake/QMapLibre

%changelog
