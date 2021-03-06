GALLERIES=`ls *.yml`

YELLOW=\033[93m
CLEAR=\033[0m

all: check run rsync

check:
	@echo "${YELLOW}Checking Python code${CLEAR}"
	pylint --rcfile=pylint.cfg *.py

run:
	@echo "${YELLOW}Generating galleries${CLEAR}"
	python photogallery.py $(GALLERIES)

rsync:
	@echo "${YELLOW}Rsync with web server${CLEAR}"
	@for gallery in $(GALLERIES) ; do \
		dest=`python -c "import os, yaml; print os.path.expanduser(yaml.load(open('$$gallery'))['destination'])"`; \
		dir=`basename "$$dest"`; \
		rsync -azvs -e ssh "$$dest" casa@sweetohm.net:"/home/web/photos/$$dir"; \
	done

help:
	@echo "${YELLOW}Help${CLEAR}"
	@echo "check:  Check Python code with Pylint"
	@echo "run:    Run script to generate galleries"
	@echo "rsync:  Sunchronize generated galleries with site"
