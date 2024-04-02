import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class VimLikeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Vim-like Text Editor")
        self.file_path = None
        self.font_size = 24
        self.insert_mode = True

        self.text_area = tk.Text(root, wrap="word", bg="#222222", fg="#A6FF96", insertbackground="#A6FF96", selectbackground="#dcdcdc", font=("Courier", self.font_size))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<Key>", self.on_key_press)

        # Adicionando barra de rolagem invisível
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side="right", fill="y")
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)


        self.create_status_bar()
        self.create_menu()
        self.bind_shortcuts()

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="MOVEMENT MODE", bd=0, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        shortcut_menu = tk.Menu(menubar, tearoff=0)
        shortcut_menu.add_command(label="Show Shortcuts", command=self.show_shortcuts)
        menubar.add_cascade(label="Shortcuts", menu=shortcut_menu)

        zoom_menu = tk.Menu(menubar, tearoff=0)
        zoom_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl+plus")
        zoom_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+minus")
        menubar.add_cascade(label="Zoom", menu=zoom_menu)

    def bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_as_file())
        self.root.bind("<Control-x>", lambda event: self.cut_text())
        self.root.bind("<Control-c>", lambda event: self.copy_text())
        self.root.bind("<Control-v>", lambda event: self.paste_text())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-a>", lambda event: self.select_all())
        self.root.bind("<Control-plus>", lambda event: self.zoom_in())
        self.root.bind("<Control-minus>", lambda event: self.zoom_out())
        self.root.bind("<Control-q>", lambda event: self.exit_program())

        # Ativar modo de inserção com a tecla "i"
        self.root.bind("i", lambda event: self.toggle_insert_mode(event))

        # Voltar ao modo de movimento com a tecla "Esc"
        self.root.bind("<Escape>", lambda event: self.toggle_insert_mode(event))

    def on_key_press(self, event):
        if self.insert_mode:
            self.status_bar.config(text="INSERT MODE")
        else:
            self.status_bar.config(text="MOVEMENT MODE")

    def toggle_insert_mode(self, event):
        self.insert_mode = not self.insert_mode
        if self.insert_mode:
            self.status_bar.config(text="INSERT MODE")
        else:
            self.status_bar.config(text="MOVEMENT MODE")

    # Métodos de funcionalidade (open_file, save_file, etc.) continuam aqui...

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("Shell Script Files", "*.sh")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", file.read())

    def save_file(self):
        if not self.file_path:
            self.save_as_file()
            return
        with open(self.file_path, "w") as file:
            file.write(self.text_area.get("1.0", tk.END))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))
                self.file_path = file_path

    def exit_program(self):
        self.root.quit()

    def cut_text(self):
        self.copy_text()
        self.text_area.delete("sel.first", "sel.last")

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.selection_get())

    def paste_text(self):
        self.text_area.insert("insert", self.root.clipboard_get())

    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", "end")

    def zoom_in(self):
        self.font_size += 1
        self.text_area.config(font=("Courier", self.font_size))

    def zoom_out(self):
        self.font_size -= 1
        if self.font_size <= 1:
            self.font_size = 1
        self.text_area.config(font=("Courier", self.font_size))

    def show_shortcuts(self):
        message = """
        Shortcuts:
        - Open: Ctrl+O
        - Save: Ctrl+S
        - Save As: Ctrl+Shift+S
        - Cut: Ctrl+X
        - Copy: Ctrl+C
        - Paste: Ctrl+V
        - Undo: Ctrl+Z
        - Redo: Ctrl+Y
        - Select All: Ctrl+A
        """
        messagebox.showinfo("Shortcuts", message)

if __name__ == "__main__":
    root = tk.Tk()
    editor = VimLikeEditor(root)
    root.mainloop()
