import sys
from megasamples.cli import main

# line-buffered even when redirected, so a build log reads in the order things happened
sys.stdout.reconfigure(line_buffering=True)
sys.exit(main())
