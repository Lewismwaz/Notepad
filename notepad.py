import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, master):
        self.master = master
        master.title("Untitled - Notepad")
        self.text_area = tk.Text(master, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.filename = None
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Word Wrap", command=self.toggle_word_wrap)
        menu_bar.add_cascade(label="View", menu=view_menu)

        self.master.config(menu=menu_bar)

    def new_file(self):
        if self.text_area.get("1.0", "end-1c") != '':
            response = messagebox.askyesnocancel("Save Changes?", "Do you want to save changes to the current file?")
            if response == True:
                self.save_file()
            elif response == False:
                self.text_area.delete("1.0", "end")
                self.master.title("Untitled - Notepad")
                self.filename = None
        else:
            self.text_area.delete("1.0", "end")
            self.master.title("Untitled - Notepad")
            self.filename = None

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.filename = file_path
            self.master.title(file_path + " - Notepad")
            with open(file_path, "r") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, f.read())

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self.master.title(self.filename + " - Notepad")
        else:
            file_path = filedialog.asksaveasfilename()
            if file_path:
                self.filename = file_path
                with open(file_path, "w") as f:
                    f.write(self.text_area.get("1.0", "end-1c"))
                self.master.title(self.filename + " - Notepad")

    def toggle_word_wrap(self):
        wrap_state = self.text_area.cget("wrap")
        if wrap_state == "none":
            self.text_area.config(wrap="word")
        else:
            self.text_area.config(wrap="none")

root = tk.Tk()
notepad = Notepad(root)
root.mainloop()
