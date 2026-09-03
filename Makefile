# megasamples build orchestration. Every target is a thin shim over a script in scripts/, so the
# pipeline is testable without make. Target list and rationale: PLAN.md section 2.4.
PY      ?= python3
DATASET ?=
SF      ?= 1

.PHONY: help core-fast image test-image okf-check provenance build-server build-server-stop clean-context
.PHONY: sakila chinook northwind pubs

help:
	@echo "make <dataset>        fetch, stage, load, test one dataset (sakila chinook northwind pubs)"
	@echo "make core-fast        the CI subset (PLAN.md section 4.3)"
	@echo "make okf-check        validate the knowledge bundle"
	@echo "make build-server     start the throwaway MySQL build server"
	@echo "make build-server-stop"

# --- per-dataset pipeline: fetch -> stage -> load -> test ---------------------------------
define DATASET_RULE
$(1):
	@echo "== $(1): fetch"    && $$(PY) scripts/fetch.py $(1)
	@echo "== $(1): stage"    && $$(PY) scripts/stage.py $(1)
	@echo "== $(1): load"     && $$(PY) scripts/load.py  $(1)
	@echo "== $(1): test"     && $$(PY) scripts/verify.py $(1)
endef
$(foreach d,sakila chinook northwind pubs,$(eval $(call DATASET_RULE,$(d))))

core-fast: sakila chinook northwind pubs

build-server:
	@$(PY) scripts/db.py start
build-server-stop:
	@$(PY) scripts/db.py stop
clean-context:
	rm -rf docker/context/*

okf-check:
	@$(PY) scripts/okf_check.py --bundle knowledge
	@$(PY) scripts/okf_fix_quotes.py --bundle knowledge --check
