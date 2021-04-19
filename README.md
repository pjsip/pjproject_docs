# docs.pjsip.org Project

## Overview

### Overview of The Documentation Infrastructure

The PJSIP docs at **https://docs.pjsip.org** is hosted by the *Read the Docs* (RTD) service. It contains:
1. reference manuals (was at [pjsip.org/docs/latest/...](https://www.pjsip.org/docs/latest/pjlib/docs/html/index.htm)
2. pjsua2 book (was at [pjsip.org/docs/book-latest](https://www.pjsip.org/docs/book-latest/html/index.html))
3. (TODO) wiki (previously at https://trac.pjsip.org/repos/) 

The PJSIP's RTD settings page is at https://readthedocs.org/projects/pjsip/. Here you can control various aspects of the RTD page.

The documentation repository is at https://github.com/pjsip/pjproject_docs (you're reading the README of that repository).


### Directory Layout

- `docs/`
    - `source/`
        - `conf.py`: Sphinx conf
        - `*.rst`: hand-written documentation
        - `pjproject/`: Git submodule for pjproject
        - `api/`
            - `*.rst`: hand-written index files for API reference
            - `generated/`: output directory of `breathe-apidoc`
        - `pjsua2/`
            - `*.rst`: PJSUA2 book (was pjsip-book)



### Overview of Generation Process

There are two ways to build PJSIP RTD docs: locally, and in the RTD server. You build the docs locally only when developing the documentation itself, i.e. to preview the docs locally. 

For the live version, the docs are built in the RTD server, either triggered manually from the RTD settings page (above), or automatically every time someone commits **to the pjproject_docs repository** (i.e., not to the main *pjproject* repository!).

More will be explained in *Generating Documentation* section below.

## Installation

These are the installation instructions for generating the documentation locally. For RTD, the required installations are already specified in `readthedocs.yml` and `requirements.txt`. 

### 1. Install Doxygen 1.8.4

You need at least Doxygen 1.8.1 because Doxygen 1.5.1 is not suitable for Breathe.

### 2. Install other requirements

Install with this command:

```cmd
$ pip install -r requirements.txt
```
### 3. Check Installation

Check that the following tools are available on the PATH:

```
$ doxygen -v
$ sphinx-build --version
$ breathe-apidoc --version
```

## Generating Documentation Locally

You build docs locally when you modify the docs (such as releasing new version, modifying
the content) in order to test it locally first before updating the live docs. 

Here are the steps to do it. Make sure you have followed the steps in *Installation* above.

### Pull pjproject source

There is a `pjproject` submodule in `docs/source/pjproject` directory.

The first time after you clone `pjproject_docs`, you need to pull the submodules with
the following command in the `pjproject_docs` directory:

```sh
$ git submodule update --init --recursive
```

Subsequently, use this when updating `pjproject_docs` to pull the submodules:

```sh
$ git pull --recurse-submodules
```

### Generate the Docs

#### 1. Set environment variable:

Bash:
```
$ export READTHEDOCS=True
``` 

Windows:
```
C:> SET READTHEDOCS=True
```

Note: setting the `READTHEDOCS` environment variable causes the build system to 
regenerate Doxygen XML and breathe API docs. As long as the source doesn't change,
this only needs to be done once. Unset `READTHEDOCS` env var to disable these 
Doxygen and breathe API execution.

#### 2. Build

```
$ cd docs
$ make html
```

The result is `docs/build/html/index.html`. You can previous the result in the browser.

#### Notes

Just for information, when running Sphinx's `make html`, or when building the doc in RTD server, the following processes happen:
* doxygen is run by `conf.py`. This outputs XML files in various `pjproject/**/docs` directories.
* `breathe-apidoc` is run by `conf.py`. This script reads Doxygen's XML files and outputs
  `.rst` documentation for all files in `docs/source/api/generated` directory.
* Sphinx then processes the `.rst` files and build a nice documentation.


## Generating Live Documentation

The live (RTD) docs in https://docs.pjsip.org are generated automatically when someone commits
anything to the `pjproject_docs` repository. Alternatively, you can manually trigger rebuilding
of the doc from the PJSIP's RTD settings page. 

## Releasing New Version

First read how versioning is done in RTD: https://docs.readthedocs.io/en/stable/versions.html

Here's how to release new version for PJSIP docs:

1. Checkout


## Guides

For reference:

- https://docs.readthedocs.io/en/stable/index.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- https://breathe.readthedocs.io/en/latest/index.html
- https://breathe.readthedocs.io/en/latest/readthedocs.html

