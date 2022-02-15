from setuptools import setup, find_packages
from codecs import open
from pathlib import Path
import os


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="stratocumulus",
    use_scm_version=True,
    zip_safe=False,
    description="Stratocumulus is the backend component of Cumulus.",
    long_description=long_description,
    url="https://github.com/lilab-bcb/stratocumulus",
    author="Yiming Yang, Rimte Rocher, Bo Li",
    author_email="cumulus-support@googlegroups.com",
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        'Operating System :: Microsoft :: Windows',
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords="Cloud computing",
    packages=find_packages(),
    setup_requires=["setuptools_scm"],
    install_requires=[
        l.strip() for l in Path("requirements.txt").read_text("utf-8").splitlines()
    ],
    python_requires=">= 3",
    entry_points={"console_scripts": ["strato=strato.__main__:main"]},
)
