SHELL := /bin/bash
.PHONY : all package install uninstall

all :

package : ale.py MANIFEST.in README.md setup.py
	python setup.py sdist

install : dist/ALE-0.1dev.tar.gz
	sudo pip install dist/ALE-0.1dev.tar.gz

uninstall : dist/ALE-0.1dev.tar.gz
	yes | sudo pip uninstall ale

