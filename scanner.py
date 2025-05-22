import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Event to control stopping the scan
stop_event = threading.Event()

def scan_port(host, port, text_widget):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            text_widget.insert(tk.END, f"Port {port}: OPEN\n")
        else:
            text_widget.insert(tk.END, f"Port {port}: Closed\n")
    except socket.error:
        text_widget.insert(tk.END, f"Port {port}: Error\n")

def scan(host, start_port, end_port, text_widget, btn_scan, btn_stop):
    for port in range(start_port, end_port + 1):
        if stop_event.is_set():
            text_widget.insert(tk.END, "Scan stopped by user.\n")
            break
        scan_port(host, port, text_widget)
    btn_scan.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)

def start_scan():
    host = entry_host.get()
    start_port = entry_start_port.get()
    end_port = entry_end_port.get()

    if not host or not start_port.isdigit() or not end_port.isdigit():
        text_result.insert(tk.END, "Please enter valid host and port numbers.\n")
        return

    start_port_int = int(start_port)
    end_port_int = int(end_port)

    text_result.delete('1.0', tk.END)
    text_result.insert(tk.END, f"Scanning {host} from port {start_port_int} to {end_port_int}...\n")

    stop_event.clear()  # Clear stop event before starting
    btn_scan.config(state=tk.DISABLED)  # Disable scan button during scan
    btn_stop.config(state=tk.NORMAL)    # Enable stop button

    # Run scan in a separate thread
    threading.Thread(target=scan, args=(host, start_port_int, end_port_int, text_result, btn_scan, btn_stop), daemon=True).start()

def stop_scan():
    stop_event.set()  # Signal the scan thread to stop
    btn_stop.config(state=tk.DISABLED)

# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Port Scanner")

tk.Label(root, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_host = tk.Entry(root, width=30)
entry_host.grid(row=0, column=1, padx=5, pady=5)
entry_host.insert(0, "127.0.0.1")

tk.Label(root, text="Start Port:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_start_port = tk.Entry(root, width=10)
entry_start_port.grid(row=1, column=1, padx=5, pady=5, sticky='w')
entry_start_port.insert(0, "1")

tk.Label(root, text="End Port:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_end_port = tk.Entry(root, width=10)
entry_end_port.grid(row=2, column=1, padx=5, pady=5, sticky='w')
entry_end_port.insert(0, "1024")

btn_scan = tk.Button(root, text="Scan", command=start_scan)
btn_scan.grid(row=3, column=0, pady=10)

btn_stop = tk.Button(root, text="Stop", command=stop_scan, state=tk.DISABLED)
btn_stop.grid(row=3, column=1, pady=10)

text_result = scrolledtext.ScrolledText(root, width=50, height=20)
text_result.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
