#!/usr/bin/env python3
"""oracle_hr: thin wrapper over the shared Oracle converter.

Record: knowledge/datasets/oracle-hr.md
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
import oracle_convert  # noqa: E402

if __name__ == "__main__":
    oracle_convert.run(sys.argv[1], sys.argv[2], "oracle_hr", ['hr_create.sql', 'hr_populate.sql', 'hr_code.sql'])
