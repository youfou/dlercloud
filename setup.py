import sys

import setuptools
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.md', 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name='dlercloud',
    version='0.0.8',
    author='Youfou',
    author_email='youfouzz@gmail.com',
    description='A Python Wrapper for DlerCloud API',
    keywords=[
        'DlerCloud',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/youfou/dlercloud',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
