# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help html clean clean_unneeded

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
clean html: source/intro/architecture.svg clean_unneeded
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

source/intro/architecture.svg: source/intro/PJPROJECT\ 2.0\ Architecture.svg
	cd source/intro && python3 fix_svg_link.py

was_clean_unneeded:
	@for d in pjlib pjlib-util pjnath pjmedia pjsip; do \
	  rm -f "source/api/generated/$${d}/grouplist.rst"; \
	done
