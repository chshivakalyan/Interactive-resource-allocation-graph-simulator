import tkinter as tk
from tkinter import ttk, messagebox
from allocation import ResourceManager
from visualization import GraphVisualizer


class ResourceAllocationApp:
    def __init__(self):
        # ===============================
        # Main Window Setup
        # ===============================
        self.root = tk.Tk()
        self.root.title("Interactive Resource Allocation Simulator")
        self.root.geometry("1200x800")

        # Backend manager
        self.manager = ResourceManager()

        # -------------------------------
        # Styling
        # -------------------------------
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 11))

        # Root grid config
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_widgets()

        # Graph visualizer
        self.visualizer = GraphVisualizer(self.manager, self.canvas)
        self.visualizer.show_graph()

    def create_widgets(self):
        # ===============================
        # Main Container
        # ===============================
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=0)  # controls
        main_frame.columnconfigure(1, weight=1)  # visualization
        main_frame.rowconfigure(1, weight=1)

        # ===============================
        # Controls Frame
        # ===============================
        input_frame = ttk.LabelFrame(main_frame, text="Controls", padding=15)
        input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Input layout
        input_frame.columnconfigure(0, weight=0)
        input_frame.columnconfigure(1, weight=1)

        # ---- Process Input ----
        ttk.Label(input_frame, text="Process:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        self.process_entry = ttk.Entry(input_frame, width=20)
        self.process_entry.grid(row=0, column=1, padx=5, pady=5)

        # ---- Resource Input ----
        ttk.Label(input_frame, text="Resource:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.resource_entry = ttk.Entry(input_frame, width=20)
        self.resource_entry.grid(row=1, column=1, padx=5, pady=5)

        # ===============================
        # Button Grid (Equal Size 2×2)
        # ===============================
        # Make two equal-width columns for buttons
        input_frame.columnconfigure(0, weight=1, uniform="buttons")
        input_frame.columnconfigure(1, weight=1, uniform="buttons")

        # Make rows equal height (optional but recommended)
        input_frame.rowconfigure(2, weight=1)
        input_frame.rowconfigure(3, weight=1)

        # ---- Buttons ----
        ttk.Button(
            input_frame, text="Allocate", command=self.allocate_resource
        ).grid(row=2, column=0, sticky="nsew", pady=5, padx=3)

        ttk.Button(
            input_frame, text="Release", command=self.release_resource
        ).grid(row=2, column=1, sticky="nsew", pady=5, padx=3)

        ttk.Button(
            input_frame, text="Check Deadlock", command=self.check_deadlock
        ).grid(row=3, column=0, sticky="nsew", pady=5, padx=3)

        ttk.Button(
            input_frame, text="Clear All", command=self.clear_log
        ).grid(row=3, column=1, sticky="nsew", pady=5, padx=3)

        # ===============================
        # Status Frame
        # ===============================
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding=10)
        status_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)

        self.status_text = tk.Text(status_frame, height=10, width=45)
        self.status_text.grid(row=0, column=0, sticky="nsew")

        # ===============================
        # Visualization Frame
        # ===============================
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding=5)
        viz_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(viz_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

    # ===============================
    # Button Actions
    # ===============================
    def allocate_resource(self):
        process = self.process_entry.get().strip()
        resource = self.resource_entry.get().strip()

        if process and resource:
            message = self.manager.allocate(process, resource)
            self.status_text.insert(tk.END, message + "\n")
            self.process_entry.delete(0, tk.END)
            self.resource_entry.delete(0, tk.END)
            self.visualizer.show_graph()
        else:
            messagebox.showerror("Input Error", "Please enter both process and resource.")

    def release_resource(self):
        process = self.process_entry.get().strip()
        resource = self.resource_entry.get().strip()

        if process and resource:
            message = self.manager.release(process, resource)
            if "No allocation" in message:
                messagebox.showerror("Error", message)
            else:
                self.status_text.insert(tk.END, message + "\n")

            self.process_entry.delete(0, tk.END)
            self.resource_entry.delete(0, tk.END)
            self.visualizer.show_graph()
        else:
            messagebox.showerror("Input Error", "Please enter both process and resource.")

    def check_deadlock(self):
        has_deadlock, message = self.manager.detect_deadlock()
        self.status_text.insert(tk.END, message + "\n")

        if has_deadlock:
            messagebox.showwarning("Deadlock Alert", message)
        else:
            messagebox.showinfo("Deadlock Check", message)

    def clear_log(self):
        message = self.manager.clear_all()
        self.status_text.insert(tk.END, message + "\n")
        self.visualizer.show_graph()

    # ===============================
    # App Runner
    # ===============================
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ResourceAllocationApp()
    app.run()
