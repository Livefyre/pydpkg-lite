from setuptools import setup

__version__ = 0.1

setup(
    name='pydpkg-lite',
    version=__version__,
    description="Lite version of Greg Perkins' pydpkg",
    keywords='dpkg, deb',
    author='Gene Hallman',
    author_email='gene@livefyre.com',
    url='https://github.com/genehallman/pydpkg-lite',
    license='BSD',
    scripts=['src/dpkg.py']
)
