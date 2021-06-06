from setuptools import setup, find_packages
import re
import io

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='re-manga',
    version='0.0.2',
    author='Varun Panchal',
    author_email='varunpanchal283@gmail.com',
    description='Get your favourite manga in pdf',
    packages=find_packages(),
    url='https://github.com/varunpanchal283/re-manga',
    keywords=['anime', 'manga' ,'downloader', 'manga bulk downloader', 'download', 'mangadex'],

    long_description=long_description,
    long_description_content_type='text/markdown',

	install_requires=[
	        'beautifulsoup4==4.9.3',
	        'requests==2.25.1',
	        'PyInquirer==1.0.3',
	        'prettytable==2.1.0',
	        'img2pdf==0.4.1',
            'pyfiglet==0.8.post1'
	],

	entry_points={"console_scripts": ["re-manga=remanga.__main__:main"]},
)