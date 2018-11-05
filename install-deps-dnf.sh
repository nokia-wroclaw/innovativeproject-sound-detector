#!/bin/bash

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This script must be sourced to work. Please run:"
    echo 
    echo "  source $0"
    exit 1
fi;

echo "Installing system dependencies..."
sudo dnf install -y portaudio-devel python3-tkinter python3-virtualenv

if [ ! -d "./.venv" ]; then
    echo "No virtualenv present"
    echo "Preparing virtualenv"
    virtualenv -p python3 .venv
else
    echo "Vritualenv present at .venv, skipping bootstrap"
fi;
echo "Activating virtualenv..."
source ./.venv/bin/activate
echo "Installing Python dependencies to virtualenv..."
pip install -r requirements.txt
echo "Ready to go!"
echo