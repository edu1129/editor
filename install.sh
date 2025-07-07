#!/bin/bash

# Script ko error aane par exit karne ke liye
set -e

echo ">>> 'add' Text Editor Installation for Termux <<<"
echo ""

# Termux ke liye zaroori packages
echo "1. Checking and installing required Termux packages..."
echo "   Updating package lists..."
pkg update -y

echo "   Installing X11 repository (for GUI support)..."
pkg install -y x11-repo

echo "   Installing Python, Tkinter support (tk), and Git..."
pkg install -y python tk git

echo "   Required packages are installed."
echo ""

# Script ke current directory ko find karein
INSTALL_DIR="$(pwd)"
echo "2. Installation directory: $INSTALL_DIR"
echo ""

echo "3. Installing Python dependencies from requirements.txt..."
# YAHAN BADLAV KIYA GAYA HAI: pip upgrade wali line hata di gayi hai.
pip install -r "$INSTALL_DIR/requirements.txt"
echo "   Python dependencies installed successfully."
echo ""

# Main editor script ka path
EDITOR_SCRIPT="$INSTALL_DIR/editor.py"

# Command ka naam
COMMAND_NAME="add"
# Termux mein installation path $PREFIX/bin hota hai
INSTALL_PATH="$PREFIX/bin/$COMMAND_NAME"

echo "4. Creating the '$COMMAND_NAME' command at $INSTALL_PATH..."

# Ek wrapper script banayein jo editor ko python3 ke saath run karega
cat > "$INSTALL_PATH" <<EOF
#!/bin/bash
# Yeh script 'add' command ko run karne ke liye hai.
# Yeh editor.py ko sahi Python interpreter ke saath run karta hai
# aur saare command-line arguments (\$@) pass karta hai.
# Termux GUI ke liye DISPLAY variable zaroori ho sakta hai.
if [ -z "\$DISPLAY" ]; then
    export DISPLAY=":1"
fi
python3 "$EDITOR_SCRIPT" "\$@"
EOF

echo "5. Making the command executable..."
chmod +x "$INSTALL_PATH"
echo ""

echo "✅ Installation Complete!"
echo ""
echo "IMPORTANT: Is editor ko chalane ke liye aapko ek X11/VNC server ki zaroorat hai."
echo "Agar setup nahi hai, to README.md file padhein."
echo ""
echo "You can now run the editor from anywhere by typing:"
echo "   add [filename]"
echo "Example: add hello.txt"
