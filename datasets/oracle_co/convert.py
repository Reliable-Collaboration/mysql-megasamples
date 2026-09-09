#!/usr/bin/env python3
"""oracle_co: thin wrapper over the shared Oracle converter.

Record: knowledge/datasets/oracle-co.md
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from megasamples.sources import oracle_convert  # noqa: E402

if __name__ == "__main__":
    oracle_convert.run(sys.argv[1], sys.argv[2], "oracle_co", ['co_create.sql', 'co_populate.sql'])
