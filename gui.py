import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial

# Core Data Structures remain the same
class Patient:
    def __init__(self, id, name, severity):
        self.id = id
        self.name = name
        self.severity = severity
        self.left = None
        self.right = None

class PriorityNode:
    def __init__(self, id, name, severity):
        self.id = id
        self.name = name
        self.severity = severity
        self.next = None

class HospitalManagementSystem:
    def __init__(self):
        self.bst_root = None
        self.priority_queue_head = None

    # ... [Previous methods remain the same] ...
    def insert_bst(self, root, id, name, severity):
        if root is None:
            return Patient(id, name, severity)
        if id < root.id:
            root.left = self.insert_bst(root.left, id, name, severity)
        else:
            root.right = self.insert_bst(root.right, id, name, severity)
        return root

    def inorder_bst(self, root, result):
        if root:
            self.inorder_bst(root.left, result)
            result.append(f"ID: {root.id}, Name: {root.name}, Severity: {root.severity}")
            self.inorder_bst(root.right, result)

    def insert_priority_queue(self, id, name, severity):
        new_node = PriorityNode(id, name, severity)
        if not self.priority_queue_head or severity > self.priority_queue_head.severity:
            new_node.next = self.priority_queue_head
            self.priority_queue_head = new_node
            return
        current = self.priority_queue_head
        while current.next and current.next.severity >= severity:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def dequeue_priority_queue(self):
        if not self.priority_queue_head:
            return "Queue is empty."
        served_patient = f"ID: {self.priority_queue_head.id}, Name: {self.priority_queue_head.name}"
        self.priority_queue_head = self.priority_queue_head.next
        return f"Served patient: {served_patient}"

    def display_priority_queue(self):
        result = []
        current = self.priority_queue_head
        while current:
            result.append(f"ID: {current.id}, Name: {current.name}, Severity: {current.severity}")
            current = current.next
        return "\n".join(result)

class EnhancedGUI:
    def __init__(self):
        self.hms = HospitalManagementSystem()
        self.setup_main_window()
        self.setup_styles()
        self.create_notebook()
        self.create_input_frame()
        self.create_bst_tab()
        self.create_pq_tab()

    def setup_main_window(self):
        self.root = tk.Tk()
        self.root.title("Hospital Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
    def setup_styles(self):
        # Configure styles for widgets
        style = ttk.Style()
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        # Custom button style
        self.button_style = {
            "font": ("Arial", 10),
            "bg": "#4a90e2",
            "fg": "white",
            "activebackground": "#357abd",
            "activeforeground": "white",
            "relief": tk.RAISED,
            "padx": 20,
            "pady": 5
        }
        
        # Warning button style (for serve patient)
        self.warning_button_style = self.button_style.copy()
        self.warning_button_style["bg"] = "#e74c3c"
        self.warning_button_style["activebackground"] = "#c0392b"

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

    def create_input_frame(self):
        # Create and store input widgets
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.severity_var = tk.StringVar()

    def create_input_fields(self, parent):
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill='x', padx=20, pady=10)

        # Grid layout for input fields
        labels = [("ID:", self.id_var), 
                 ("Name:", self.name_var), 
                 ("Severity:", self.severity_var)]
        
        for i, (label_text, var) in enumerate(labels):
            ttk.Label(input_frame, text=label_text, style="Header.TLabel").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(input_frame, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')

        input_frame.grid_columnconfigure(1, weight=1)
        return input_frame

    def create_bst_tab(self):
        self.bst_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bst_frame, text="BST Operations")

        # Header
        ttk.Label(self.bst_frame, text="Binary Search Tree Management", 
                 style="Header.TLabel").pack(pady=10)

        # Input fields
        self.create_input_fields(self.bst_frame)

        # Buttons frame
        button_frame = ttk.Frame(self.bst_frame)
        button_frame.pack(fill='x', padx=20, pady=10)

        # BST Buttons
        tk.Button(button_frame, text="Add to BST", 
                 command=lambda: self.add_patient_bst(), 
                 **self.button_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Display BST", 
                 command=lambda: self.display_bst(), 
                 **self.button_style).pack(side=tk.LEFT, padx=5)

        # Output area
        self.bst_output = tk.Text(self.bst_frame, height=15, width=60)
        self.bst_output.pack(padx=20, pady=10, fill='both', expand=True)

    def create_pq_tab(self):
        self.pq_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pq_frame, text="Priority Queue Operations")

        # Header
        ttk.Label(self.pq_frame, text="Priority Queue Management", 
                 style="Header.TLabel").pack(pady=10)

        # Input fields
        self.create_input_fields(self.pq_frame)

        # Buttons frame
        button_frame = ttk.Frame(self.pq_frame)
        button_frame.pack(fill='x', padx=20, pady=10)

        # Priority Queue Buttons
        tk.Button(button_frame, text="Add to Queue", 
                 command=lambda: self.add_priority_queue(), 
                 **self.button_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Serve Next Patient", 
                 command=lambda: self.serve_priority_queue(), 
                 **self.warning_button_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Display Queue", 
                 command=lambda: self.display_priority_queue(), 
                 **self.button_style).pack(side=tk.LEFT, padx=5)

        # Output area
        self.pq_output = tk.Text(self.pq_frame, height=15, width=60)
        self.pq_output.pack(padx=20, pady=10, fill='both', expand=True)

    def clear_inputs(self):
        self.id_var.set("")
        self.name_var.set("")
        self.severity_var.set("")

    def get_input_values(self):
        try:
            id_val = int(self.id_var.get())
            name_val = self.name_var.get().strip()
            severity_val = int(self.severity_var.get())
            
            if not name_val:
                raise ValueError("Name cannot be empty")
            if severity_val < 1 or severity_val > 10:
                raise ValueError("Severity must be between 1 and 10")
                
            return id_val, name_val, severity_val
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None

    def add_patient_bst(self):
        values = self.get_input_values()
        if values:
            id_val, name_val, severity_val = values
            self.hms.bst_root = self.hms.insert_bst(self.hms.bst_root, id_val, name_val, severity_val)
            self.bst_output.insert(tk.END, f"Patient added to BST: ID={id_val}, Name={name_val}, Severity={severity_val}\n")
            self.clear_inputs()

    def display_bst(self):
        result = []
        self.hms.inorder_bst(self.hms.bst_root, result)
        self.bst_output.delete(1.0, tk.END)
        self.bst_output.insert(tk.END, "BST Records (Inorder):\n" + "\n".join(result) + "\n")

    def add_priority_queue(self):
        values = self.get_input_values()
        if values:
            id_val, name_val, severity_val = values
            self.hms.insert_priority_queue(id_val, name_val, severity_val)
            self.pq_output.insert(tk.END, f"Patient added to Priority Queue: ID={id_val}, Name={name_val}, Severity={severity_val}\n")
            self.clear_inputs()

    def serve_priority_queue(self):
        result = self.hms.dequeue_priority_queue()
        self.pq_output.insert(tk.END, result + "\n")

    def display_priority_queue(self):
        result = self.hms.display_priority_queue()
        self.pq_output.delete(1.0, tk.END)
        self.pq_output.insert(tk.END, "Priority Queue:\n" + result + "\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedGUI()
    app.run()