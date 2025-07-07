#!/usr/bin/env python3
import os
import sys
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.guess import guess_lexer_for_filename
from pygments.util import ClassNotFound
from dotenv import load_dotenv, set_key
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# --- Configuration ---
ENV_FILE = os.path.join(os.path.expanduser("~"), ".add_editor_config.env")
console = Console()

# --- AI Setup ---
def setup_ai_config():
    """Checks for and sets up Gemini API configuration."""
    load_dotenv(dotenv_path=ENV_FILE)
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL_NAME")

    if not api_key or not model_name:
        console.print(Panel("[bold yellow]AI Configuration nahi mili. Chaliye setup karein.[/bold yellow]", title="First Time Setup", border_style="yellow"))
        if not api_key:
            api_key = console.input("[bold green]Apna Gemini API Key yahan paste karein: [/bold green]")
            set_key(ENV_FILE, "GEMINI_API_KEY", api_key)
        if not model_name:
            model_name = console.input("[bold green]Kaun sa Gemini model use karna hai? (e.g., gemini-1.5-pro-latest): [/bold green]")
            set_key(ENV_FILE, "GEMINI_MODEL_NAME", model_name)
        console.print(Panel("[bold green]Configuration save ho gayi hai.[/bold green]", title="Success", border_style="green"))
    
    return api_key, model_name

def analyze_with_ai(content, api_key, model_name):
    """Sends content to Gemini AI for analysis."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"Please analyze the following file content. Explain what it does, suggest improvements, or identify potential bugs.\n\n```\n{content}\n```"
        with console.status("[bold yellow]AI analyze kar raha hai...[/bold yellow]", spinner="dots"):
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI analysis me error aaya: {e}"

# --- Editor Class ---
class Editor:
    def __init__(self, filename):
        self.filename = filename
        self.original_content = ""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.original_content = f.read()

        try:
            lexer = PygmentsLexer(guess_lexer_for_filename(self.filename, self.original_content))
        except ClassNotFound:
            lexer = None

        self.buffer = Buffer(document=self.original_content, multiline=True)
        self.buffer.on_text_changed += self.update_status_bar
        
        self.status_bar_text = ""
        self.update_status_bar()

        # Keybindings
        kb = KeyBindings()

        @kb.add("c-h")  # CTRL + H for Save
        def _save(event):
            self.save_file()

        @kb.add("c-x")  # CTRL + X for Exit
        def _exit(event):
            self.save_file()
            event.app.exit()

        @kb.add("c-r")  # CTRL + R for Rename
        def _rename(event):
            self.rename_file(event.app)

        @kb.add("c-s")  # CTRL + S for Search (Not save)
        def _search(event):
            # This is a placeholder for a more complex search implementation
            self.set_status("Search (CTRL+S) functionality not implemented in this version.")

        @kb.add("c-a")  # CTRL + A for AI Analyze
        def _analyze(event):
            event.app.exit(result="analyze")

        # Layout
        self.application = Application(
            layout=Layout(
                container=HSplit([
                    Window(content=BufferControl(buffer=self.buffer, lexer=lexer)),
                    Window(height=1, char="─"),
                    Window(height=1, content=FormattedTextControl(lambda: self.status_bar_text), style="class:status"),
                ]),
                focused_element=self.buffer
            ),
            key_bindings=kb,
            full_screen=True,
            style=Style.from_dict({
                'status': 'bg:#222222 #ffffff'
            })
        )

    def update_status_bar(self, buffer=None):
        """Updates the status bar text."""
        is_dirty = "*" if self.buffer.text != self.original_content else ""
        self.status_bar_text = f" {self.filename}{is_dirty} | CTRL+H: Save | CTRL+A: Analyze | CTRL+R: Rename | CTRL+X: Save & Exit "

    def set_status(self, message, temporary=True):
        """Temporarily sets a message on the status bar."""
        self.status_bar_text = message

    def save_file(self):
        """Saves the buffer content to the file."""
        with open(self.filename, "w") as f:
            f.write(self.buffer.text)
        self.original_content = self.buffer.text
        self.update_status_bar()
        self.set_status(f"File '{self.filename}' saved successfully!")

    def rename_file(self, app):
        # This is a basic implementation. A real one would use a prompt_toolkit dialog.
        self.set_status("Rename not yet implemented.")

    def run(self):
        """Runs the editor application."""
        return self.application.run()


def main():
    if len(sys.argv) != 2:
        print("Usage: add <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    
    # Run setup first if needed, before launching the editor
    api_key, model_name = setup_ai_config()

    editor = Editor(filename)
    result = editor.run()

    if result == "analyze":
        analysis_text = analyze_with_ai(editor.buffer.text, api_key, model_name)
        console.print(Panel(Markdown(analysis_text), title="[bold green]AI Analysis[/bold green]", border_style="green", expand=True))
        console.input("\n[yellow]Press Enter to continue...[/yellow]")

if __name__ == "__main__":
    main()
