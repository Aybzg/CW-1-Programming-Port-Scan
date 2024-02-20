import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, Menu
import socket
import threading
import ipaddress

# Function to validate an IP address
def valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False
    
# Function to scan a single port
def scan_port(host, port, output, sem, results, status_var, scan_btn):
    with sem:  # Use semaphore to limit concurrency
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
                scanner.settimeout(1)
                result = scanner.connect_ex((host, port))
                if result == 0:
                    msg = f"Port {port}: Open\n"
                else:
                    msg = f"Port {port}: Closed\n"
                output.insert(tk.END, msg)
                results.append(msg)
        except Exception as e:
            msg = f"Error scanning port {port}: {e}\n"
            output.insert(tk.END, msg)
        finally:
            status_var.set(f"Completed scanning port {port}")
            if port == int(ports_entry.get().split('-')[1]):  # Check if it's the last port
                scan_btn.config(state=tk.NORMAL)
                status_var.set("Scan completed.")
# Main GUI application
def gui():
    app = tk.Tk()
    app.title("Cool Port Scanner")
    app.geometry("800x600")  # Set initial size of the window
    app.configure(bg='#333333')

    # Custom style
    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure("TLabel", background="#333333", foreground="#FFFFFF")
    style.configure("TButton", background="#333333", foreground="#FFFFFF", borderwidth=1)
    style.configure("TFrame", background="#333333", relief="flat")
    style.map("TButton", background=[('active', '#0052cc'), ('disabled', '#333333')])
    # Menu Bar
    menu_bar = Menu(app, bg="#333333", fg="#FFFFFF", relief=tk.FLAT)
    app.config(menu=menu_bar)

    # File Menu
    file_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#FFFFFF")
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Status Bar
    status_var = tk.StringVar()
    status_var.set("Ready")
    status_bar = ttk.Label(app, textvariable=status_var, background="#555555", foreground="#FFFFFF", relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Function to save results
    def save_results():
        text = output_text.get("1.0", tk.END)
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "w") as file_output:
                file_output.write(text)
            status_var.set("Results saved successfully.")
