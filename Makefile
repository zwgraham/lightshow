VENV=venv
PIP=venv/bin/pip
PY=venv/bin/python

$(VENV): 
	virtualenv $(VENV) 
	$(PIP) install -r requirements.txt

run:
	$(PY) -m lightshow.gateway


