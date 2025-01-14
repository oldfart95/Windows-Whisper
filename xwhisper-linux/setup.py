from setuptools import setup, find_packages
import os

# Get the directory containing this file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Read requirements from requirements.txt
requirements_path = os.path.join(base_dir, 'requirements.txt')
with open(requirements_path) as f:
    requirements = f.read().splitlines()

setup(
    name='xwhisper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'xwhisper=speech_engine:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['assets/*'],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    data_files=[
        ('share/applications', ['xwhisper.desktop']),
        ('share/icons/hicolor/256x256/apps', ['assets/icon.png']),
    ],
)