from setuptools import setup, find_packages

setup(
    name="log2ml_toolchain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "linformer-pytorch>=0.1.0",
        "tokenizers>=0.15.0",
        "pandas>=2.0.0",
        "pyarrow>=14.0.1",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "flake8>=7.0.0",
        ],
    },
    python_requires=">=3.11",
    author="norandom",
    description="A tool for converting log files into machine learning-ready vector representations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/norandom/log2ml_toolchain",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
