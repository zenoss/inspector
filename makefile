.DEFAULT_GOAL = default

clean:
	@rm -rf inspected-*
	@find . | grep .pyc | xargs rm

lint:
	@pylint -d too-many-branches -d line-too-long -d invalid-name -d missing-docstring -d too-many-locals -d too-many-statements -r n inspect script

exe:
	@chmod +x scripts/*

test:
	@./tests/test

save-test:
	@./tests/test --save

default:
	@echo "There's nothing to build here, this is just a utility makefile."
