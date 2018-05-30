default: run

run:
	python3 aquachain-kv

deps:
	pip3 install --user -r requirements.txt
	python3 setup.py install --user
	garden install qrcode

test:
	python3 setup.py test

clean:
	rm -rf aquachain-kv.egg-info
	rm -rvf *.pyc */*.pyc */__pycache__ || true
	rm -rvf *.ini || true
	python3 setup.py clean

help:
	@printf 'aquachain gui wallet builder\n\n'
	@printf 'available targets:\n\n'
	@printf '\tmake deps\n\n'
	@printf '\tmake run\n\n'
	@printf '\tmake clean\n\n'
	@printf '\tmake install\n\n'

install:
	python3 setup.py install --user

onetest:
	python3 -m tests.test_keystore Test_Keystore.test_loadphrase
