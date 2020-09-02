import io, os
from setuptools import setup

# Package meta-data.
NAME = 'MondayClient'
DESCRIPTION = 'A client to query Monday.com v2 API'
URL = 'https://github.com/lalondesteve/MondayClient/'
EMAIL = 'lalondesteve@gmail.com'
AUTHOR = 'Steve Lalonde'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'
REQUIRED = [
    'requests', 'wheel', 'python-dotenv'
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(name=NAME,
      version='0.1',
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license='MIT',
      packages=['MondayClient'],
      install_requires=REQUIRED,
      include_package_data=True,
      zip_safe=False,
      classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Development Status :: 3 - Alpha',
      ],
      )
