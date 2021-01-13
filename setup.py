from setuptools import find_packages, setup

setup(
    name='arvancloud-ddns',
    version='0.1.0',
    description='DDNS script to sync public IP address to ArvanCloud dns records',
    author='Touhid arastu',
    author_email='touhid.arastu@gmail.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    license='MIT',
    keywords='arvancloud ddns',
    install_requires=[
        'requests',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'arvancloud-ddns = arvancloud_ddns.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
