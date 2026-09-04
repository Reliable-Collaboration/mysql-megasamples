# megasamples build orchestration. Every target is a thin shim over a script in scripts/, so the
# pipeline is testable without make. Target list and rationale: PLAN.md section 2.4.
# the project venv when uv has created one (duckdb, lxml and py7zr live there), else system python
PY      ?= $(shell test -x .venv/bin/python && echo .venv/bin/python || echo python3)
DATASET ?=
SF      ?= 1

.PHONY: help check dvdstore-reviews nyc-taxi-yellow chicago-full wwi-export core core-fast print-core print-core-fast image image-only test-image bench-index-order okf-check provenance build-server build-server-stop clean-context dump
.PHONY: sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe oracle_sh employees adventureworks_lt adventureworks dvdstore contoso nyc_taxi chicago_crimes stackexchange_beer lahman enron wikipedia_simple

help:
	@echo "make <dataset>        fetch, stage, load, test one dataset (see CORE_FAST below)"
	@echo "make core             every core dataset (what the image contains)"
	@echo "make core-fast        the CI subset (PLAN.md section 4.3)"
	@echo "make check            the local gate: bundle validation + generated files up to date"
	@echo "make okf-check        validate the knowledge bundle"
	@echo "make wwi-export       re-derive WideWorldImporters from Microsoft's .bak (SQL Server,"
	@echo "                      Developer EULA -- see the target below; needed once, not per build)"
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
$(foreach d,adventureworks_dw wideworldimporters wideworldimporters_dw bts_ontime contoso_1m contoso_10m stackexchange_dba enron_full wikipedia_simple_full sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe oracle_sh employees adventureworks_lt adventureworks dvdstore contoso nyc_taxi chicago_crimes stackexchange_beer lahman enron wikipedia_simple,$(eval $(call DATASET_RULE,$(d))))

# every core dataset: what the published image contains
CORE := sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe \
        oracle_sh employees adventureworks_lt adventureworks dvdstore contoso nyc_taxi \
        chicago_crimes stackexchange_beer lahman enron wikipedia_simple

# the CI subset (PLAN.md section 4.3). Six datasets are deliberately outside it:
#   lahman           maintainer-supplied: there is no URL a build can fetch (manifest `manual: true`)
#   chicago_crimes   a live API whose content, and so its sha256, changes daily
#   enron 443 MB, wikipedia_simple 540 MB, oracle_sh 91 MB, adventureworks (69 tables, the longest
#                    conversion) -- download and wall-clock budget on a hosted runner
# The first two become CI-able once R-02 publishes them as release assets; the rest stay local.
CORE_FAST := sakila chinook northwind pubs smallsets jaffle_shop oracle_hr oracle_co oracle_oe \
             adventureworks_lt dvdstore contoso nyc_taxi stackexchange_beer employees

core: $(CORE)

core-fast: $(CORE_FAST)

# build the image from whatever datasets are named in DATASETS (default: the core-fast set)
DATASETS ?= $(CORE)
image: $(DATASETS) image-only

# bake what is already loaded in the build server, without re-running the datasets. CI uses this
# after `make core-fast` so the pipeline is not run twice.
image-only:
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

# WideWorldImporters is the only dataset with no script or CSV form. Producing it means running
# SQL Server 2022 Developer Edition, which means accepting Microsoft's EULA; the script refuses to
# start until you say so, and prints the terms. Nothing licensed under that EULA is redistributed --
# the container is deleted afterwards and only the exported data, which is MIT, is kept.
#   MEGASAMPLES_ACCEPT_MSSQL_EULA=1 make wwi-export
# You only need this to re-derive the export. Building or using the databases does not.
wwi-export:
	@$(PY) scripts/fetch.py wideworldimporters wideworldimporters_dw
	@$(PY) scripts/wwi_export.py

# Extended tier: 3,475,226 yellow trips appended to a loaded `nyc_taxi` (which must exist first).
nyc-taxi-yellow:
	@$(PY) scripts/fetch.py nyc_taxi_yellow
	@$(PY) scripts/stage.py nyc_taxi_yellow
	@$(PY) scripts/load.py  nyc_taxi_yellow
	@$(PY) scripts/verify.py nyc_taxi_yellow

# Extended tier: 8.2 M crimes (2001..2024) appended to a loaded `chicago_crimes`. One CSV per year,
# ~2.5 GB of download; the digests drift because the portal revises closed years.
chicago-full:
	@$(PY) scripts/fetch.py chicago_crimes_full
	@$(PY) scripts/stage.py chicago_crimes_full
	@$(PY) scripts/load.py  chicago_crimes_full
	@$(PY) scripts/verify.py chicago_crimes_full

bench-index-order:
	@$(PY) scripts/bench_index_order.py --dataset $(or $(DATASET),employees) --repeat $(or $(REPEAT),1)

provenance:
	@$(PY) scripts/gen_provenance.py

# used by CI to pass the same list to `make image` and `make test-image`
print-core-fast:
	@echo $(CORE_FAST)
print-core:
	@echo $(CORE)

# the local gate, in place of CI: everything that does not need a build. `make core-fast`,
# `make image` and `make test-image` are the rest of it, and they run in Docker on this machine.
check:
	@$(PY) scripts/okf_check.py
	@$(PY) scripts/gen_provenance.py --check

# extended tier: loads the 190 MB review tables into an already-loaded dvdstore
dvdstore-reviews:
	@echo "== dvdstore_reviews: fetch" && $(PY) scripts/fetch.py dvdstore_reviews
	@echo "== dvdstore_reviews: stage" && $(PY) scripts/stage.py dvdstore_reviews
	@echo "== dvdstore_reviews: load"  && $(PY) scripts/load.py dvdstore_reviews

okf-check:
	@$(PY) scripts/okf_check.py --bundle knowledge
	@$(PY) scripts/okf_fix_quotes.py --bundle knowledge --check
