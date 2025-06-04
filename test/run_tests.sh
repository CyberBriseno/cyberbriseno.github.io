#!/bin/bash
# Simple test runner
set -e
python3 "$(dirname "$0")/check_links.py"
