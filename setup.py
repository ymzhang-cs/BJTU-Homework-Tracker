from setuptools import setup, find_packages
from version import __version__

setup(
    name='bjtu_homework_tracker',  
    version=__version__,      
    packages=find_packages(),  
    install_requires=[  
        'requests',  
        'selenium',
        'chromedriver-autoinstaller',
        'edgedriver-autoinstaller',
        'beautifulsoup4',
        'pyyaml'
    ],
    description='A package for tracking homeworks in BJTU',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Yuanming Zhang',
    author_email='ymzhang.cs@gmail.com',
    url='https://github.com/ymzhang-cs/BJTU-Homework-Tracker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
