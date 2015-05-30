from setuptools import setup, find_packages

setup(
    name="broku",
    version="0.1",
    author="snare",
    author_email="snare@ho.ax",
    description=("A terrible terminal remote for Roku"),
    license="Buy snare a beer",
    keywords="",
    url="https://github.com/snare/broku",
    packages=find_packages(),
    install_requires=['roku', 'blessed', 'PyYAML'],
    package_data={'': ['keys.yaml']},
    entry_points={
        'console_scripts': ['broku=broku:main']
    }
)
