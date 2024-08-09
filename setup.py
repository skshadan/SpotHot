from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import platform

class CustomInstallCommand(install):
    """Customized setuptools install command to install system packages."""
    def run(self):
        install.run(self)
        python_command = 'python3' if platform.system() != 'Windows' else 'python'
        subprocess.check_call([python_command, 'spothot/post_install.py'])

setup(
    name='spothot',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'spothot=spothot.main:main',
        ],
    },
    author='Shadan Khan',
    author_email='shadankhantech@gmail.com',
    description='A package to set up Raspberry Pi as a Wi-Fi hotspot',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/skshadan/spothot',  # Replace with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
