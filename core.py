import os
import pandas as pd
import numpy
import tkinter as tk

from pathlib import Path
from tkinter import messagebox, filedialog, ttk





class ANIProcessor:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

        self.figure = None
        self.canvas = None
    
    def setup_ui(self):
        self.root.title("ANI    Processer")
        self.root.geometry("500x100+800+500")

        tk.Label(self.root, text="ANI表:").grid(row=0, column=0)
        self.input_entry = tk.Entry(self.root)
        self.input_entry.grid(row=0, column=1)
        tk.Button(self.root, text="浏览", command=lambda entry=self.input_entry: self.browse_file(entry)).grid(row=0, column=2)

        tk.Label(self.root, text="Output File").grid(row=1, column=0)
        self.output_entry = tk.Entry(self.root)
        self.output_entry.grid(row=1, column=1)
        tk.Button(self.root, text="浏览", command=lambda entry=self.output_entry: self.browse_file(entry)).grid(row=1, column=2)

        tk.Button(self.root, text="submit", command=self.process_main).grid(row=0, column=3, rowspan=2)

    def browse_file(self, entry_widget):
        filepath = filedialog.askopenfilename()
        if filepath:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filepath)
            entry_widget.xview_moveto(1)

    def process_main(self):
        input_path = self.input_entry.get().strip()
        output_path = self.output_entry.get().strip()

        # if not input_path:
        #     messagebox.showerror("错误", "需要填入ANI文件路径")
        #     return
        
        # if not output_path:
        #     messagebox.showerror("错误", "需要填入ANI文件路径")
        #     return
        
        # if not os.path.exists(input_path):
        #     messagebox.showerror("错误", "填入的ANI文件不存在")

        # try:
        #     ani_lower_matrix = pd.read_csv(r'D:/project_gut/1/plasmid301.txt.matrix', sep='\t')
        # except Exception as e:
        #     messagebox.showerror("错误", f"无法读取文件:\n{str(e)}")

        # strain_names_list = ani_lower_matrix.iloc[:, 0].apply(lambda x: Path(str(x)).stem if pd.notna(x) else None)

        # ani_lower_matrix.drop(ani_lower_matrix.columns[0], axis=1, inplace=True)
        # ani_lower_matrix.insert(0, 'filename', strain_names_list)

        # ani_lower_matrix_names_trans = ani_lower_matrix.copy()

        # new_col_names = ['x' + str(name) if name is not None else 'x_None' for name in strain_names_list]

        # ani_lower_matrix_names_trans.columns = new_col_names[:len(ani_lower_matrix_names_trans.columns)]
        
        # n = len(strain_names_list)
        # missing_cols = n + 1 - len(ani_lower_matrix_names_trans.columns)
        # for i in range(missing_cols):
        #     ani_lower_matrix_names_trans[f'New_{i}'] = pd.NA

        ani_lower_matrix = pd.read_csv('D:/project_gut/1/plasmid301.txt.matrix', sep='\t')

        ani_lower_matrix.iloc[:, 0] = ani_lower_matrix.iloc[:, 0].apply(lambda x: Path(str(x)).stem if pd.notna(x) else None)

        strain_names = ani_lower_matrix.iloc[:, 0].tolist()
        new_columns = [ani_lower_matrix.columns[0]] + strain_names
        ani_lower_matrix.columns = new_columns[:len(ani_lower_matrix.columns)]

        last_strain = strain_names[-1]
        ani_lower_matrix[last_strain] = pd.NA
        
        ani_lower_matrix.reset_index(drop=True, inplace=True)

        temp_output_path = 'D:/project_gut/1/output_matrix.tsv'
        ani_lower_matrix.to_csv(temp_output_path, sep='\t', index=False)
        os.startfile(temp_output_path)

        print("1")




if __name__ == "__main__":
    root = tk.Tk()
    app = ANIProcessor(root)
    root.mainloop()



