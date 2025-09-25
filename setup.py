from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-client-python",
    version="1.0.0",
    author="Aneesh Puttur",
    author_email="aneeshkp@gmail.com",
    description="A flexible Python client for the Model Context Protocol (MCP)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aneeshkp/mcp-client-python",
    project_urls={
        "Bug Tracker": "https://github.com/aneeshkp/mcp-client-python/issues",
        "Documentation": "https://github.com/aneeshkp/mcp-client-python/blob/main/docs/usage.md",
        "Source": "https://github.com/aneeshkp/mcp-client-python",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=1.0",
            "pytest-cov>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-client=mcp_client.cli:main",
        ],
    },
)
