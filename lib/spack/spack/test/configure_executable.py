"""
Tests for configure executable. The only special case is on Cray platforms.
Every other platform should have configure working the same way.
"""
import os
import pytest
import shutil
import tempfile
import unittest

from llnl.util.filesystem import join_path
import spack.architecture
from spack.build_environment import ConfigureExecutable
from spack.util.environment import path_put_first


@pytest.mark.usefixtures('mock_modulecmd')
class ConfigureExecutableTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        conf_exe = join_path(self.tmpdir, "configure")
        with open(conf_exe, "w") as c:
            c.write("#!/bin/sh\n")
            c.write("echo $@")
        os.chmod(conf_exe, 0o700)

        path_put_first("PATH", [self.tmpdir])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_configure(self):
        # In our test platform running normal is building for the frontend.
        arch = spack.architecture.arch_for_spec("test-redhat6-x86_32")
        configure = ConfigureExecutable("configure", arch)
        self.assertEqual(configure("--prefix=install/path", output=str).strip(),
                         "--prefix=install/path")
