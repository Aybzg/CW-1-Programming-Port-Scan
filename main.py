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