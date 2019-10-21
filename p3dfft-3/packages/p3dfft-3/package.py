# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install p3dfft-3
#
# You can edit this file again by typing:
#
#     spack edit p3dfft-3
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class P3dfft3(Package):
    """put a proper description of this  package here later."""

    homepage = "https://www.p3dfft.net"
    url      = "https://github.com/sdsc/p3dfft.3/archive/master.tar.gz"
    git = "https://github.com/sdsc/p3dfft.3"

    version('develop', branch = 'master')
    version('0.0.0', '3c62c2bdf4aa91c3f1ab122efc1b3799')

    variant('fftw', default = True,
            description='Builds with FFTW library')
    variant('essl', default=False,
            description='Builds with ESSL library')
    variant('mpi', default = True,
            description="Enable MPI support.")
    variant('openmp', default=False,
            description="Enable OpenMP support.")

    depends_on('mpi',when = '+mpi')
    depends_on('fftw',when = '+fftw')
    depends_on('essl',when = '+essl')
    depends_on('openmp',when = '+openmp')


    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        spack_env.set('CC', spec['mpi'].mpicc)
        spack_env.set('FC', spec['mpi'].mpifc)
        spack_env.set('CXX', spec['mpi'].mpicxx)

    def install(self, spec, prefix):
        config_args = ['--prefix={0}'.format(prefix)]

        if '+fftw' in spec:
            config_args.append('--enable-fftw')
            config_args.append ('--with-fftw-lib= %s' % spec['fftw'].prefix.lib)
            config_args.append ('--with-fftw-inc= %s' % spec['fftw'].prefix.include)

        if '+essl' in spec:
            config_args.append('--enable-essl')
            config_args.append ('--with-fftw-lib= %s' % spec['essl'].prefix.lib)
            config_args.append ('--with-fftw-inc= %s' % spec['essl'].prefix.include)

        configure( *config_args)

        make()
        make('install')
