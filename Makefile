PYTHON = python3
APP = myrpal.py


run:
	$(PYTHON) $(APP) $(file)

lexer:
	$(PYTHON) $(APP) -l $(file)

ast:
	$(PYTHON) $(APP) -ast $(file)

st:
	$(PYTHON) $(APP) -st $(file)

clean:
	rm -rf __pycache__ *.pyc

.PHONY: run lexer ast st clean
