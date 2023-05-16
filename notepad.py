import tkinter as tk
from tkinter import BOTH, END, INSERT, SEL, YES, IntVar, Menu, Radiobutton, Text, filedialog, messagebox
from tkinter.font import Font
from tkinter import font, filedialog, messagebox, simpledialog


class Notepad:
    def __init__(self, master):
        self.master = master
        master.title("Untitled - Notepad")
        self.master.geometry("800x440")
        self.text_area = tk.Text(master, wrap=tk.WORD, font=("Segoe UI", 10))
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.dark_mode_var = tk.IntVar(value=0)
        self.filename = None
        self.create_context_menu()  # Create the right-click context menu
        self.create_menu()

    def create_menu(self):
        # create the menu bar
        menubar = tk.Menu(self.master, borderwidth=0)
        

# create the file menu
        file_menu = tk.Menu(menubar, tearoff=0, borderwidth=0, activeborderwidth=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Exit", command=self.exit_notepad)
        menubar.add_cascade(label="File", menu=file_menu)
        
    

# create the edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, borderwidth=0, activeborderwidth=0)
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all_text)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
# Create the settings menu
        settings_menu = tk.Menu(menubar, tearoff=0, borderwidth=0, activeborderwidth=0)
        theme_menu = tk.Menu(settings_menu, tearoff=0, borderwidth=0, activeborderwidth=0)
        theme_menu.add_radiobutton(label="Dark Theme", variable=self.dark_mode_var, value=1, command=self.apply_dark_theme)
        theme_menu.add_radiobutton(label="Light Theme", variable=self.dark_mode_var, value=0, command=self.apply_light_theme)
        settings_menu.add_command(label="Font", command=self.open_font_dialog)
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)

# create the more menu
        more_menu = tk.Menu(menubar, tearoff=0, borderwidth=0, activeborderwidth=0)
        more_menu.add_command(label="About Notepad", command=self.about_notepad)
        menubar.add_cascade(label="More", menu=more_menu)
   
# configure the menu bar
        self.master.config(menu=menubar)
        file_menu.bind("<ButtonRelease-1>", lambda event: self.configure_submenu_width(file_menu))
        edit_menu.bind("<ButtonRelease-1>", lambda event: self.configure_submenu_width(edit_menu))
        settings_menu.bind("<ButtonRelease-1>", lambda event: self.configure_submenu_width(settings_menu))
        more_menu.bind("<ButtonRelease-1>", lambda event: self.configure_submenu_width(more_menu))

    def configure_submenu_width(self, menu):
        menu_width=menu.winfo_width()
        menu.entryconfigure(0, width=menu_width)
        
    def open_font_dialog(self):
        current_font = font.Font(font=self.text_area["font"])
        font_tuple = self.custom_font_dialog(current_font)
        if font_tuple:
            font_family = font_tuple[0]
            font_size = font_tuple[1]
            font_string = f"{font_family} {font_size}"
            self.text_area.configure(font=font_string)
        else:
            # Font dialog cancelled, do nothing
            pass

    def custom_font_dialog(self, current_font):
        font_dialog = tk.Toplevel(self.master)
        font_dialog.geometry("300x150")
        font_dialog.title("Select Font")

        font_dialog_label = tk.Label(font_dialog, text="Font Name:")
        font_dialog_label.pack(side=tk.TOP, padx=5, pady=5)

        font_name_var = tk.StringVar()
        font_name_var.set(current_font.actual()["family"])
        font_name_entry = tk.Entry(font_dialog, textvariable=font_name_var)
        font_name_entry.pack(side=tk.TOP, padx=5, pady=5)

        font_size_label = tk.Label(font_dialog, text="Font Size:")
        font_size_label.pack(side=tk.TOP, padx=5, pady=5)

        font_size_var = tk.StringVar()
        font_size_var.set(current_font.actual()["size"])
        font_size_entry = tk.Entry(font_dialog, textvariable=font_size_var)
        font_size_entry.pack(side=tk.TOP, padx=5, pady=5)

        ok_button = tk.Button(font_dialog, text="OK", command=font_dialog.destroy)
        ok_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        font_dialog.transient(self.master)  # Set dialog as transient to the parent window
        font_dialog.wait_visibility()  # Wait for the dialog window to be visible
        font_dialog.grab_set()  # Set a grab on the dialog window to prevent interaction with the parent window

        self.master.wait_window(font_dialog)  # Wait for the dialog window to be destroyed

        font_family = font_name_var.get()
        font_size = font_size_var.get()
        font_string = f"{font_family} {font_size}"

        return font_string



    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all_text(self):
        self.text_area.tag_add(SEL, "1.0", END)
        self.text_area.mark_set(INSERT, "1.0")
        self.text_area.see(INSERT)
        
    def create_context_menu(self):
        context_menu = tk.Menu(self.master, tearoff=0)
        context_menu.add_command(label="Cut", command=self.cut_text)
        context_menu.add_command(label="Copy", command=self.copy_text)
        context_menu.add_command(label="Paste", command=self.paste_text)
        context_menu.add_separator()
        context_menu.add_command(label="Select All", command=self.select_all_text)
        self.text_area.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

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
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("Python file", "*.py"),("Java file","*.java"),("C file","*.c"),("C++ file","*.cpp"),("JavaScript file","*.js"),("HTML file","*.html"),("CSS file","*.css"),("PHP file","*.php"),("XML file","*.xml")])
        if file_path:
            self.filename = file_path
            with open(file_path, "w") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self.master.title(self.filename + " - Notepad")
    
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("Python file", "*.py"),("Java file","*.java"),("C file","*.c"),("C++ file","*.cpp"),("JavaScript file","*.js"),("HTML file","*.html"),("CSS file","*.css")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
        self.filename = file_path
        self.master.title(file_path + " - Notepad")
        
    def apply_dark_theme(self):
        # Implement the logic for applying the dark theme
        # For example, you can change the background and text colors of the text area
        self.text_area.config(bg='black', fg='white')

    def apply_light_theme(self):
        # Implement the logic for applying the light theme
        # For example, you can change the background and text colors of the text area
        self.text_area.config(bg='white', fg='black')        
        
    def exit_notepad(self):
        self.master.destroy()
        
    def about_notepad(self):
        messagebox.showinfo("About Notepad", "This is a simple text editor written in Python using Tkinter extension.")
      

root = tk.Tk()
notepad = Notepad(root)
root.mainloop()

