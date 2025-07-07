# Add Text Editor

'Add' ek halka-fulka, modern text editor hai jo Python aur Tkinter se bana hai. Isme AI-powered code analysis (Google Gemini ke zariye) aur zaroori editing features hain.

## Features

- **File Handling**: Nayi file banayein ya maujooda file ko `add filename.ext` command se kholein.
- **AI Code Analysis**: `CTRL + A` daba kar apne code ka AI se analysis karwayein.
- **Text Search**: `CTRL + S` se text search karein, search kiya gaya text yellow highlight ho jayega.
- **Save File**: `CTRL + H` se file save karein.
- **Cut Text**: `CTRL + X` se select kiye gaye text ko cut karein.
- **Rename File**: `CTRL + R` se current file ko rename karein.
- **First-Time Setup**: Pehli baar istemal karne par, editor aapse Gemini API Key aur Model Name poochega.

## Installation

The installation script automatically detects your environment (Linux/macOS vs. Termux) and installs accordingly.

### For Linux / macOS

1.  **Repository Clone Karein:**
    ```bash
    git clone <your-repo-url>
    cd add-editor
    ```

2.  **Installation Script Run Karein:**
    Script ko execute karne ke liye permissions dein aur use `sudo` ke saath run karein taaki `add` command system-wide available ho sake.

    ```bash
    chmod +x install.sh
    sudo bash install.sh
    ```

### For Termux (Android)

1.  **Repository Clone Karein:**
    ```bash
    git clone <your-repo-url>
    cd add-editor
    ```

2.  **Installation Script Run Karein:**
    Termux mein `sudo` ki zaroorat nahi hai.
    ```bash
    chmod +x install.sh
    bash install.sh
    ```

3.  **GUI Setup (Zaroori):**
    Termux mein GUI applications chalaane ke liye aapko ek X11 server ki zaroorat hogi.
    -   Apne Android device par ek X11 server app install karein (jaise XServer XSDL).
    -   Termux mein, `DISPLAY` environment variable set karein:
        ```bash
        export DISPLAY=:0
        ```
    -   Yeh command aap har baar Termux session shuru karne par daal sakte hain, ya apne `.bashrc` mein add kar sakte hain.

## Ho Gaya!
Ab aap terminal mein `add` command ka istemal kar sakte hain.

## Usage

- **Naya Editor Kholne Ke Liye:**
  ```bash
  add
  ```

- **File Kholne Ya Banane Ke Liye:**
  ```bash
  add my_script.py
  ```
  Agar `my_script.py` maujood nahi hai, to yeh ban jayegi.

## Keybindings

- `CTRL + A`: AI se code analyze karein.
- `CTRL + S`: Text search karein.
- `CTRL + H`: File save karein.
- `CTRL + R`: File rename karein.
- `CTRL + X`: Text cut karein.
