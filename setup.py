from os.path import join, dirname

from setuptools import setup, find_packages


def get_version():
    fname = join(dirname(__file__), "src/exco/__version__.py")
    with open(fname) as f:
        ldict = {}
        code = f.read()
        exec(code, globals(), ldict)  # version defined here
        return ldict['version']


setup(name='exco',
      version=get_version(),
      description='Excel Comment Orm',
      long_description=open('README.md').read().strip(),
      long_description_content_type='text/markdown',
      author='Piti Ongmongkolkul',
      author_email='piti118@gmail.com',
      url='https://github.com/thegangtechnology/exco',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      py_modules=['exco'],
      entry_points={
          'console_scripts': ['exco_watch=exco.exco_watch:ExcoWatch.main'],
      },
      install_requires=[
          'openpyxl',
          'pyyaml',
          'stringcase',
          'watchdog'
      ],
      extras_require={
          'dev': [
              'ipykernel',
              'mypy',
              'autopep8',
              'pytest',
              'pytest-cov',
              'wheel'
          ],
          'test': [
              'pytest',
              'pytest-cov'
          ]
      },
      license='Private',
      zip_safe=False,
      keywords='',
      classifiers=[''])
