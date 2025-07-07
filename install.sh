#!/bin/bash

echo "=========================================="
echo "    'add' - The AI Text Editor Installer"
echo "=========================================="
echo

# System-specific installation
if [[ -d /data/data/com.termux ]]; then
    echo "[*] Termux environment detect hua."
    echo "[*] Zaroori packages install kiye jaa rahe hain..."
    pkg update -y && pkg upgrade -y
    pkg install python git -y
    INSTALL_DIR="/data/data/com.termux/files/usr/bin"
else
    echo "[*] Standard Linux environment detect hua."
    echo "[*] Zaroori packages install kiye jaa rahe hain..."
    if ! command -v sudo &> /dev/null; then
        echo "[Error] 'sudo' command nahi mila. Kripya 'sudo' install karein."
        exit 1
    fi
    sudo apt update -y && sudo apt upgrade -y
    sudo apt install python3 python3-pip git -y
    INSTALL_DIR="/usr/local/bin"
fi

# Install Python dependencies
echo
echo "[*] Python libraries (pip) install ki jaa rahi hain..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[Error] Python libraries install nahi ho payi. Kripya 'pip' aur internet connection check karein."
    exit 1
fi

# Make the editor script executable
chmod +x editor.py

# Create a symbolic link to make it a global command.
echo "[*] 'add' command set ki jaa rahi hai..."
SCRIPT_PATH=$(realpath editor.py)

if [[ -d /data/data/com.termux ]]; then
    ln -sf "$SCRIPT_PATH" "$INSTALL_DIR/add"
else
    sudo ln -sf "$SCRIPT_PATH" "$INSTALL_DIR/add"
fi

if [ $? -ne 0 ]; then
    echo "[Error] Command banane me fail. Kripya check karein ki aapke paas permissions hain."
    exit 1
fi

echo
echo "=========================================="
echo "   Installation Poora Hua! 🎉"
echo "=========================================="
echo "Ab aap naya terminal session shuru karke editor ka istemal kar sakte hain:"
echo
echo "    add your_file_name.txt"
echo
