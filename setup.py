from setuptools import setup
from setuptools import find_packages
from os.path import join

package_name = 'waypoint_editor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        (join('share', package_name), ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'launch',
        'launch_ros'
    ],
    zip_safe=True,
    author='Stevie Dale',
    author_email='sdale4@asu.edu',
    maintainer='Stevie Dale',
    maintainer_email='sdale4@asu.edu',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Package containing first attempt at making python package.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'waypoint_editor = src.waypoint_editor:main',
        ],
    },
)
