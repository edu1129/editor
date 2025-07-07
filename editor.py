import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, Toplevel
import sys
import os
import json
import google.generativeai as genai

# Configuration file ka path (user ke home directory mein)
CONFIG_FILE = os.path.expanduser("~/.add_editor_config.json")

class TextEditor:
    def __init__(self, master, filepath=None):
        self.master = master
        self.filepath = filepath
        self.gemini_model = None

        # Window ka title set karein
        self.update_title()

        # Text widget banayein
        self.text_widget = scrolledtext.ScrolledText(master, wrap=tk.WORD, undo=True)
        self.text_widget.pack(expand=True, fill='both')

        # AI setup karein
        self.setup_ai()

        # Agar filepath diya gaya hai, to file open karein
        if self.filepath:
            self.open_file(self.filepath)

        # Key bindings set karein
        self.create_bindings()

    def update_title(self):
        """Window ka title update karta hai."""
        title = os.path.basename(self.filepath) if self.filepath else "Untitled"
        self.master.title(f"Add Editor - {title}")

    def create_bindings(self):
        """Keyboard shortcuts ko bind karta hai."""
        self.master.bind("<Control-h>", self.save_file)
        self.master.bind("<Control-H>", self.save_file) # Uppercase ke liye bhi
        self.master.bind("<Control-s>", self.search_text)
        self.master.bind("<Control-S>", self.search_text)
        self.master.bind("<Control-a>", self.analyze_with_ai)
        self.master.bind("<Control-A>", self.analyze_with_ai)
        self.master.bind("<Control-r>", self.rename_file)
        self.master.bind("<Control-R>", self.rename_file)
        # CTRL+X (Cut) ke liye built-in event ka istemal karein
        self.master.bind("<Control-x>", self.cut_text)
        self.master.bind("<Control-X>", self.cut_text)

    def open_file(self, filepath):
        """File ko kholta hai aur content ko text widget mein daalta hai."""
        try:
            # Agar file exist nahi karti, to ek khali file banayein
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    pass # Khali file ban gayi
            
            with open(filepath, 'r') as f:
                content = f.read()
                self.text_widget.delete('1.0', tk.END)
                self.text_widget.insert('1.0', content)
        except Exception as e:
            messagebox.showerror("Error", f"File kholne mein error: {e}")

    def save_file(self, event=None):
        """Current text ko file mein save karta hai."""
        if not self.filepath:
            # Agar file ka naam nahi hai, to "Save As" dialog dikhayein
            new_path = simpledialog.askstring("Save As", "File ka naam daalein:")
            if not new_path:
                return # User ne cancel kar diya
            self.filepath = new_path
        
        try:
            content = self.text_widget.get('1.0', tk.END)
            with open(self.filepath, 'w') as f:
                f.write(content)
            self.update_title()
            # Status bar ya message dikha sakte hain
            messagebox.showinfo("Success", f"File '{self.filepath}' save ho gayi.")
        except Exception as e:
            messagebox.showerror("Error", f"File save karne mein error: {e}")

    def rename_file(self, event=None):
        """Current file ko rename karta hai."""
        if not self.filepath:
            messagebox.showwarning("Warning", "Pehle file ko save karein.")
            return

        new_name = simpledialog.askstring("Rename File", "Naya file naam daalein:", initialvalue=os.path.basename(self.filepath))
        if not new_name:
            return

        try:
            new_filepath = os.path.join(os.path.dirname(self.filepath), new_name)
            os.rename(self.filepath, new_filepath)
            self.filepath = new_filepath
            self.update_title()
            messagebox.showinfo("Success", f"File ko '{new_name}' naam se rename kar diya gaya hai.")
        except Exception as e:
            messagebox.showerror("Error", f"File rename karne mein error: {e}")

    def search_text(self, event=None):
        """Text widget mein text search karta hai aur use highlight karta hai."""
        # Purane highlights ko hatayein
        self.text_widget.tag_remove('search', '1.0', tk.END)

        search_term = simpledialog.askstring("Search", "Kya search karna hai?")
        if not search_term:
            return

        self.text_widget.tag_configure('search', background='yellow', foreground='black')
        
        start_pos = '1.0'
        count = 0
        while True:
            start_pos = self.text_widget.search(search_term, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_term)}c"
            self.text_widget.tag_add('search', start_pos, end_pos)
            start_pos = end_pos
            count += 1
        
        if count == 0:
            messagebox.showinfo("Not Found", f"'{search_term}' nahi mila.")

    def cut_text(self, event=None):
        """Selected text ko cut karta hai."""
        self.text_widget.event_generate("<<Cut>>")
        return "break" # Default binding ko rokne ke liye

    def setup_ai(self):
        """Gemini AI ko configure karta hai."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            api_key = config.get("api_key")
            model_name = config.get("model_name")
        else:
            # Pehli baar setup
            api_key = simpledialog.askstring("Gemini API Setup", "Apna Gemini API Key daalein:", show='*')
            if not api_key:
                messagebox.showerror("Error", "API Key zaroori hai.")
                self.master.quit()
                return
            
            model_name = simpledialog.askstring("Gemini Model Setup", "Gemini model ka naam daalein (e.g., gemini-pro):", initialvalue="gemini-pro")
            if not model_name:
                model_name = "gemini-pro" # Default

            # Config file save karein
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"api_key": api_key, "model_name": model_name}, f)
        
        try:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel(model_name)
        except Exception as e:
            messagebox.showerror("AI Error", f"AI ko configure karne mein error: {e}")
            self.gemini_model = None

    def analyze_with_ai(self, event=None):
        """AI se current text ko analyze karwata hai."""
        if not self.gemini_model:
            messagebox.showerror("AI Error", "AI model load nahi hua hai. Restart karke try karein.")
            return

        code_content = self.text_widget.get('1.0', tk.END)
        if not code_content.strip():
            messagebox.showinfo("Info", "Analyze karne ke liye koi content nahi hai.")
            return

        # Loading message
        loading_window = Toplevel(self.master)
        loading_window.title("Analyzing...")
        loading_window.geometry("200x50")
        tk.Label(loading_window, text="AI se analyze kiya ja raha hai...").pack(pady=10)
        self.master.update()

        try:
            prompt = f"Please analyze the following code. Provide a brief summary, identify potential bugs, and suggest improvements:\n\n```\n{code_content}\n```"
            response = self.gemini_model.generate_content(prompt)
            
            loading_window.destroy() # Loading window band karein
            self.show_ai_response(response.text)

        except Exception as e:
            loading_window.destroy()
            messagebox.showerror("AI API Error", f"API se response lene mein error: {e}")

    def show_ai_response(self, response_text):
        """AI ke response ko ek naye window mein dikhata hai."""
        response_window = Toplevel(self.master)
        response_window.title("AI Analysis Result")
        response_window.geometry("600x400")
        
        text_area = scrolledtext.ScrolledText(response_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill='both')
        text_area.insert(tk.END, response_text)
        text_area.config(state='disabled') # Read-only

if __name__ == "__main__":
    root = tk.Tk()
    
    # Command-line se file path lein
    file_path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    
    app = TextEditor(root, filepath=file_path_arg)
    
    root.mainloop()
