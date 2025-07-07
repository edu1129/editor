#!/bin/bash

# Script ko error aane par exit karne ke liye
set -e

echo ">>> 'add' Text Editor Installation Script <<<"

# Check karein ki script root (sudo) ke saath run ho rahi hai ya nahi
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo: sudo bash install.sh"
  exit 1
fi

echo "1. Checking for Python3 and Pip3..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "Error: python3 and pip3 are required. Please install them and try again."
    exit 1
fi
echo "   Python3 and Pip3 found."

# Script ke current directory ko find karein
INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "2. Installation directory: $INSTALL_DIR"

echo "3. Installing Python dependencies from requirements.txt..."
pip3 install -r "$INSTALL_DIR/requirements.txt"
echo "   Dependencies installed successfully."

# Main editor script ka path
EDITOR_SCRIPT="$INSTALL_DIR/editor.py"

# Command ka naam
COMMAND_NAME="add"
# Installation path (system-wide commands ke liye standard location)
INSTALL_PATH="/usr/local/bin/$COMMAND_NAME"

echo "4. Creating the '$COMMAND_NAME' command at $INSTALL_PATH..."

# Ek wrapper script banayein jo editor ko python3 ke saath run karega
# 'tee' command sudo ke saath file mein likhne ki permission deta hai
tee "$INSTALL_PATH" > /dev/null <<EOF
#!/bin/bash
# Yeh script 'add' command ko run karne ke liye hai.
# Yeh editor.py ko sahi Python interpreter ke saath run karta hai
# aur saare command-line arguments ($@) pass karta hai.
python3 "$EDITOR_SCRIPT" "\$@"
EOF

echo "5. Making the command executable..."
chmod +x "$INSTALL_PATH"

echo ""
echo "✅ Installation Complete!"
echo "You can now run the editor from anywhere by typing:"
echo "   add [filename]"
echo "Example: add hello.txt"
