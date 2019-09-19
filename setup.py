from setuptools import setup, find_packages

setup(
    name="carlae",

    version="0.0.2",
    
    author="Benny Chin",
    author_email="wcchin.88@gmail.com",

    packages=['carlae', 'carlae.themes', 'carlae.docdata'],

    include_package_data=True,

    #url="https://github.com/wcchin/pyreveal",

    license="LICENSE",
    description="a dead simple project page generator",

    long_description=open("README.md").read(),
    
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'Topic :: Documentation',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],

    keywords='markdown, static site generator, jinja2',

    install_requires=[
        "jinja2",
        "markdown",
        "pyyaml", 
        "watchdog",
    ],
    entry_points = {
        "console_scripts": ['carlae = carlae.carlae:main']
        },
)
