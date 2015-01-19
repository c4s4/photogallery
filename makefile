GALLERIES=`ls *.yml`

YELLOW=\033[93m
CLEAR=\033[0m

all: check run

check:
	@echo "${YELLOW}Checking Python code${CLEAR}"
	pylint --rcfile=pylint.cfg *.py

run:
	@echo "${YELLOW}Generating galleries${CLEAR}"
	python photogallery.py $(GALLERIES)
