#!/bin/bash

TARGET_FILE=${1:-gui.py}
VENV_DIR=".venv"

echo "=== Setup starting ==="

if [ ! -d "$VENV_DIR" ]; then
    echo "-> Creating virtual environment in ./$VENV_DIR..."
    python -m venv "$VENV_DIR"
else
    echo "-> Virtual environment already exists."
fi

echo "-> Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "-> Installing/verifying dependencies..."
python -m pip install --upgrade pip --quiet
python -m pip install gradio --quiet

if [ ! -f "$TARGET_FILE" ]; then
    echo ""
    echo "❌ Error: Could not find '$TARGET_FILE'!"
    echo "Please save your Python code as '$TARGET_FILE' or pass the filename as an argument."
    echo "Usage: ./run_gui.sh [filename.py]"
    exit 1
fi

echo "-> Starting the application!"
echo "-> Look for a forwarded port notification in your devcontainer, or open http://localhost:8082"
echo "======================"
python "$TARGET_FILE"