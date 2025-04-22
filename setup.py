from setuptools import setup, find_packages

setup(
    name="human-typing-simulator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyautogui>=0.9.53",
        "numpy>=1.21.0",
        "tk>=0.1.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A realistic human typing simulator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/human-typing-simulator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "typing-simulator=src.cli:main",
        ],
    },
)
