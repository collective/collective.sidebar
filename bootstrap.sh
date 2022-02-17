#/bin/sh
`which python3` -m venv .
./bin/pip install -r requirements.txt
./bin/buildout -c develop.cfg
