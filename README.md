# docs.pjsip.org Project

## Overview

This repository holds the `.rst` files for docs.pjsip.org site. The Doxygen html files
are generated on the fly.

The main documentation files are in `docs` folder. Inside, there are `source` and `build`
folders. These directory layout conforms to Sphinx layout, i.e. `source` is the *source*, 
and `build` is for the output files.

Inside the `docs/source` folder, there is a Git submodule for `pjproject`. 


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

Pull pjproject according to the version which documentation is to be built.
If you're building the latest docs, then you can just pull the latest source.
Otherwise pull to the relevant version.

You may also need to checkout to different branch than the master. This is totally
up to you. 

```sh
$ cd source/pjproject
$ git pull
$ git checkout pjsip_docs
```


### Generate the Docs

```
$ cd docs
$ generate
$ make html
```

The output is `build/html/index.html`



## Guides

For reference:

- http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- https://breathe.readthedocs.io/en/latest/index.html

