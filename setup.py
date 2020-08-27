from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'preql',         # How you named your package folder (MyLib)
  packages = ['preql'],
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='mit',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple python-mysql linker.',
  long_description=long_description,
  long_description_content_type='text/markdown',   
  author = 'Saksham Gupta',                   # Type in your name
  author_email = 'saksham1970@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Saksham1970/PreQL',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Saksham1970/PreQL/archive/v_02.tar.gz',    # I explain this later on
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