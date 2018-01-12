##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import collections

class Minidft(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://qe-forge.org/gf/download/frsrelease/144/456/MiniDFT-1.06.tar.gz"

    version('1.06', '52db2d3f308af1a846daff45af1a977d')

    variant("openmp", default=False, description="Enable openmp")
    variant("shared", default=True, description="Enable shared libraries")

    depends_on("fftw")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")
    depends_on("mpi")

    parallel = False

    def setup_environment(self, spack_env, run_env):
        spack_env.set("CRAYPE_LINK_TYPE", "dynamic")

    @property
    def build_directory(self):
        return self.stage.source_path + "/src"

    def edit(self, spec, prefix):
        spec = self.spec
        shared = True if "+shared" in spec else False
        contents = {}

        flags = ""
        if "%intel" in spec:
            dflags = "-D__INTEL"
            flags = " -fpp -O2"
        elif "%gcc" in spec:
            dflags = "-D__GFORTRAN"
            flags = " -O3 -cpp -x f95-cpp-input"
        elif "%cce" in spec:
            dflags = "-D__CRAY"
            flags = " -O2 -e F"
        elif "pgi" in spec:
            dflags = "-D__PGI"
            flags = " -fast -Mcache_align -r8 -Mpreprocess"

        contents["DFLAGS"] = dflags
        contents["FFLAGS"] = flags

        if "+openmp" in spec:
            contents["USE_OPENMP"] = "TRUE"
            fftw_libs =  find_libraries(["libfftw3", "libfftw3_threads"],
                                   root=spec["fftw"].prefix.lib,
                                   shared=shared)
            if "%intel" in spec:
                contents["DFLAGS"] +=  " -D__OPENMP"

            contents["FFLAGS"] += " " + self.compiler.openmp_flag
            contents["LDFLAGS"] = self.compiler.openmp_flag

        else:
            fftw_libs = find_libraries("libfftw3", root=spec["fftw"].prefix.lib,
                                shared=shared)

        contents["FFTW_INCL"] = "-I{0}".format(spec["fftw"].prefix.include)
        contents["FFTW_LIBS"] = fftw_libs.ld_flags

        blas_flags = spec["blas"].libs.ld_flags
        if "^intel-mkl" in spec and "~shared" in spec:
            blas_flags = "-Wl,--start-group {0} -Wl,--end-group".format(blas_flags)
        contents["BLAS_LIBS"] = blas_flags

        contents["CC" ] = spack_cc
        contents["FC"] = spack_fc
        contents["LD"] = spack_fc


        if "+scalapack" in spec:
            contents["SCALAPACK"] = spec["scalapack"].libs

        contents["MPI"] = "-L{0}".format(spec["mpi"].prefix.lib)

        with open("src/Makefile", "w") as inc:
            for key in contents:
                inc.write("{0} = {1}\n".format(key, contents[key]))
            inc.write("include Makefile.base")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("src/mini_dft", prefix.bin)
        install_tree("test", prefix.test)
        install_tree("benchmark", prefix.benchmark)
        install_tree("espresso", prefix.espresso)
