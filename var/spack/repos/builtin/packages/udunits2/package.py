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


class Udunits2(AutotoolsPackage):
    """Automated units conversion"""

    homepage = "http://www.unidata.ucar.edu/software/udunits"
    url      = "https://www.gfd-dennou.org/arch/ucar/unidata/pub/udunits/udunits-2.2.24.tar.gz"

    variant("shared", default=True, description="Enabled shared libs")
    version('2.2.24', '898b90dc1890f172c493406d0f26f531')
    version('2.2.23', '9f66006accecd621a4c3eda4ba9fa7c9')
    version('2.2.21', '1585a5efb2c40c00601abab036a81299')

    depends_on('expat')
    depends_on('libxml2')
    depends_on("libbsd")

    def configure_args(self):
        xml_libs = find_libraries("libxml2", self.spec["libxml2"].prefix.lib, shared=False)
        expat_libs = find_libraries("libexpat", self.spec["expat"].prefix.lib, shared=False)
        bsd_libs = find_libraries("libbsd", self.spec["libbsd"].prefix.lib, shared=False)
        libs = (expat_libs + xml_libs + bsd_libs)
        args = ["LIBS={0}".format(libs.ld_flags)]
        if "~shared" in self.spec:
            args.append("--disable-shared")

        return args
