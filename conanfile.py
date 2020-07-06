from conans import ConanFile, CMake, tools
from pathlib import Path
from glob import glob
import os
import subprocess

from conans.tools import os_info, SystemPackageTool


class OpenSceneGraphConan(ConanFile):
    name = "openscenegraph-ifad"
    version = "3.6.3.1"
    license = "http://www.openscenegraph.org/images/LICENSE.txt"
    url = "https://github.com/ifad-ts/OpenSceneGraph"
    description = "IFAD version of OpenSceneGraph. The OpenSceneGraph is an open source high performance 3D graphics toolkit, used by application developers in fields such as visual simulation, games, virtual reality, scientific visualization and modelling. Written entirely in Standard C++ and OpenGL it runs on all Windows platforms, OSX, GNU/Linux, IRIX, Solaris, HP-Ux, AIX and FreeBSD operating systems. The OpenSceneGraph is now well established as the world leading scene graph technology, used widely in the vis-sim, space, scientific, oil-gas, games and virtual reality industries."
    settings = "os", "compiler", "build_type", "arch"
    requires = "osgvisual/11_full@ifad/stable"
    options = {"pure_gl3": [True, False]}
    default_options = "pure_gl3=False"
    generators = "cmake"
    copy_source_to_build_dir = False
    build_policy = "missing"  # "always" #
    short_paths = True  # for win<10 naming
    exports_sources = "applications/*", "CMakeModules/*", "doc/*", "include/*", "packaging/*", "PlatformSpecifics/*", "src/*", "*.txt" # export the source code with the recipe

    def configure(self):
        # it is necessary to remove the VS runtime when packaging multiple build types into a single package
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def system_requirements(self):
        self.output.warn("system_requirements: ")
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            self.run('sudo apt-get build-dep openscenegraph', True)
            # gstreamer seems missing after build-dep
            pack_name = "libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libasio-dev libcollada-dom2.4-dp-dev libdcmtk-dev libfltk1.3-dev libnvtt-dev libboost-filesystem-dev"
        elif os_info.linux_distro == "fedora" or os_info.linux_distro == "centos":
            pack_name = "TODOpackage_names_in_fedora_and_centos"
        elif os_info.is_macos:
            pack_name = "TODOpackage_names_in_macos"
        elif os_info.is_freebsd:
            pack_name = "TODOpackage_names_in_freebsd"
        elif os_info.is_solaris:
            pack_name = "TODOpackage_names_in_solaris"

        if pack_name:
            installer = SystemPackageTool()
            installer.install(
                pack_name)  # Install the package, will update the package database if pack_name isn't already installed

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['WIN32_USE_MP'] = "ON"
        cmake.definitions['BUILD_SHARED_LIBS'] = "ON"
        cmake.definitions['BUILD_OSGEXAMPLES'] = 'OFF'
        cmake.definitions['BUILD_DOCUMENTATION'] = 'OFF'
        cmake.definitions['BUILD_OSGAPPLICATIONS'] = 'ON'
        cmake.definitions['OSG_USE_QT'] = 'OFF'
        cmake.definitions['CMAKE_CXX_FLAGS_RELEASE'] = '/MD /O2 /Ob2 /D NDEBUG /Zi /Oy- /wd4589 /wd4456'
        cmake.definitions['CMAKE_SHARED_LINKER_FLAGS_RELEASE'] = '/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO'
        cmake.definitions['CMAKE_EXE_LINKER_FLAGS_RELEASE'] = '/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO'
        cmake.definitions['CMAKE_MODULE_LINKER_FLAGS_RELEASE'] = '/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO'
        if self.options.pure_gl3:
            cmake.definitions['OSG_GL3_AVAILABLE'] = 'ON'
            cmake.definitions['OSG_GL1_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GL2_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GLES1_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GLES2_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GL_DISPLAYLISTS_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GL_FIXED_FUNCTION_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GL_MATRICES_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GL_VERTEX_ARRAY_FUNCS_AVAILABLE'] = 'OFF'
            cmake.definitions['OSG_GL_VERTEX_FUNCS_AVAILABLE'] = 'OFF'

        with tools.environment_append({'OSG_3RDPARTY_DIR': self.deps_cpp_info["osgvisual"].rootpath.replace('\\', '/')}):
            cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        # add OpenSceneGraph-Data folder
        self.run("git clone https://github.com/openscenegraph/OpenSceneGraph-Data.git " +
                 os.path.join(self.package_folder, "OpenSceneGraph-Data"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.OSG_ROOT = self.package_folder
        self.env_info.OSG_FILE_PATH.append(os.path.join(self.package_folder, "OpenSceneGraph-Data"))
        if self.settings.os != "Windows":
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
