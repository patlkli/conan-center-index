from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
from conan.tools.microsoft import is_msvc, is_msvc_static_runtime
import os


required_conan_version = ">=2.0.9"

#
class FastcgippConan(ConanFile):
    name = "fastcgipp"
    description = "High-efficiency C++ API to communicate with web servers through the FastCGI protocol"
    license = "LGPL-3.0-or-later"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/eddic/fastcgipp"
    topics = ("api", "web", "fastcgi")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_sql": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_sql": False
    }
    implements = ["auto_shared_fpic"]

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        if self.options.with_sql:
            self.requires("libpq/15.5")
        self.requires("libcurl/8.10.1")

    def validate(self):
        check_min_cppstd(self, 20)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        # Using patches is always the last resort to fix issues. If possible, try to fix the issue in the upstream project.
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["SQL"] = self.options.with_sql
        tc.generate()

        deps = CMakeDeps(self)
        # You can override the CMake package and target names if they don't match the names used in the project
        # deps.set_property("fontconfig", "cmake_file_name", "Fontconfig")
        # deps.set_property("fontconfig", "cmake_target_name", "Fontconfig::Fontconfig")
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "COPYING", self.source_folder, os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

        # Some files extensions and folders are not allowed. Please, read the FAQs to get informed.
        # Consider disabling these at first to verify that the package_info() output matches the info exported by the project.
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = ["fastcgipp"]
        self.cpp_info.set_property("cmake_file_name", "Fastcgipp")
        self.cpp_info.set_property("cmake_target_name", "Fastcgipp::fastcgipp")

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("pthread")
