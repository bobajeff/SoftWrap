# Copyright (C) 2021 Jean Da Costa machado.
# Jean3dimensional@gmail.com
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, Extension
from Cython.Build import cythonize
from distutils.util import get_platform
import re
from sys import argv
from os import path

debug = 'debug' in argv
if debug:
    argv.remove('debug')

platf = get_platform().lower()
print(f'compiling for platform: {platf}')
if 'linux' in platf:
    extra_compile_args = ['-ffast-math', '-fopenmp', '-O3'] + (['-g3'] if debug else [])
    extra_link_args = ['-fopenmp'] + (['-g3'] if debug else [])

elif 'win' in platf:
    extra_compile_args = ['/O2', '/openmp', '/fp:fast'] + (['/debug'] if debug else [])
    extra_link_args = ['/openmp'] + (['/debug'] if debug else [])

else: # mac
    extra_compile_args = ['-ffast-math', '-O3', '-std=c++2a'] + (['-g3'] if debug else [])
    extra_link_args = ['-g3'] if debug else []


modules = cythonize(
    Extension(
        'softwrap_core',
        ['core/core2.pyx'],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        include_dirs=["core"]
    )
)

setup(
    name='softwrap_core',
    ext_modules=modules
)
