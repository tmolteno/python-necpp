build:
	python3 setup.py sdist
	#python3 setup.py bdist_wheel
	
clean:
	rm -rf build
	rm -rf dist
	
test-upload:
	python3 -m pip install --user --upgrade twine

	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	python3 -m twine upload dist/*

test-install:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps PyNEC --upgrade
	
