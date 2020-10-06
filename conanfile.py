from conans import ConanFile, CMake, tools
import os


class OpenscenegraphConan(ConanFile):
    name = "openscenegraph-ifad"
    version = "3.6.3.3"
    description = "IFAD version of OpenSceneGraph. OpenSceneGraph is an open source high performance 3D graphics toolkit"
    topics = ("ifad", "conan", "openscenegraph", "graphics")
    url = "https://github.com/ifad-ts/OpenSceneGraph"
    homepage = "https://github.com/ifad-ts/OpenSceneGraph"
    license = "MIT"
    exports_sources = "applications/*", "CMakeModules/*", "doc/*", "include/*", "packaging/*", "PlatformSpecifics/*", "src/*", "*.txt" # export the source code with the recipe
    short_paths = True
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_osg_applications": [True, False],
        "build_osg_plugins_by_default": [True, False],
        "build_osg_examples": [True, False],
        "dynamic_openthreads": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "build_osg_applications": False,
        "build_osg_plugins_by_default": True,
        "build_osg_examples": False,
        "dynamic_openthreads": True,
        "zlib:shared": True,
        "freetype:shared": True,
        "libjpeg:shared": True,
        "libxml2:shared": True,
        "libpng:shared": True,
        "libtiff:shared": True
    }
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.11",
        "freetype/2.10.2",
        "libjpeg/9d",
        "libxml2/2.9.10",
        #"libcurl/7.72.0",
        "libpng/1.6.37",
        "libtiff/4.1.0",
        #"sdl2/2.0.12@bincrafters/stable",
        #"jasper/2.0.14",
        #"cairo/1.17.2@bincrafters/stable",
        # "openblas/0.3.10", Removed until openblas is in conan center
    )

    _cmake = None

    def requirements(self):
        if self.settings.os != "Windows":
            self.requires("asio/1.13.0")
        if self.settings.os == "Linux":
            self.requires("xorg/system")
        self.requires("opengl/system")
        self.requires("glu/system")

    def system_requirements(self):
        if tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                installer.install("libegl1-mesa-dev")
                installer.install("libgtk2.0-dev")
                installer.install("libpoppler-glib-dev")
            else:
                self.output.warn("Could not determine Linux package manager, skipping system requirements installation.")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["BUILD_OSG_APPLICATIONS"] = self.options.build_osg_applications
            self._cmake.definitions["DYNAMIC_OPENSCENEGRAPH"] = self.options.shared
            self._cmake.definitions["BUILD_OSG_PLUGINS_BY_DEFAULT"] = self.options.build_osg_plugins_by_default
            self._cmake.definitions['BUILD_OSG_EXAMPLES'] = self.options.build_osg_examples
            self._cmake.definitions["DYNAMIC_OPENTHREADS"] = self.options.dynamic_openthreads

            if self.settings.compiler == "Visual Studio":
                self._cmake.definitions['BUILD_WITH_STATIC_CRT'] = "MT" in str(self.settings.compiler.runtime)

            self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.OSG_ROOT = self.package_folder
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("rt")
        if not self.options.shared:
            self.cpp_info.defines.append("OSG_LIBRARY_STATIC=1")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
