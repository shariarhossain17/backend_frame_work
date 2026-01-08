

import io
import os

from setuptools import find_packages, setup

# Package meta-data 
NAME = "code_hacker"  
DESCRIPTION = "code_hacker web Framework built for learning purposes."
EMAIL = "shariarhossain23@gmail.com"  
AUTHOR = "Shahriar Hossain"  
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"

# Framework dependencies
REQUIRED = [
    "Jinja2==3.1.2",
    "parse==1.19.0", 
    "requests==2.28.1",
    "requests-wsgi-adapter==0.4.1",
    "WebOb==1.8.7",
    "whitenoise==6.2.0",
]

# Advanced setup configuration
here = os.path.abspath(os.path.dirname(__file__))


try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load version information
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

# Main setup configuration
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["test_*"]),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    setup_requires=["wheel"],
)
