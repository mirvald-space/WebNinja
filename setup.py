from setuptools import setup, find_packages

setup(
    name="web-intel-agent",
    version="0.1.0",
    description="A standalone web agent based on Playwright and LLM",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.30.0",
        "requests>=2.28.1",
        "python-dotenv>=0.21.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)