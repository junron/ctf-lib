from setuptools import setup, find_packages

setup(name='ctflib',
      version='3.1.2',
      description='[PRIVATE] Tools for speeding up CTFing',
      author='jro',
      install_requires=["z3-solver", "aiohttp", "requests", "beautifulsoup4", "pwntools", "click"],
      entry_points={
            'console_scripts': [
                  'ctf = ctflib.scripts.main:cli',
            ],
      },
      packages=find_packages())
