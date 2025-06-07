PYTHON = python3
APP = myrpal.py
INPUT = test.rpal

# Default target
run:
	$(PYTHON) $(APP) $(INPUT)

lexer:
	$(PYTHON) $(APP) -l $(INPUT)

ast:
	$(PYTHON) $(APP) -ast $(INPUT)

st:
	$(PYTHON) $(APP) -st $(INPUT)

all:
	$(PYTHON) $(APP) -l -ast -st $(INPUT)

clean:
	rm -rf __pycache__ *.pyc

.PHONY: run lexer ast st all clean
