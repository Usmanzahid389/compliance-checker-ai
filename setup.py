from setuptools import setup, find_packages

setup(
    name="compliance_checker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",  # For ChatGPT API integration
        "requests>=2.31.0",  # For API calls
        "python-dotenv>=1.0.0",  # For environment variable management
        "pydantic>=2.0.0",  # For data validation
    ],
    author="Your Organization",
    author_email="your.email@organization.com",
    description="A package for compliance checking using ChatGPT and sophisticated matching algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 