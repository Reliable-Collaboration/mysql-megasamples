# megasamples build orchestration. Every target is a thin shim over a script in scripts/, so the
# pipeline is testable without make. Target list and rationale: PLAN.md section 2.4.
# the project venv when uv has created one (duckdb, lxml and py7zr live there), else system python
PY      ?= $(shell test -x .venv/bin/python && echo .venv/bin/python || echo python3)
DATASET ?=
SF      ?= 1

.PHONY: help core-fast image test-image okf-check provenance build-server build-server-stop clean-context dump
.PHONY: sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe oracle_sh employees adventureworks_lt adventureworks dvdstore contoso nyc_taxi chicago_crimes stackexchange_beer lahman

help:
	@echo "make <dataset>        fetch, stage, load, test one dataset (see CORE_FAST below)"
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
$(foreach d,sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe oracle_sh employees adventureworks_lt adventureworks dvdstore contoso nyc_taxi chicago_crimes stackexchange_beer lahman,$(eval $(call DATASET_RULE,$(d))))

CORE_FAST := sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe oracle_sh employees adventureworks_lt adventureworks dvdstore contoso nyc_taxi chicago_crimes stackexchange_beer lahman

core-fast: $(CORE_FAST)

# build the image from whatever datasets are named in DATASETS (default: the core-fast set)
DATASETS ?= $(CORE_FAST)
image: $(DATASETS)
	@$(PY) scripts/db.py start
	@for d in $(DATASETS); do $(PY) scripts/dump.py $$d; done
	@$(PY) scripts/registry.py $(DATASETS)
	@DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile -t mysql-megasamples:dev .
	@echo "built mysql-megasamples:dev with: $(DATASETS)"

test-image:
	@$(PY) tests/image_test.py $(DATASETS)

build-server:
	@$(PY) scripts/db.py start
build-server-stop:
	@$(PY) scripts/db.py stop
clean-context:
	rm -rf docker/context/*

okf-check:
	@$(PY) scripts/okf_check.py --bundle knowledge
	@$(PY) scripts/okf_fix_quotes.py --bundle knowledge --check
