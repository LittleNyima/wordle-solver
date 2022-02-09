from setuptools import setup, find_packages

setup(
    name="wordle-solver",
    version="0.0.2",
    description="Solver of Wordle, including a profiler",
    author="LittleNyima",
    author_email="littlenyima@163.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "ordered_set==4.1.0"
    ]
)