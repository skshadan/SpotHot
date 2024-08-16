from setuptools import setup, find_packages

setup(
    name='spothot',
    version='2.6',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
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
