import os
import re
import tkinter as tk

from pathlib import Path
from tkinter import messagebox, filedialog, ttk

class Phytree_add_info:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

        self.figure = None
        self.canvas = None

    def setup_ui(self):
        self.root.title("infoAdder")
        self.root.geometry("500x100+800+500")

        tk.Label(self.root, text="进化树文件(.newick)").grid(row=0, column=0)
        self.newick_entry = tk.Entry(self.root)
        self.newick_entry.grid(row=0, column=1)
        tk.Button(self.root, text="浏览", command=lambda entry=self.newick_entry: self.browse_file(entry)).grid(row=0, column=2)

        tk.Label(self.root, text="重命名文件").grid(row=1, column=0)
        self.rule_entry = tk.Entry(self.root)
        self.rule_entry.grid(row=1, column=1)
        tk.Button(self.root, text="浏览", command=lambda entry=self.rule_entry: self.browse_file(entry)).grid(row=1, column=2)

        tk.Button(self.root, text="submit", command=self.newick_import).grid(row=0, column=3, rowspan=2)

    def browse_file(self, entry_widget):
        filepath = filedialog.askopenfilename()
        if filepath:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filepath)
            entry_widget.xview_moveto(1)
    
    def newick_import(self):
        self.newick_path = self.newick_entry.get().strip()
        self.rule_path = self.rule_entry.get().strip()
        self.info_match()

    def info_match(self):
        self.matching_table = {}
        with open(self.rule_path, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 1):
                strain_gcf_fna = lines[i].split(',')[0].strip()
                strain_clean = self.strain_rename_clean(strain_gcf_fna)
                strain_gcf = self.strain_rename_gcf(strain_gcf_fna)
                strain_time = lines[i].split(',')[1].strip()
                strain_species = lines[i].split(',')[2].strip()
                strain_places = lines[i].split(',')[3].strip()
                strain_info = strain_clean + "_" + strain_time + "_" + strain_species + "_" + strain_places
                self.matching_table[strain_gcf] = strain_info
        self.info_add()
    
    def strain_rename_clean(self, strain_unrename):
        strain_rename = strain_unrename.split('-GCF')[0].strip()
        return strain_rename
    
    def strain_rename_gcf(self, strain_unrename):
        strain_rename = strain_unrename.split('.fna')[0].strip()
        return strain_rename    

    
    def info_add(self):
        with open(self.newick_path, 'r') as file:
            newick_data = file.read()
        for strain_gcf, strain_info in self.matching_table.items():
            newick_data = re.sub(r'\b' + re.escape(strain_gcf) + r'\b', strain_info, newick_data)
        with open(self.newick_path, 'w') as file:
            file.write(newick_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = Phytree_add_info(root)
    root.mainloop()