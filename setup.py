from setuptools import setup, find_packages

setup(
    name='scorpiui',
    version='0.0.1',
    author='Gemechis Chala (ScorpiDev)',
    author_email='venopyx@gmail.com',
    description='ScorpiUI: A Python UI library for building web apps with minimal HTML, CSS, and JS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/venopyx/scorpiui',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='ui library python web development',
    python_requires='>=3.6',
    install_requires=[
        'Flask>=2.0',
        'Jinja2>=3.0',
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/venopyx/scorpiui/issues',
        'Source': 'https://github.com/venopyx/scorpiui',
    },
)
