#!/bin/bash
rm -rf .venv
python3 -m venv .venv
source tools/activate.sh
source tools/install.sh
echo "!!! Please run 'tools/activate.sh' to enable the environment !!!"

