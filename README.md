# docs.pjsip.org Project

## Overview

### Overview of The Documentation Infrastructure

The PJSIP docs at **https://docs.pjsip.org** is hosted by the *Read the Docs* (RTD) service. It contains:
1. reference manuals (was at [pjsip.org/docs/latest/...](https://www.pjsip.org/docs/latest/pjlib/docs/html/index.htm)
2. pjsua2 book (was at [pjsip.org/docs/book-latest](https://www.pjsip.org/docs/book-latest/html/index.html))
3. (TODO) wiki (previously at https://trac.pjsip.org/repos/) 

The PJSIP's RTD settings page is at https://readthedocs.org/projects/pjsip/. Here you can control various aspects of the RTD page. Some will be explained below.

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
    - `build/`: output files will be placed here



### Overview of Generation Process

There are two ways to build PJSIP RTD docs: locally, and in the RTD server. You build the docs locally only when developing the documentation itself, i.e. to preview the results locally. 

For the live version, the docs are built in the RTD server automatically whenever changes are pushed to **pjproject_docs** repository (note: not the *pjproject* repository!)


## Local Installation

These are for generating the docs locally. For RTD, the required installations are already specified in `readthedocs.yml` and `requirements.txt`. 

Note that local installation is not required for releasing new documentation version (new pjproject version). You only need a text editor for that. This will be explained in later section.

Also note that these are only tested on Linux at the moment. Macs should work, and Windows is supported in the codes, but both haven't been tested yet.


#### 1. Install Doxygen 1.8.4

You need at least Doxygen 1.8.1 because Doxygen 1.5.1 is not suitable for Breathe.

#### 2. Install Python

We need Python version 3.7 or newer. It's also recommended co create `virtualenv` environment to avoid cluttering your main Python installation.

#### 3. Clone pjproject_docs with the submodules

```sh
$ git clone https://github.com/pjsip/pjproject_docs.git
$ cd pjproject_docs
$ git submodule update --init --recursive
```

Note: the last command is for fetching the `pjproject` submodule in `docs/source/pjproject` directory.

#### 4. Install other requirements

Run this command (maybe inside your virtualenv) to install the required Python modules:

```cmd
$ pip install -r requirements.txt
```


#### 5. Check Installation

Check that the tools are available on the PATH by running the following:

```
$ doxygen -v
$ sphinx-build --version
$ breathe-apidoc --version
```

## Generating Documentation Locally

You build the docs locally when you are developing them in order to test locally first before updating the live docs.

Here are the steps to do it. Make sure you have followed the steps in *Installation* above. If you created a virtualenv environment, activate that environment.

### Git pull

Subsequently, to update `pjproject_docs` and the `pjproject` submodule:

```sh
$ cd pjproject_docs
$ git pull --recurse-submodules
```

### Generate the Docs

#### 1. Set environment variable

Bash:
```
$ export READTHEDOCS=True
``` 

Windows:
```
C:> SET READTHEDOCS=True
```

Note: setting the `READTHEDOCS` environment variable causes the build system to 
regenerate Doxygen XML and *breathe* API docs. If this is unset, *breathe* will generate 
documentation from existing Doxygen XML files. 

#### 2. Build

```sh
$ cd docs
$ make clean html
```

The result is `docs/build/html/index.html`. You can open this in the browser.

## How It Works

Just for information, when running Sphinx's `make html`, or when building the doc in RTD server, the following processes happen:
* `docs/source/conf.py` is read by sphinx
* if `READTHEDOCS` environment variable is set to True, `doxygen` is run by `conf.py`. This outputs Doxygen XML files in various `pjproject/**/docs` directories.
* `breathe-apidoc` is run by `conf.py`. This script reads Doxygen's XML files and outputs
  `.rst` documentation for all files in `docs/source/api/generated` directory.
* Sphinx then processes the `.rst` files and build a nice documentation.


## Building Live Documentation

The live (RTD) docs in https://docs.pjsip.org are generated automatically whenever changes are pushed to the `pjproject_docs` repository. 

You can see the live building process, as well as logs of all previous build processes from the **Builds** page (https://readthedocs.org/projects/pjsip/builds/). This comes handy when the build failed to investigate what went wrong.

You can also manually trigger rebuilding of the doc by clicking **Build Version** from that page, but this shouldn't be necessary unless you modify something in the RTD settings and want to regenerate the docs.


## Versioning the Documentation

RTD supports multiple versions of the docs. It does so by analyzing the Git *tags* of the **pjproject_docs** repository.

As an overview, by default RTD only supports `latest` version of the doc, which corresponds to latest commit in Git `master`. If there is a Git tag in the repository, RTD will create `stable` version of the doc, which corresponds to the latest Git tag of the repository. If you wish to show the individual version, activate the version from https://readthedocs.org/projects/pjsip/versions/.

For more info please see https://docs.readthedocs.io/en/stable/versions.html

Follow the steps below to create new documentation version.

### Creating New Documentation Version

#### 1. Git pull 

```sh
$ cd pjproject_docs
$ git pull --recurse-submodules
```

#### 2. Set READTHEDOCS environment variable

Bash:
```
$ export READTHEDOCS=True
``` 

Windows:
```
C:> SET READTHEDOCS=True
```

#### 3. Set which PJPROJECT version to build

1. Edit `docs/source/conf.py`
2. Modify **`pjproject_tag`** to match the PJPROJECT Git **tag** which documentation is to be built. Example:
   ```python
   pjproject_tag = '2.10'
   ``` 
3. Save and close


#### 3b. Optional: build the docs locally

You need to have local installation to do this. Build the docs by running these:

```sh
$ cd docs
$ make clean html
```

Then open `docs/build/html/index.html` to preview the result.

#### 4. Git commit (but don't push yet)

```sh
$ cd pjproject_docs
$ git add -u
$ git commit -m 'Setting pjproject version to 2.10'
```


#### 5. Tag pjproject_docs

```sh
$ git tag 2.10
```

#### 6. Git push with tags

Push the tags first then the code.

```sh
$ cd pjproject_docs
$ git push --tags
$ git push
```

The last command would trigger a building process for version `latest` in RTD. 

#### 7. See the building process

Open https://readthedocs.org/projects/pjsip/builds/, there should be one that is currently 
building (i.e. for `latest` version).

You may wait until it is finished (it will take approximately 15 minutes) to make sure that 
everything is okay, or otherwise continue to the next steps (but it will cause more than one 
build processes to be started by RTD, which is okay).

#### 8. Activate the version

Go to https://readthedocs.org/projects/pjsip/versions/, and activate the new version and make it active and public.

This will trigger a new build process for that version.

#### 9. Wait the build process

Wait until all build processes are finished.


### Creating documentation for latest master

After a version is released, if you want to generate a documentation for the latest *master*
(i.e. before next version is released), you need to do the following.

#### 1. Set PJPROJECT version to *master*

1. Edit `docs/source/conf.py`
2. Set **`pjproject_tag`** `master`, e.g.:
    ```python
   pjproject_tag = 'master'
   ``` 
3. Save and close

#### 2. Commit and Push

```sh
$ cd pjproject_docs
$ git add -u
$ git commit -m ..
$ git push
```

Note that **you must not add any tags** to the `pjproject_docs` repository.

#### 3. Watch the building process

There should be a build process for the *latest* version.


### Handling errors

If the building fails, these are the steps to recreate the documentation.

1. Investigate the error by looking at the build logs (in the Builds page)
2. Fix the error.
3. If the error is in the `latest` version, you just need to commit, push, and watch the building process in RTD.
4. If the error is in the tagged version (e.g. `2.10`, etc.), then you need to delete the tag first:

   ```sh
   $ git tag -d <the tag>
   $ git push --delete origin <the tag>
   ``` 


### Cleaning generated files

To clean up the `build` directory:

```
$ cd docs
$ make clean
```


## More Info

For reference:

- https://docs.readthedocs.io/en/stable/index.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- https://breathe.readthedocs.io/en/latest/index.html
- https://breathe.readthedocs.io/en/latest/readthedocs.html

