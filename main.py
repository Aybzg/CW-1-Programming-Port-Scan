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