# -*- coding: utf-8 -
#
# This file is part of speedydeploy released under the MIT license. 
# See the NOTICE for more information.

import os
import sys
from setuptools import setup, find_packages

from lfs_gallery import VERSION


setup(
    name='lfs_gallery',
    version=VERSION,

    description='Image Gallery for LFS',
    long_description=file(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author='Victor Safronovich',
    author_email='vsafronovich@gmail.com',
    license='MIT',
    url='http://github.com/suvit/lfs-gallery',
    zip_safe=False,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    install_requires=file(
        os.path.join(
            os.path.dirname(__file__),
            'requirements.txt'
        )
    ).read().split(),
    include_package_data=True,
)
