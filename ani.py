import os
import numpy as np 
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from tkinter import messagebox, filedialog, ttk
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram,leaves_list, fcluster

class ANIProcessor:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

        self.figure = None
        self.canvas = None
    
    def setup_ui(self):
        self.root.title("ANIProcesser")
        self.root.geometry("500x150+800+500")

        tk.Label(self.root, text="ANI (下三角矩阵):").grid(row=0, column=0)
        self.input_dir = tk.Entry(self.root)
        self.input_dir.grid(row=0, column=1)
        tk.Button(self.root, text="浏览", command=lambda entry=self.input_dir: self.browse_file(entry)).grid(row=0, column=2)

        tk.Label(self.root, text="输出文件夹:").grid(row=1, column=0)
        self.output_dir = tk.Entry(self.root)
        self.output_dir.grid(row=1, column=1)
        tk.Button(self.root, text="浏览", command=lambda entry=self.output_dir: self.save_file(entry)).grid(row=1, column=2)

        tk.Label(self.root, text="NA值 (0~100):").grid(row=2, column=0)
        self.NA_replace = tk.Entry(self.root)
        self.NA_replace.grid(row=2, column=1)

        tk.Button(self.root, text="submit", command=self.process_main).grid(row=0, column=3, rowspan=3)

    def browse_file(self, entry_widget):
        filepath = filedialog.askopenfilename()
        if filepath:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filepath)
            entry_widget.xview_moveto(1)
    
    def save_file(self, entry_widget):
        filepath = filedialog.askdirectory()
        if filepath:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filepath)
            entry_widget.xview_moveto(1)
    
    def value_define(self):

        self.ani_input_path = self.input_dir.get().strip()
        ani_output_dir_up = self.output_dir.get().strip()

        self.ani_output_dir = os.path.join(ani_output_dir_up, "ani_output")
        os.makedirs(self.ani_output_dir, exist_ok=True)
        self.tree_output_path = os.path.join(self.ani_output_dir, 'Dendrogram.png')
        self.list_output_path = os.path.join(self.ani_output_dir, 'sorted_strain_list.txt')
        self.heatmap_output_path = os.path.join(self.ani_output_dir, 'heatmap.png')

        self.NA_replace_value = self.NA_replace.get().strip()

    def process_main(self):

        self.value_define()

        with open(self.ani_input_path, 'r') as f:
            raw_data = [line.strip().split('\t') for line in f if line.strip()]
        strain_numbers = len(raw_data) - 1

        strain_names = []
        for j in range(strain_numbers):
            if j < strain_numbers:
                strain_names.append(os.path.splitext(os.path.basename(raw_data[j+1][0]))[0])

        clean_data = []
        for line in raw_data:
            processed_line = [
                self.NA_replace_value if x in [None, 'NA', 'NaN'] else float(x)
                for x in line[1:]
            ]
            processed_line.append(100)
            clean_data.append(processed_line)


        lower_tri_matrix = np.zeros((strain_numbers, strain_numbers), dtype=np.float32)
        for i in range(strain_numbers):
            lower_tri_matrix[i, :i+1] = clean_data[i+1][:i+2]
        upper_tri_matrix = lower_tri_matrix.T
        sym_matrix = np.maximum(lower_tri_matrix, upper_tri_matrix)

        dist_matrix = 100 - sym_matrix
        condensed_dist = squareform(dist_matrix, checks=False)
        Z = linkage(condensed_dist, method='average')

        plt.figure(figsize=(10, 5))
        dendrogram(Z,
                labels=strain_names,
                orientation='top',
                leaf_rotation=90)
        plt.title("Dendrogram")
        plt.ylabel("distance")
        plt.savefig(self.tree_output_path)
        plt.close()

        optimal_order = leaves_list(Z)
        sorted_labels = [strain_names[i] for i in optimal_order]
        with open(self.list_output_path, 'w') as f:
            f.write('\n'.join(sorted_labels))
        
        sorted_data = pd.DataFrame(sym_matrix).iloc[optimal_order, optimal_order]
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            sorted_data,
            cmap="RdBu_r",
            square=True,
            xticklabels=[],
            yticklabels=[strain_names[i] for i in optimal_order],
            cbar_kws={"label": "ANI"},
            linewidths=0.0,
        )
        plt.title("Clustered Heatmap")
        plt.yticks(rotation=0, fontsize=5)
        plt.tight_layout()
        plt.savefig(self.heatmap_output_path)
        plt.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ANIProcessor(root)
    root.mainloop()