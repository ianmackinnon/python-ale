SHELL := /bin/bash
.PHONY : all package install uninstall test

all : dist/ALE-0.1dev.tar.gz

clean :
	rm -rf *.pyc dist MANIFEST build 

package : ale.py MANIFEST.in README.md setup.py
	python setup.py sdist

dist/ALE-0.1dev.tar.gz : package

install :
	sudo pip install dist/ALE-0.1dev.tar.gz

uninstall : dist/ALE-0.1dev.tar.gz
	yes | sudo pip uninstall ale

test : 
	cd test && ./read_test.py

