from conans.model.conan_file import ConanFile
from conans import CMake
import os


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    def requirements(self):  self.requires("openscenegraph-ifad/3.6.3.2@ifad/stable")
    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        #self.copy(pattern="*.so", dst="lib", src="lib")
        
    def test(self):
        #self.output.info(os.environ)
        #self.run("cmd /c dir /s")
        if self.settings.build_type == "Debug":
            self.run(".%sDebug\\osgrequire.exe cow.osgt" % os.sep)
        else:
            self.run(".%sRelease\\osgrequire.exe cow.osgt" % os.sep)
        #assert os.path.exists(os.path.join(self.deps_cpp_info["osgrequire"].rootpath, "LICENSE"))

