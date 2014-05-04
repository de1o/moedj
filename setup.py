from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='moedj',
    version='0.5.8',
    url='https://github.com/deloeating/moedj',
    license='MIT',
    author='delo',
    tests_require=['pytest'],
    install_requires=[
        'BeautifulSoup>=3.2.1',
        'redis>=2.8.0',
        'pytz>=2012d',
        'Django>=1.5.1',
        'pysqlite>=2.6.3',
        'requests>=2.2.1',
        'celery>=3.1.9',
        ],
    cmdclass={'test': PyTest},
    author_email='deloeating@gmail.com',
    description='A simple weibo bot for zh.moegirl.org',
    long_description=long_description,
    zip_safe=False,
    packages=find_packages("."),
    package_data={
        '': ['*.md'],
        'moedjpack': ['static/css/*.css', 'static/js/*.js',
                      'static/img/*', 'templates/*/*.html',
                      'templates/*.html'],
    },
    platforms='linux',
    entry_points={
        'console_scripts':
        ['mpserver=moedjpack.run:main',
         'mpcron=moedjpack.moepad.cron:main',
         'mpupdate=moedjpack.moepad.update:update',
         'mpsend=moedjpack.moepad.update:send',
         'delprefix=moedjpack.moepad.update:deletePrefix',
         'mplog=moedjpack.moepad.showstatus:showlog',
         'mpverify=moedjpack.moepad.showstatus:show_verifying',
         'mpsyncdb=moedjpack.moepad.mputils:create_default_db',
         ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
