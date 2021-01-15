install:
	pip install -e .

clean-build:
	rm -fR build/
	rm -fR dist/
	rm -fR *.egg-info

publish:
	python setup.py sdist
	twine upload dist/*
