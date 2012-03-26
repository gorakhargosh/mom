RM = rm -rf

PKG_NAME=mom

.PHONY: all clean distclean develop lint test upload-doc view-doc doc docs build dist release auto submodules push push-github push-google

all: build

help:
	@echo "Possible targets:"
	@echo "    test        - run testsuite"
	@echo "    doc(s)      - builds the documentation"
	@echo "    view-doc    - opens documentation in the browser"
	@echo "    upload-doc  - uploads the documentation to PyPI"
	@echo "    develop     - set up development environment"
	@echo "    clean       - clean up generated files"
	@echo "    release     - performs a release"
	@echo "    auto        - continuous builds"
	@echo "    push        - 'git push' to all hosted repositories"

release: clean test upload-doc
	python setup.py sdist upload

dist: clean
	python setup.py sdist

build: doc
	@bin/python setup.py build

doc-rebuild:
	@make -C docs/ clean
	@make SPHINXBUILD=../bin/sphinx-build -C docs/ html

docs: doc

doc: # develop
	@make SPHINXBUILD=../bin/sphinx-build -C docs/ html

upload-doc: doc
	@bin/python setup.py upload_docs --upload-dir=docs/build/html

view-doc: doc
	@bin/python -c "import webbrowser; webbrowser.open('docs/build/html/index.html')"

test: doc-rebuild
	@echo "You will need Coverage 3.5 and unittest2 or higher for this to work."
	@rm -rf htmlcov
	@bin/coverage erase
	@py.test -n4 --cov mom --cov-report html

lint:
	@-pylint $(PKG_NAME)

auto: tools/nosy.py
	@bin/python tools/nosy.py .

# Development environment targets and dependencies.
develop: submodules bin/python

submodules:
	@git submodule update --init --recursive

bin/buildout: buildout.cfg setup.py
	@python tools/bootstrap.py --distribute

bin/python: bin/buildout
	@bin/buildout

push: push-github push-google

push-github:
	@echo "Pushing repository to remote:github [github.com]"
	@git push github master

push-google:
	@echo "Pushing repository to remote:google [code.google.com]"
	@git push google master

clean:
	@make -C docs/ clean > /dev/null
	@$(RM) build/ *.egg-info/
	@find . \( \
		-iname "*.pyc" \
		-or -iname "*.pyo" \
		-or -iname "*.so" \
		-or -iname "*.o" \
		-or -iname "*~" \
		-or -iname "._*" \
		-or -iname "*.swp" \
		-or -iname "Desktop.ini" \
		-or -iname "Thumbs.db" \
		-or -iname "__MACOSX__" \
		-or -iname ".DS_Store" \
		\) -delete

distclean: clean
	@$(RM) \
		dist/ \
		bin/ \
		develop-eggs/ \
		eggs/ \
		parts/ \
		MANIFEST \
		htmlcov/ \
		.pythoscope/ \
		.coverage \
		.installed.cfg
