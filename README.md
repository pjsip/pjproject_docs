# docs.pjsip.org Project

## Overview

### Overview of the documentation infrastructure

The PJSIP docs at **https://docs.pjsip.org** is hosted by the *Read the Docs* (RTD) service. It contains:
1. reference manuals (was at [pjsip.org/docs/latest/...](https://www.pjsip.org/docs/latest/pjlib/docs/html/index.htm)
2. pjsua2 book (was at [pjsip.org/docs/book-latest](https://www.pjsip.org/docs/book-latest/html/index.html))
3. (TODO) wiki (previously at https://trac.pjsip.org/repos/) 

The PJSIP's RTD settings page is at https://readthedocs.org/projects/pjsip/. This page controls various aspects of the RTD page. Some will be explained below.

The documentation repository is at https://github.com/pjsip/pjproject_docs. You are reading the README
of that repository.


### Contents

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
- `readthedocs.yml`: configuration for generating live RTD.
- `requirements.txt`: Python modules required to build the docs
- `Dockerfile`: to build Docker image.


### Overview of the generation process

There are three methods to build PJSIP RTD docs: 
1. In the RTD server. This method is the simplest, and it's intended for routine operations such as
   releasing new version or minor editing of the documentation.
2. (locally) using provided Docker image. This is the preferred method for authoring/developing the
   documentation.
3. (locally) using manual installation, if you don't want to use the Docker image, or if you need
   to understand how the Docker image is built.


## Method 1: managing live documentation

Use this method to perform routine tasks such as releasing new PJSIP version or editing of the documentation.

This method doesn't require any software except git and text editor. In fact, you don't even need those as you can edit the files directly on GitHub (but this is not recommended).

The live (RTD) docs in https://docs.pjsip.org are generated automatically whenever changes are pushed to the `pjproject_docs` repository (note: not the *pjproject* repository!). So remember that every commit will trigger costly build in RTD.

You can see the live building process, as well as logs of all previous build processes from the **Builds** page (https://readthedocs.org/projects/pjsip/builds/). This comes handy when the build failed to investigate what went wrong.

You can also manually trigger rebuilding of the doc by clicking **Build Version** from that page, but this shouldn't be necessary unless you modify something in the RTD settings and want to regenerate the docs.

### Editing documentation

Just pull *pjproject_docs* to your computer, edit, commit, and push the files. Once the files are pushed to GitHub, this will trigger a build process in RTD.

### Creating new documentation version for a new PJSIP release

Follow the instructions in [Versioning the documentation](#versioning-the-documentation) section below.

## Method 2: Using the Docker image

We've provided an Ubuntu 22.04 Docker image that contains all the required software to develop the
docs. It is equipped with two nice editors, **vim** and **tilde**, and it even contains pre-built
documentation to get you started.

Below are steps to use this method.

### Install Docker

Follow the installation instructions on https://www.docker.com/get-started/ to install Docker on
your system (Linux, Mac, or Windows).

### Pull and run pjproject-docs image

```
$ docker pull pjsip/pjproject-docs
$ docker run -dit -p 8000:8000 --name=pjproject-docs pjsip/pjproject-docs
```

### Viewing local RTD

Point your browser to http://localhost:8000 to view RTD served by the Docker container.

### Open terminal to the Docker container

```
$ docker exec -it pjproject-docs bash
```

The next section explains how to edit and generate the docs.

### Editing the docs

(In the Docker container terminal)

1. Go to `/root/pjproject_docs` directory to edit the files, rebuild the documentation etc. 
   as explained in the next section (**Generating Documentation Locally**)
   - Note: The container contains two nice text editors: **vim** and **tilde**. 
     You may of course install other editors (or any other software, for that matter) 
     using `apt-get install` as usual.
2. The HTTP server is served by `python3 -m http.server` background process. It automatically
   serves the latest generated HTML files in `docs/build/html` directory.


## Generating documentation locally

The Docker container already contains cloned repository of the `pjproject-docs` in
`/root/pjproject-docs`. You can pull, add, edit, modify, and push this repository as usual.

Below are steps to generate the docs. Perform these steps in the Docker container terminal.

### Git pull

```sh
$ cd pjproject_docs
$ git pull --recurse-submodules
$ git submodule update --remote
```

Note:

- if directory `source/pjproject` is still empty, run:

```
$ git submodule update --init --recursive
```

### Update requirements

New Python modules may be added to requirements after the docker image is created, so let's
make sure all required Python modules are installed.

```cmd
$ pip install -r requirements.txt
```

### Generate the docs

#### 1. Set environment variable

The `READTHEDOCS` environment variable is used to control whether Doxygen XML and *breathe*
API docs needs to be regenerated. You need to set it to generate docs for different PJPROJECT
versions. On the other hand, when you only edit the `.rst` files, there is no need to regenerate
the Doxygen files, so unset it (`unset READTHEDOCS`). 

To set the value:
```
$ export READTHEDOCS=True
``` 


#### 2. Build the docs

```sh
$ cd docs
$ make clean html
```

The result is `docs/build/html/index.html`. Now refresh the http://localhost:8000 page in the host
computer to view the updated docs.

## How it works

This section is just for information. 

When running Sphinx's `make html`, or when building the doc in RTD server, the following processes happen:

* `docs/source/conf.py` is read by sphinx
* if `READTHEDOCS` environment variable is set to True, `doxygen` is run by `conf.py`. This outputs Doxygen XML files in various `pjproject/**/docs` directories.
* `breathe-apidoc` is run by `conf.py`. This script reads Doxygen's XML files and outputs
  `.rst` documentation for all files in `docs/source/api/generated` directory.
* Sphinx then processes the `.rst` files and build a nice documentation.


## Versioning the documentation

RTD supports multiple versions of the docs. It does so by analyzing the Git *tags* of the **pjproject_docs** repository.

By default, RTD only supports `latest` version of the doc, which corresponds to latest commit in Git `master` (again, of the `pjproject_docs` repository). If you wish to show the individual version, activate the version from https://readthedocs.org/projects/pjsip/versions/.

For more info please see https://docs.readthedocs.io/en/stable/versions.html

Follow the steps below to create documentation for specific PJSIP version.

### Creating new documentation version

#### 1a: get the source

Pull the docs:

```sh
$ cd pjproject_docs
$ git pull
```

#### 1b: get the source (for Docker installation)

Open terminal to the Docker container

```
$ docker exec -it pjproject-docs bash
```

All the remaining steps are done in the the terminal to the Docker container.

Pull the docs:

```sh
$ cd pjproject_docs
$ git pull --recurse-submodules
$ git submodule update --remote
```

Note:

- if directory `source/pjproject` is still empty, run:

```
$ git submodule update --init --recursive
```

Set READTHEDOCS environment variable:

Bash:
```
$ export READTHEDOCS=True
``` 

#### 2. Set which PJPROJECT version to build

1. Edit `docs/source/conf.py` (note: use **tilde** or **vim**)
2. Modify **`pjproject_tag`** to match the PJPROJECT Git **tag** which documentation is to be built. Example:
   ```python
   pjproject_tag = '2.10'
   ``` 
3. Save and close


#### 3. Optional: build the docs locally

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


### Restoring documentation for latest master

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


### (Only for local installation) Cleaning generated files

To clean up the `build` directory:

```
$ cd docs
$ make clean
```

## Method 3: Manual installation

These are for generating the docs locally if you do not wish to use the Docker image
(note for RTD, the required installations are already specified in `readthedocs.yml`
and `requirements.txt`). 

Note that local installation is not required for releasing new documentation version (new pjproject version). You only need a text editor for that.

Also note that these are only tested on Linux at the moment, and Windows will not work
(because `conf.py` calls `./configure` to initialize the macros). Mac may work but untested.


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


#### 5. Check installation

Check that the tools are available on the PATH by running the following:

```
$ doxygen -v
$ sphinx-build --version
$ breathe-apidoc --version
```


## Generating Docker image

### Install requirements

Install the required software as explained in **Manual Installation** section above.

### Fetch and generate documentation locally

Follow the instructions in **Generate the Docs** section above.
The objective is to copy this generated documentation to the Docker image file
so that the image doesn't have to start from scratch.


### Build the Docker image

```
$ cd pjproject_docs
$ docker build --tag pjproject-docs .
```

### Test the image

Run a Docker container from the image with `docker run` (see above).

### Tag and upload the image

This is for PJSIP team to upload the image to Docker hub repository:

```
$ docker tag pjproject-docs pjsip/pjproject-docs
$ docker login
$ docker push pjsip/pjproject-docs
```

## Cheatsheet

Image related commands:

```
docker build --tag pjproject-docs .
docker image ls
docker image rm pjproject-docs
```

Container related commands:

```
docker run -dit -p 8000:8000 --name=pjproject-docs pjsip/pjproject-docs
docker ps
docker container ls
docker exec -it pjproject-docs bash
docker kill pjproject-docs
docker start pjproject-docs
docker container rm pjproject-docs
```

Repository related commands:

```
docker tag pjproject-docs pjsip/pjproject-docs
docker push pjsip/pjproject-docs
```

Service commands:

```
sudo service docker start
sudo systemctl start docker.socket
```

## More Info

For reference:

- https://docs.readthedocs.io/en/stable/index.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- https://breathe.readthedocs.io/en/latest/index.html
- https://breathe.readthedocs.io/en/latest/readthedocs.html

