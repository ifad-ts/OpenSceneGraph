#
# Copyright (c) 2005 - 2014 Ralf Corsepius, Ulm, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define apivers 3.2.1
%define srcvers 3.2.1.3

Name:           OpenSceneGraph-ifad
Version:        %{srcvers}
Release:        1%{?dist}
Summary:        IFAD version of OpenSceneGraph. High performance real-time graphics toolkit.

Group:          Applications/Multimedia
# The OSGPL is just the wxWidgets license.
License:        wxWidgets
URL:            http://www.openscenegraph.org/
# Announced as stable, but published under developer_releases ;)
Source0:        http://www.openscenegraph.org/downloads/developer_releases/OpenSceneGraph-%{srcvers}.zip

Patch1:         0001-Cmake-fixes.patch
Patch2:         0002-Fix-invalid-char.patch
# Upstream deactivated building osgviewerWX for obscure reasons
# Reactivate for now.
Patch3:         0003-Activate-osgviewerWX.patch

BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  libXmu-devel
BuildRequires:  libX11-devel
BuildRequires:  Inventor-devel
BuildRequires:  freeglut-devel
BuildRequires:  libgta-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libungif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  doxygen graphviz
BuildRequires:  cmake
BuildRequires:  wxGTK-devel
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  gtkglext-devel
BuildRequires:  librsvg2-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  openal-soft-devel

BuildRequires:  qt-devel
BuildRequires:  qtwebkit-devel

BuildRequires:  SDL-devel

BuildRequires:  fltk-devel

BuildRequires:  gnuplot

BuildRequires:  libvncserver-devel

# According to the FPG, this should be defined, but it's not.
%define _fontdir /usr/share/fonts

%description
The OpenSceneGraph is an OpenSource, cross platform graphics toolkit for the 
development of high performance graphics applications such as flight 
simulators, games, virtual reality and scientific visualization. 
Based around the concept of a SceneGraph, it provides an object oriented 
framework on top of OpenGL freeing the developer from implementing and 
optimizing low level graphics calls, and provides many additional utilities 
for rapid development of graphics applications.

%prep
%setup -q -c
cd OpenSceneGraph-%{srcvers}
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e 's,\.:/usr/share/fonts/ttf:,.:%{_fontdir}:/usr/share/fonts/ttf:,' \
src/osgText/Font.cpp

iconv -f ISO-8859-1 -t utf-8 AUTHORS.txt > AUTHORS.txt~
mv AUTHORS.txt~ AUTHORS.txt
cd ..

%build
mkdir -p BUILD
pushd BUILD
CFLAGS="${RPM_OPT_FLAGS} -pthread"
CXXFLAGS="${RPM_OPT_FLAGS} -pthread"
%cmake -DBUILD_OSG_EXAMPLES=ON -DBUILD_DOCUMENTATION=ON ../OpenSceneGraph-%{srcvers} -Wno-dev
make VERBOSE=1 %{?_smp_mflags}

make doc_openscenegraph doc_openthreads
popd

%install
pushd BUILD
make install DESTDIR=${RPM_BUILD_ROOT}

# Supposed to take OpenSceneGraph data
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/OpenSceneGraph
popd

# Hack to fix error: File not found .../usr/share/doc/OpenThreads
mkdir -p %{buildroot}/usr/share/doc/OpenThreads

%files
%doc OpenSceneGraph-%{srcvers}/{AUTHORS,LICENSE,NEWS,README}.txt
%{_bindir}/osgarchive
%{_bindir}/osgconv
%{_bindir}/osgversion
%{_bindir}/osgviewer
%{_bindir}/osgfilecache
%{_bindir}/present3D
%{_bindir}/osgQtBrowser
%{_bindir}/osgQtWidgets

%package libs
Summary:        Runtime libraries for OpenSceneGraph
Group:          Applications/Multimedia

%description libs
Runtime libraries files for OpenSceneGraph.

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/osgPlugins-%{apivers}
#%exclude %{_libdir}/osgPlugins-%{apivers}/osgdb_qfont.so
%{_libdir}/libosgAnimation.so.*
%{_libdir}/libosgDB.so.*
%{_libdir}/libosgFX.so.*
%{_libdir}/libosgGA.so.*
%{_libdir}/libosgManipulator.so.*
%{_libdir}/libosgParticle.so.*
%{_libdir}/libosgPresentation.so.*
%{_libdir}/libosgShadow.so.*
%{_libdir}/libosgSim.so.*
%{_libdir}/libosg.so.*
%{_libdir}/libosgTerrain.so.*
%{_libdir}/libosgText.so.*
%{_libdir}/libosgUtil.so.*
%{_libdir}/libosgViewer.so.*
%{_libdir}/libosgVolume.so.*
%{_libdir}/libosgWidget.so.*

%package devel
Summary:        Development files for OpenSceneGraph
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}
Requires:       OpenThreads-ifad-devel

%description devel
Development files for OpenSceneGraph.

%files devel
%doc BUILD/doc/OpenSceneGraphReferenceDocs
%{_includedir}/osg
%{_includedir}/osgAnimation
%{_includedir}/osgDB
%{_includedir}/osgFX
%{_includedir}/osgGA
%{_includedir}/osgManipulator
%{_includedir}/osgParticle
%{_includedir}/osgPresentation
%{_includedir}/osgShadow
%{_includedir}/osgSim
%{_includedir}/osgTerrain
%{_includedir}/osgText
%{_includedir}/osgUtil
%{_includedir}/osgViewer
%{_includedir}/osgVolume
%{_includedir}/osgWidget
%{_libdir}/libosgAnimation.so
%{_libdir}/libosgDB.so
%{_libdir}/libosgFX.so
%{_libdir}/libosgGA.so
%{_libdir}/libosgManipulator.so
%{_libdir}/libosgParticle.so
%{_libdir}/libosgPresentation.so
%{_libdir}/libosgShadow.so
%{_libdir}/libosgSim.so
%{_libdir}/libosg.so
%{_libdir}/libosgTerrain.so
%{_libdir}/libosgText.so
%{_libdir}/libosgUtil.so
%{_libdir}/libosgViewer.so
%{_libdir}/libosgVolume.so
%{_libdir}/libosgWidget.so
%{_libdir}/pkgconfig/openscenegraph-osgAnimation.pc
%{_libdir}/pkgconfig/openscenegraph-osgDB.pc
%{_libdir}/pkgconfig/openscenegraph-osgFX.pc
%{_libdir}/pkgconfig/openscenegraph-osgGA.pc
%{_libdir}/pkgconfig/openscenegraph-osgManipulator.pc
%{_libdir}/pkgconfig/openscenegraph-osgParticle.pc
%{_libdir}/pkgconfig/openscenegraph-osg.pc
%{_libdir}/pkgconfig/openscenegraph-osgShadow.pc
%{_libdir}/pkgconfig/openscenegraph-osgSim.pc
%{_libdir}/pkgconfig/openscenegraph-osgTerrain.pc
%{_libdir}/pkgconfig/openscenegraph-osgText.pc
%{_libdir}/pkgconfig/openscenegraph-osgUtil.pc
%{_libdir}/pkgconfig/openscenegraph-osgViewer.pc
%{_libdir}/pkgconfig/openscenegraph-osgVolume.pc
%{_libdir}/pkgconfig/openscenegraph-osgWidget.pc
%{_libdir}/pkgconfig/openscenegraph.pc


%package examples-SDL
Summary:        OSG sample applications using SDL
Group:          Applications/Multimedia

%description examples-SDL
OSG sample applications using SDL.

%files examples-SDL
%{_bindir}/osgviewerSDL

%package examples-fltk
Summary:        OSG sample applications using FLTK
Group:          Applications/Multimedia

%description examples-fltk
OSG sample applications using FLTK.

%files examples-fltk
%{_bindir}/osgviewerFLTK

%package examples-gtk
Summary:        OSG sample applications using gtk
Group:          Applications/Multimedia

%description examples-gtk
OSG sample applications using gtk

%files examples-gtk
%{_bindir}/osgviewerGTK

%package qt
Summary:        OSG Qt bindings
Group:          Applications/Multimedia

%description qt
OSG Qt bindings.

%files qt
%{_libdir}/libosgQt.so.*
%dir %{_libdir}/osgPlugins-%{apivers}
#%{_libdir}/osgPlugins-%{apivers}/osgdb_qfont.so

%post qt -p /sbin/ldconfig

%postun qt -p /sbin/ldconfig

%package qt-devel
Summary:        OSG Qt development files
Group:          Applications/Multimedia
Requires:       %{name}-qt = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}
Requires:       qt-devel

%description qt-devel
Development files for OSG Qt bindings.

%files qt-devel
%{_includedir}/osgQt
%{_libdir}/libosgQt.so
%{_libdir}/pkgconfig/openscenegraph-osgQt.pc


%package examples-qt
Summary:        OSG sample applications using qt
Group:          Applications/Multimedia

%description examples-qt
OSG sample applications using qt

%files examples-qt
%{_bindir}/osgviewerQt
#%{_bindir}/osgQtBrowser
#%{_bindir}/osgQtWidgets

# OpenSceneGraph-examples
%package examples
Summary:        Sample applications for OpenSceneGraph
Group:          Applications/Multimedia

%description examples
Sample applications for OpenSceneGraph

%files examples
%{_bindir}/osg2cpp
%{_bindir}/osganalysis
%{_bindir}/osganimate
%{_bindir}/osganimationeasemotion
%{_bindir}/osganimationhardware
%{_bindir}/osganimationmakepath
%{_bindir}/osganimationmorph
%{_bindir}/osganimationnode
%{_bindir}/osganimationskinning
%{_bindir}/osganimationsolid
%{_bindir}/osganimationtimeline
%{_bindir}/osganimationviewer
%{_bindir}/osgatomiccounter
%{_bindir}/osgautocapture
%{_bindir}/osgautotransform
%{_bindir}/osgbillboard
%{_bindir}/osgblendequation
%{_bindir}/osgcallback
%{_bindir}/osgcamera
%{_bindir}/osgcatch
%{_bindir}/osgclip
%{_bindir}/osgcluster
%{_bindir}/osgcompositeviewer
%{_bindir}/osgcomputeshaders
%{_bindir}/osgcopy
%{_bindir}/osgcubemap
%{_bindir}/osgdatabaserevisions
%{_bindir}/osgdelaunay
%{_bindir}/osgdepthpartition
%{_bindir}/osgdepthpeeling
%{_bindir}/osgdistortion
%{_bindir}/osgdrawinstanced
%{_bindir}/osgfadetext
%{_bindir}/osgfont
%{_bindir}/osgforest
%{_bindir}/osgfpdepth
%{_bindir}/osgframerenderer
%{_bindir}/osgfxbrowser
%{_bindir}/osggameoflife
%{_bindir}/osggeometry
%{_bindir}/osggeometryshaders
%{_bindir}/osggpx
%{_bindir}/osggraphicscost
%{_bindir}/osghangglide
%{_bindir}/osghud
%{_bindir}/osgimagesequence
%{_bindir}/osgimpostor
%{_bindir}/osgintersection
%{_bindir}/osgkdtree
%{_bindir}/osgkeyboard
%{_bindir}/osgkeyboardmouse
%{_bindir}/osgkeystone
%{_bindir}/osglauncher
%{_bindir}/osglight
%{_bindir}/osglightpoint
%{_bindir}/osglogicop
%{_bindir}/osglogo
%{_bindir}/osgmanipulator
%{_bindir}/osgmemorytest
%{_bindir}/osgmotionblur
%{_bindir}/osgmovie
%{_bindir}/osgmultiplemovies
%{_bindir}/osgmultiplerendertargets
%{_bindir}/osgmultitexture
%{_bindir}/osgmultitexturecontrol
%{_bindir}/osgmultitouch
%{_bindir}/osgmultiviewpaging
%{_bindir}/osgoccluder
%{_bindir}/osgocclusionquery
%{_bindir}/osgoit
%{_bindir}/osgoscdevice
%{_bindir}/osgoutline
%{_bindir}/osgpackeddepthstencil
%{_bindir}/osgpagedlod
%{_bindir}/osgparametric
%{_bindir}/osgparticle
%{_bindir}/osgparticleeffects
%{_bindir}/osgparticleshader
%{_bindir}/osgpdf
%{_bindir}/osgphotoalbum
%{_bindir}/osgpick
%{_bindir}/osgplanets
%{_bindir}/osgpoints
%{_bindir}/osgpointsprite
%{_bindir}/osgposter
%{_bindir}/osgprecipitation
%{_bindir}/osgprerender
%{_bindir}/osgprerendercubemap
%{_bindir}/osgqfont 
%{_bindir}/osgreflect
%{_bindir}/osgrobot
%{_bindir}/osgscalarbar
%{_bindir}/osgscreencapture
%{_bindir}/osgscribe
%{_bindir}/osgsequence
%{_bindir}/osgshadercomposition
%{_bindir}/osgshadergen
%{_bindir}/osgshaders
%{_bindir}/osgshaderterrain
%{_bindir}/osgshadow
%{_bindir}/osgshape
%{_bindir}/osgsharedarray
%{_bindir}/osgsidebyside
%{_bindir}/osgsimpleshaders
%{_bindir}/osgsimplegl3
%{_bindir}/osgsimplifier
%{_bindir}/osgsimulation
%{_bindir}/osgslice
%{_bindir}/osgspacewarp
%{_bindir}/osgspheresegment
%{_bindir}/osgspotlight
%{_bindir}/osgstereoimage
%{_bindir}/osgstereomatch
%{_bindir}/osgteapot
%{_bindir}/osgterrain
%{_bindir}/osgtessellate
%{_bindir}/osgtessellationshaders
%{_bindir}/osgtext
%{_bindir}/osgtext3D
%{_bindir}/osgtexture1D
%{_bindir}/osgtexture2D
%{_bindir}/osgtexture3D
%{_bindir}/osgtexturecompression
%{_bindir}/osgtexturerectangle
%{_bindir}/osgthirdpersonview
%{_bindir}/osgthreadedterrain   
%{_bindir}/osguniformbuffer     
%{_bindir}/osgunittests
%{_bindir}/osguserdata
%{_bindir}/osguserstats
%{_bindir}/osgvertexattributes
%{_bindir}/osgvertexprogram
%{_bindir}/osgviewerGLUT
%{_bindir}/osgviewerWX
%{_bindir}/osgvirtualprogram
%{_bindir}/osgvnc  
%{_bindir}/osgvolume
%{_bindir}/osgwidgetaddremove
%{_bindir}/osgwidgetbox
%{_bindir}/osgwidgetcanvas
%{_bindir}/osgwidgetframe
%{_bindir}/osgwidgetinput
%{_bindir}/osgwidgetlabel
%{_bindir}/osgwidgetmenu
%{_bindir}/osgwidgetmessagebox
%{_bindir}/osgwidgetnotebook
%{_bindir}/osgwidgetperformance
%{_bindir}/osgwidgetscrolled
%{_bindir}/osgwidgetshader
%{_bindir}/osgwidgetstyled
%{_bindir}/osgwidgettable
%{_bindir}/osgwidgetwindow
%{_bindir}/osgwindows

%{_datadir}/OpenSceneGraph

# OpenThreads-ifad
%package -n OpenThreads-ifad
Summary:        OpenThreads-ifad
Group:          Applications/Multimedia
License:        wxWidgets

%description -n OpenThreads-ifad
OpenThreads is intended to provide a minimal & complete Object-Oriented (OO)
thread interface for C++ programmers.  It is loosely modeled on the Java
thread API, and the POSIX Threads standards.  The architecture of the 
library is designed around "swappable" thread models which are defined at 
compile-time in a shared object library.

%post -n OpenThreads-ifad -p /sbin/ldconfig

%postun -n OpenThreads-ifad -p /sbin/ldconfig

%files -n OpenThreads-ifad
%doc OpenSceneGraph-%{srcvers}/{AUTHORS,LICENSE,NEWS,README}.txt
%{_libdir}/libOpenThreads.so.*

# OpenThreads-ifad-devel
%package -n OpenThreads-ifad-devel
Summary:        Devel files for OpenThreads-ifad
Group:          Applications/Multimedia
License:        wxWidgets
Requires:       OpenThreads-ifad = %{version}-%{release}
Requires:       pkgconfig

%description -n OpenThreads-ifad-devel
Development files for OpenThreads.

%files -n OpenThreads-ifad-devel
%doc BUILD/doc/OpenThreadsReferenceDocs
%{_libdir}/pkgconfig/openthreads.pc
%{_libdir}/libOpenThreads.so
%{_includedir}/OpenThreads

%changelog
* Wed May 20 2015 Michael Bach Jensen - 3.2.1.2-1
- First build of IFAD's own version of OpenSceneGraph.
- Configurable number of frames that can go by before page requests are removed from the request queue. This is required for osgEarth in IRAD where the camera spins quickly.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.2.1-1
- Upgrade to 3.2.1.
- Rebase patches.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.2.0-2
- Modernize spec.
- Preps for 3.2.1.

* Wed Aug 14 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.2.0-1
- Upstream update.
- Rebase patches.

* Tue Aug 13 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.0.1-18
- Fix %%changelog dates.

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.0.1-15
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 3.0.1-14
- rebuild against new libjpeg

* Mon Sep 03 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.0.1-13
- BR: libvncserver-devel, ship osgvnc (RHBZ 853755).

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Marek Kasik <mkasik@redhat.com> - 3.0.1-11
- Rebuild (poppler-0.20.0)

* Mon May 07 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.0.1-10
- Append -pthread to CXXFLAGS (Fix FTBFS).

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-9
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.0.1-7
- Rebuild for new libpng

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.0.1-6
- rebuild(poppler)

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 3.0.1-5
- Rebuild (poppler-0.18.0)

* Mon Sep 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.0.1-3
- Add BR: qtwebkit-devel.
- Add osgQtBrowser, osgQtWidgets to OpenSceneGraph-examples-qt.

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 3.0.1-2
- Rebuild (poppler-0.17.3)

* Wed Aug 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.0.1-1
- Upstream update.
- Remove OpenSceneGraph2* tags.
- Split out OpenSceneGraph-qt, OpenSceneGraph-qt-devel.
- Pass -Wno-dev to cmake.
- Append -pthread to CFLAGS.

* Sun Jul 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.5-3
- Reflect curl having silently broken their API.

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 2.8.5-2
- Rebuild (poppler-0.17.0)

* Tue Jun 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.5-1
- Upstream update.

* Mon May 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.4-2
- Reflect fltk-include paths having changed incompatibly.

* Wed Apr 27 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.4-1
- Upstream update.
- Rebase OpenSceneGraph-*.diff.
- Spec file cleanup.

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 2.8.3-10
- Rebuild (poppler-0.16.3)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.8.3-8
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.8.3-7
- rebuild (poppler)

* Wed Dec 15 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.3-6
- Add %%{_fontdir} to OSG's font file search path.

* Sat Nov 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.8.3-5
- rebuilt (poppler)

* Thu Sep 30 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.3-4
- rebuild (libpoppler-glib.so.6).

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.8.3-3
- rebuild (poppler)

* Mon Jul 12 2010 Dan Horák <dan@danny.cz> - 2.8.3-2
- rebuilt against wxGTK-2.8.11-2

* Fri Jul 02 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.3-1
- Upstream update.
- Add osg-examples-gtk.

* Wed Aug 26 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.2-3
- Change Source0 URL (Upstream moved it once again).

* Tue Aug 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.2-2
- Spec file cleanup.

* Mon Aug 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.2-1
- Upstream update.
- Reflect upstream having changes Source0-URL.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.1-2
- Remove /usr/bin/osgfilecache from *-examples.
- Further spec cleanup.

* Wed Jun 24 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.8.1-1
- Upstream update.
- Reflect upstream having consolidated their Source0:-URL.
- Stop supporting OSG < 2.6.0.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Ralf Corsépius <rc040203@freenet.de> - 2.8.0-1
- Upgrade to OSG-2.8.0.
- Remove Obsolete: Producer hacks.

* Thu Aug 14 2008 Ralf Corsépius <rc040203@freenet.de> - 2.6.0-1
- Upgrade to OSG-2.6.0.

* Wed Aug 13 2008 Ralf Corsépius <rc040203@freenet.de> - 2.4.0-4
- Preps for 2.6.0.
- Reflect the Source0-URL having changed.
- Major spec-file overhaul.

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.0-3
- fix license tag

* Tue May 13 2008 Ralf Corsépius <rc040203@freenet.de> - 2.4.0-2
- Add Orion Poplawski's patch to fix building with cmake-2.6.0.

* Mon May 12 2008 Ralf Corsépius <rc040203@freenet.de> - 2.4.0-1
- Upstream update.
- Adjust patches to 2.4.0.

* Mon Feb 11 2008 Ralf Corsépius <rc040203@freenet.de> - 2.2.0-5
- Add *-examples-SDL package.
- Add osgviewerSDL.
- Add *-examples-fltk package.
- Add osgviewerFLTK.
- Add *-examples-qt package.
- Move osgviewerQT to *-examples-qt package.

* Mon Feb 11 2008 Ralf Corsépius <rc040203@freenet.de> - 2.2.0-4
- Rebuild for gcc43.
- OpenSceneGraph-2.2.0.diff: Add gcc43 hacks.

* Wed Nov 28 2007 Ralf Corsépius <rc040203@freenet.de> - 2.2.0-3
- Re-add apivers.
- Rebuild against doxygen-1.5.3-1 (BZ 343591).

* Fri Nov 02 2007 Ralf Corsépius <rc040203@freenet.de> - 2.2.0-2
- Add qt.

* Thu Nov 01 2007 Ralf Corsépius <rc040203@freenet.de> - 2.2.0-1
- Upstream upgrade.
- Reflect Source0-URL having changed once again.
- Reflect upstream packaging changes to spec.

* Sat Oct 20 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-8
- Reflect Source0-URL having changed.

* Thu Sep 27 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-7
- Let OpenSceneGraph-libs Obsoletes: Producer
- Let OpenSceneGraph-devel Obsoletes: Producer-devel.

* Wed Sep 26 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-6
- By public demand, add upstream's *.pcs.
- Add hacks to work around the worst bugs in *.pcs.
- Add OpenSceneGraph2-devel.
- Move ldconfig to *-libs.
- Abandon OpenThreads2.
- Remove obsolete applications.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-5
- Prepare renaming package into OpenSceneGraph2.
- Split out run-time libs into *-libs subpackage.
- Rename pkgconfig files into *-2.pc.
- Reactivate ppc64.
- Mass rebuild.

* Sat Jun 30 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-4
- Cleanup CVS.
- Add OSG1_Producer define.

* Fri Jun 29 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-3
- Re-add (but don't ship) *.pc.
- Let OpenSceneGraph "Obsolete: Producer".
- Let OpenSceneGraph-devel "Obsolete: Producer-devel".

* Wed Jun 27 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-2
- Build docs.

* Fri Jun 22 2007 Ralf Corsépius <rc040203@freenet.de> - 2.0-1
- Upgrade to 2.0.

* Thu Jun 21 2007 Ralf Corsépius <rc040203@freenet.de> - 1.2-4
- ExcludeArch: ppc64 (BZ 245192, 245196).

* Thu Jun 21 2007 Ralf Corsépius <rc040203@freenet.de> - 1.2-3
- Remove demeter (Defective, abandoned by upstream).

* Wed Mar 21 2007 Ralf Corsépius <rc040203@freenet.de> - 1.2-2
- Attempt to build with gdal enabled.

* Thu Oct 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2-1
- Upstream update.
- Remove BR: flex bison.
- Drop osgfbo and osgpbuffer.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.1-2
- Mass rebuild.

* Thu Aug 24 2006 Ralf Corsépius <rc040203@freenet.de> - 1.1-1
- Upstream update.

* Sat Jul 08 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0-5
- Rebuilt to with gcc-4.1.1-6.

* Wed Jun 07 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0-4
- Try to avoid adding SONAMEs on plugins and applications.

* Tue Jun 06 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0-3
- Add SONAME hack to spec (PR 193934).
- Regenerate OpenSceneGraph-1.0.diff.
- Remove OpenSceneGraph-1.0.diff from look-aside cache. Add to CVS instead.
- Fix broken shell fragments.

* Sun Feb 19 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0-2
- Rebuild.

* Sat Dec 10 2005 Ralf Corsépius <rc040203@freenet.de> - 1.0-1
- Upstream update.

* Wed Dec 07 2005 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-5
- Try at getting this package buildable with modular X11.

* Tue Dec 06 2005 Ralf Corsepius <rc040203@freenet.de> - 0.9.9-4%{?dist}.1
- Merge diffs into one file.
- Fix up *.pcs from inside of *.spec.

* Sun Aug 28 2005 Ralf Corsepius <rc040203@freenet.de> - 0.9.9-4
- Propagate %%_libdir to pkgconfig files.
- Fix typo in %%ifarch magic to setup LD_LIBRARY_PATH
- Move configuration to %%build.
- Spec file cosmetics.

* Sat Aug 27 2005 Ralf Corsepius <rc040203@freenet.de> - 0.9.9-3
- Add full URL to Debian patch.
- Add _with_demeter.
- Extend Producer %%description.
- Extend OpenThreads %%description.

* Tue Aug 09 2005 Ralf Corsepius <ralf@links2linux.de> - 0.9.9-2
- Fix license to OSGPL.
- Change permissions on pkgconfig files to 0644.

* Tue Aug 02 2005 Ralf Corsepius <ralf@links2linux.de> - 0.9.9-1
- FE submission.

* Thu Jul 21 2005 Ralf Corsepius <ralf@links2linux.de> - 0.9.9-0
- Initial spec.
