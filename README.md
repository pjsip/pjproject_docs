# docs.pjsip.org Project

## Overview

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



### Generation Process

1. First of all, the `pjproject` submodule in `docs/source/pjproject` needs to be updated
   to the correct version using `git pull`. In RTD build server, this is done automatically.
2. When you run Sphinx's `make doc`, or when building the doc in RTD server, the following processes happen:
    i. doxygen is run by `conf.py`. This outputs XML files in various `pjproject/**/docs` directories.
    ii. Then `breathe-apidoc` is run by `conf.py`. This script reads Doxygen's XML files and outputs
      `.rst` documentation for all files, groups, classes etc in `docs/api/generated` directory.
    iii. Sphinx then processes the `.rst` files and build a nice documentation.

## Installation

### 1. Install Doxygen 1.8.4


Doxygen 1.5.1 is not suitable for Breathe.

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

## Generating Documentation

### Pull pjproject source

There is a pjproject submodule in `docs/source/pjproject` directory. 
Pull this pjproject submodule according to the version which documentation is to be built.
E.g. if you're building the latest docs, then you can just pull the latest source.
Otherwise pull to the relevant version.

You may also need to checkout to different branch than the master. This is totally
up to you. 

```sh
$ cd docs/source/pjproject
$ git pull
$ git checkout pjsip_docs
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

The result is `docs/build/html/index.html`. 

## Guides

For reference:

- https://docs.readthedocs.io/en/stable/index.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- https://breathe.readthedocs.io/en/latest/index.html
- https://breathe.readthedocs.io/en/latest/readthedocs.html

