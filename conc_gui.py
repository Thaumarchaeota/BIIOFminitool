import os
import tkinter as tk

from Bio import SeqIO
from natsort import natsorted
from collections import defaultdict
from tkinter import filedialog

class SeqConcatenator:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

        self.figure = None
        self.canvas = None
    
    def setup_ui(self):
        self.root.title("SeqConcatenator")
        self.root.geometry("500x150+800+500")

        tk.Label(self.root, text="输入文件夹 (同时包含所有fasta文件与唯一的xmfa文件)").grid(row=0, column=0)
        self.input_dir = tk.Entry(self.root)
        self.input_dir.grid(row=1, column=0)
        tk.Button(self.root, text="浏览", command=lambda entry=self.input_dir: self.browse_dir(entry)).grid(row=1, column=1)

        tk.Label(self.root, text="输出文件夹:").grid(row=2, column=0)
        self.output_dir = tk.Entry(self.root)
        self.output_dir.grid(row=3, column=0)
        tk.Button(self.root, text="浏览", command=lambda entry=self.output_dir: self.browse_dir(entry)).grid(row=3, column=1)
        
        self.Ns = tk.Entry(self.root)
        self.Ns.grid(row=4, column=0)

        tk.Button(self.root, text="Concatenate", command=self.process_main).grid(row=5, column=0, columnspan=2)
    
    def browse_dir(self, entry_widget):
        filepath = filedialog.askdirectory()
        if filepath:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filepath)
            entry_widget.xview_moveto(1)
    
    def value_define(self):

        self.input_path = self.input_dir.get().strip()
        self.output_path = os.path.join(self.output_dir.get().strip(), str(self.input_path).split("/")[-1] + "_concatenated")
        os.makedirs(self.output_path, exist_ok=True)
        self.N_number = self.Ns.get().strip()

    def process(self):
        
        seq_dict = defaultdict(list)
        n_spacer = "N" * int(self.N_number)

        for filename in natsorted(os.listdir(self.input_path)):
            if filename.endswith((".fasta", ".fa", ".fna")):
                filepath = os.path.join(self.input_path, filename)
                print(f"fasta: Loading and processing {filename}...")
                
                with open(filepath) as handle:
                    for i, record in enumerate(SeqIO.parse(handle, "fasta")):
                        seq_dict[i].append(str(record.seq))
            
            sequence_name = {}
            if filename.endswith((".xmfa")):
                filepath = os.path.join(self.input_path, filename)
                print(f"mapping: use file [{filename}] to rename")

                with open(filepath, 'r') as xmfa_file:
                    for line in xmfa_file:
                        line = line.strip()
                        if line.startswith("#Sequence") and "File" in line:
                            try:
                                seq_number = int(line.split("Sequence")[1].split("File")[0])
                                seq_name = line.split("/")[-1].split(".f")[0].strip()
                                sequence_name[seq_number] = seq_name
                                print(f"mapping: successful seq{seq_number} -> {seq_name}")
                            except(IndexError, ValueError) as e:
                                print(f"mapping: error in line [{line}]\n{str(e)} ")


        output_all_file = os.path.join(self.output_path, f"concatenated_sequence.fasta")
        for position, sequences in seq_dict.items():
            output_sep_file = os.path.join(self.output_path, f"{position+1}_{sequence_name[position+1]}.fasta")
            merged_seq = n_spacer.join(sequences)
            
            with open(output_sep_file, "w") as f:
                f.write(f">{sequence_name[position+1]}\n{merged_seq}")

            with open(output_all_file, "a") as f:
                f.write(f">{sequence_name[position+1]}\n{merged_seq}\n")
            
            print(f"concatenating: {len(sequences)} sequences of Seq {position+1} ({sequence_name[position+1]}) merged")
        
        print(f"concatenating: completed")


    def process_main(self):
        self.value_define()
        self.process()


if __name__ == "__main__":
    root = tk.Tk()
    app = SeqConcatenator(root)
    root.mainloop()