from os.path import join, dirname

from setuptools import setup, find_packages


def get_version():
    fname = join(dirname(__file__), "src/excel_comment_orm/__version__.py")
    with open(fname) as f:
        ldict = {}
        code = f.read()
        exec(code, globals(), ldict)  # version defined here
        return ldict['version']


setup(name='excel_comment_orm',
      version=get_version(),
      description='',
      long_description=open('README.md').read().strip(),
      author='Piti Ongmongkolkul',
      author_email='piti118@gmail.com',
      url='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      py_modules=['excel_comment_orm'],
      install_requires=[
          'openpyxl',
          'pyyaml',
          'stringcase'
      ],
      extras_require={
          'dev': [
              'ipykernel',
              'mypy',
              'autopep8',
              'pytest',
              'pytest-cov'
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
