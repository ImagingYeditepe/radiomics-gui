import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
import numpy as np
import os
import csv

def main():
    root = tk.Tk()
    root.title("Patient Data Management")

    def open_existing_file():
        fname = fd.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if fname:
            dataf = pd.read_excel(fname)
            root.destroy()
            display_table(dataf, fname)

    def new_project():
        dataf = pd.DataFrame(columns=['patient_id', 'age', 'tumor_status', 'file_path'])
        root.destroy()
        display_table(dataf, None)

    open_button = tk.Button(root, text="Open Existing File", command=open_existing_file)
    open_button.pack(pady=20)

    new_button = tk.Button(root, text="New Project", command=new_project)
    new_button.pack(pady=20)

    root.mainloop()
    
    

def open_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            reader = csv.reader(file, delimiter="\t")
            content = list(reader)
        show_table_window(content)
    else:
        print("File not found")
        
        

def show_table_window(content):
    table_window = tk.Toplevel()
    table_window.title("File Content")

    tree = ttk.Treeview(table_window)
    tree["columns"] = ("#1", "#2", "#3", "#4", "#5")

    tree.heading("#0", text="Index")
    for i, heading in enumerate(content[0]):
        tree.heading("#" + str(i+1), text=heading)

    for index, row in enumerate(content[1:], start=1):
        tree.insert("", index, text=index, values=row)

    tree.pack(expand=True, fill="both")
    
    

def display_table(dataf, fname):
    root = tk.Tk()
    root.title("Patient Data")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame)
    tree["columns"] = ("ID", "Age", "Tumor Status", "File Path", "Open File")
    tree.heading("#0", text="")
    tree.column("#0", anchor="center", width=0)
    tree.heading("ID", text="Patient ID")
    tree.column("ID", anchor="center", width=100)
    tree.heading("Age", text="Age")
    tree.column("Age", anchor="center", width=100)
    tree.heading("Tumor Status", text="Tumor Status")
    tree.column("Tumor Status", anchor="center", width=100)
    tree.heading("File Path", text="File Path")
    tree.column("File Path", anchor="center", width=200)
    tree.heading("Open File", text="Open File")
    tree.column("Open File", anchor="center", width=100)

    for i in range(len(dataf)):
        tree.insert("", i, text="", values=(dataf.loc[i]['patient_id'], dataf.loc[i]['age'], dataf.loc[i]['tumor_status'], dataf.loc[i]['file_path'], ""))

    def on_click(event):
        item = tree.selection()[0]
        file_path = tree.item(item, "values")[3]
        open_file(file_path)

    tree.bind("<Double-1>", on_click)

    tree.pack(expand=True, fill="both")

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=10)

    add_button = tk.Button(button_frame, text="Add Patient", command=lambda: add_patient_window(tree, dataf))
    add_button.pack(side=tk.LEFT)

    delete_button = tk.Button(button_frame, text="Delete Patient", command=lambda: delete_patient(tree, dataf))
    delete_button.pack(side=tk.LEFT, padx=10)

    save_button = tk.Button(button_frame, text="Save", command=lambda: save_changes(dataf, fname))
    save_button.pack(side=tk.RIGHT)

    export_button = tk.Button(root, text="Export to Excel", command=lambda: export_to_excel(dataf))
    export_button.pack(side=tk.BOTTOM, pady=10)

    edit_button = tk.Button(button_frame, text="Edit Patient", command=lambda: edit_patient(tree, dataf))
    edit_button.pack(side=tk.LEFT, padx=10)
    
    new_project_button = tk.Button(button_frame, text="New Project", command=lambda: start_new_project(dataf, root))
    new_project_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()




def edit_patient(tree, dataf):
    selected_item = tree.selection()
    if selected_item:
        item = tree.selection()[0]
        index = int(tree.index(item))
        selected_patient = dataf.loc[index]

        edit_window = tk.Toplevel()
        edit_window.title("Edit Patient Information")

        tk.Label(edit_window, text="Patient ID:", fg="red").grid(row=0, column=0)
        tk.Label(edit_window, text="Age:", fg="red").grid(row=1, column=0)
        tk.Label(edit_window, text="Tumor/Benign:", fg="red").grid(row=2, column=0)
        tk.Label(edit_window, text="File Path:", fg="red").grid(row=3, column=0)

        patient_id_entry = tk.Entry(edit_window)
        age_entry = tk.Entry(edit_window)
        tumor_status_combobox = ttk.Combobox(edit_window, values=["Tumor", "Benign"])
        tumor_status_combobox.grid(row=2, column=1)
        tumor_status_combobox.set(selected_patient['tumor_status'])

        file_path_entry = tk.Entry(edit_window)
        patient_id_entry.grid(row=0, column=1)
        age_entry.grid(row=1, column=1)
        file_path_entry.grid(row=3, column=1)

        patient_id_entry.insert(0, selected_patient['patient_id'])
        age_entry.insert(0, selected_patient['age'])
        file_path_entry.insert(0, selected_patient['file_path'])

        def choose_file():
            file_path = fd.askopenfilename()
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)

        file_button = tk.Button(edit_window, text="Choose File", command=choose_file)
        file_button.grid(row=3, column=2)

        def update_patient():
            patient_id = patient_id_entry.get()
            age = age_entry.get()
            tumor_status = tumor_status_combobox.get()
            file_path = file_path_entry.get()

            dataf.at[index, 'patient_id'] = patient_id
            dataf.at[index, 'age'] = age
            dataf.at[index, 'tumor_status'] = tumor_status
            dataf.at[index, 'file_path'] = file_path

            edit_window.destroy()
            tree.item(item, values=(patient_id, age, tumor_status, file_path, ""))

        edit_button = tk.Button(edit_window, text="Update Patient", command=update_patient)
        edit_button.grid(row=4, columnspan=2)
        
        

def save_changes(dataf, fname):
    if fname:
        dataf.to_excel(fname, index=False)
        print("Changes saved successfully!")
    else:
        fname = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if fname:
            dataf.to_excel(fname, index=False)
            print("File saved successfully!")
            
            

def export_to_excel(dataf, filename_prefix='output'):
    tsdf = dataf['tumor_status']
    tsdf.to_excel(filename_prefix + '_labels.xlsx', index=False)

    file_path = dataf.loc[0]['file_path']
    raddf = pd.read_csv(file_path, sep='\t')
    raddf = raddf[raddf['Image type'] != 'diagnostics']
    featdf = raddf.iloc[:, 0:3]
    featdf.to_excel(filename_prefix + '_featurenames.xlsx', index=False)

    all_data = []
    for file_path in dataf['file_path']:
        raddf = pd.read_csv(file_path, sep='\t')
        raddf = raddf[raddf['Image type'] != 'diagnostics']
        featdf = raddf.iloc[:, 3]
        all_data.append(featdf.to_numpy().T)

    npdata = np.array(all_data)
    export_df = pd.DataFrame(npdata)
    export_filename = filename_prefix + '_features.xlsx'
    export_df.to_excel(export_filename, index=False)
    
    
    

def add_patient_window(tree, dataf):
    add_window = tk.Toplevel()
    add_window.title("Add New Patient")

    tk.Label(add_window, text="Patient ID:", fg="red").grid(row=0, column=0)
    tk.Label(add_window, text="Age:", fg="red").grid(row=1, column=0)
    tk.Label(add_window, text="Tumor/Benign:", fg="red").grid(row=2, column=0)
    tk.Label(add_window, text="File Path:", fg="red").grid(row=3, column=0)

    patient_id_entry = tk.Entry(add_window)
    age_entry = tk.Entry(add_window)
    tumor_status_combobox = ttk.Combobox(add_window, values=["Tumor", "Benign"])
    tumor_status_combobox.grid(row=2, column=1)
    tumor_status_combobox.set("Tumor")

    file_path_entry = tk.Entry(add_window)
    patient_id_entry.grid(row=0, column=1)
    age_entry.grid(row=1, column=1)
    file_path_entry.grid(row=3, column=1)

    def choose_file():
        file_path = fd.askopenfilename()
        if file_path:
            try:
                file_ext = file_path.split(".")[-1].lower()
                if file_ext == "xlsx":
                    df = pd.read_excel(file_path)
                elif file_ext == "tsv":
                    df = pd.read_csv(file_path, sep='\t')
                else:
                    tk.messagebox.showerror("File Error", "Unsupported file format. Please choose an Excel (xlsx) or TSV file.")
                    return

                num_rows, num_cols = df.shape
                if num_rows == 888 and num_cols == 4:
                    file_path_entry.delete(0, tk.END)
                    file_path_entry.insert(0, file_path)
                else:
                    tk.messagebox.showerror("File Error", f"Selected file should have 888 rows and 4 columns. Please choose a valid file.")
            except Exception as e:
                tk.messagebox.showerror("File Error", f"Error loading file: {str(e)}")

    file_button = tk.Button(add_window, text="Choose File", command=choose_file)
    file_button.grid(row=3, column=2)
    
    
    

    def add_patient():
        patient_id = patient_id_entry.get()
        age = age_entry.get()
        tumor_status = tumor_status_combobox.get()
        file_path = file_path_entry.get()

        dataf.loc[len(dataf)] = [patient_id, age, tumor_status, file_path]
        add_window.destroy()

        tree.delete(*tree.get_children())
        for i in range(len(dataf)):
            tree.insert("", i, text="", values=(dataf.loc[i]['patient_id'], dataf.loc[i]['age'], dataf.loc[i]['tumor_status'], dataf.loc[i]['file_path'], ""))

    add_button = tk.Button(add_window, text="Add Patient", command=add_patient)
    add_button.grid(row=4, columnspan=2)
    
    

def delete_patient(tree, dataf):
    selected_item = tree.selection()
    if selected_item:
        for item in selected_item:
            index = int(tree.index(item))
            dataf.drop(index, inplace=True)
        tree.delete(selected_item)



def start_new_project(dataf, root):
    save_changes(dataf, None)
    root.destroy()
    main()
    
    

if __name__ == "__main__":
    main()
