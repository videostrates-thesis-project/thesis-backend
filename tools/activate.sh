#!/bin/bash

# If the script is running on windows in git bash
if [[ "$OSTYPE" == "msys" ]]; then
    # Activate the virtual environment
    source .venv/Scripts/activate
else
    # Activate the virtual environment
    source .venv/bin/activate
fi
