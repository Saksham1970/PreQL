from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
  name = 'preql',         # How you named your package folder (MyLib)
  packages = ['preql'],
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='mit',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple python-mysql linker.',
  long_description=long_description,
  long_description_content_type='text/markdown',   
  author = 'Saksham Gupta',                   # Type in your name
  author_email = 'saksham1970@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Saksham1970/mysql_database',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Saksham1970/mysql_database/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Sql',"Mysql","database","preql","prequal"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'mysql-connector',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
      ],
)