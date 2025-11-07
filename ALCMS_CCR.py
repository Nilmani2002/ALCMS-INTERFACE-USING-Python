import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox

# # ---- CONFIG ----
# LEFT_LIGHT_NAMES = [f"Left {i}" for i in range(1, 16)]
# RIGHT_LIGHT_NAMES = [f"Right {i}" for i in range(1, 16)]
# # ----------------
LEFT_LIGHT_NAMES = ["NILMANI CKT-1", "RUNWAY EDGE CKT-2", "RUNWAY SPARE CCR", "TDZ CKT1", "TDZ CKT2", "TDZ SPARE CCR", "14 PAPI", "32 PAPI",
"RUNWAY C / L CKT-1", "RUNWAY C / L CKT-2", "14 APP SIDE ROW CKT-1", "14 APP SIDE ROW CKT-2", "14 APP C / L CKT-2", "A TAXI EDGE LIGHT", "B TAXI EDGE LIGHT"
]
RIGHT_LIGHT_NAMES = ["KAPIL CKT-1","C Taxi Stop Bar CKT-1","D Taxi Stop Bar CKT-1","E Taxi Stop Bar CKT-1","F Taxi Stop Bar CKT-1","G Taxi Stop Bar CKT-1","H Taxi Stop Bar CKT-1","I Taxi Stop Bar CKT-1","J Taxi Stop Bar CKT-1","K Taxi Stop Bar CKT-1","L Taxi Stop Bar CKT-1","M Taxi Stop Bar CKT-1","N Taxi Stop Bar CKT-1","14 Turn Pad CKT-1","14 Turn Pad CKT-2"]


ser_connections = {}
light_selected = {}
light_status_labels = {}
light_frames = {}
light_names = {}  # store light_id -> name mapping

def connect(light_id, combo):
    port = combo.get()
    if not port:
        messagebox.showerror("Error", f"Select a COM port for {light_names[light_id]}!")
        return
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        ser_connections[light_id] = ser
        messagebox.showinfo("Connected", f"{light_names[light_id]} connected to {port}")
    except Exception as e:
        messagebox.showerror("Connection Failed", str(e))

def toggle_light(light_id):
    light_selected[light_id] = not light_selected.get(light_id, False)
    frame = light_frames[light_id]
    if light_selected[light_id]:
        frame.config(bg="lightgreen")
    else:
        frame.config(bg="SystemButtonFace")

def send_command(cmd):
    selected = [lid for lid, sel in light_selected.items() if sel]
    if not selected:
        messagebox.showwarning("No Selection", "Please click at least one light!")
        return

    for light_id in selected:
        ser = ser_connections.get(light_id)
        if ser and ser.is_open:
            ser.write(f"{cmd}\n".encode())
            update_status(light_id, cmd)
        else:
            messagebox.showwarning("Not Connected", f"{light_names[light_id]} not connected!")

def update_status(light_id, cmd):
    label = light_status_labels.get(light_id)
    if label:
        label.config(text=f"Status: {cmd}")


def build_light_panel(parent, light_list, start_id):
    ports = [port.device for port in serial.tools.list_ports.comports()]

    # Header row
    tk.Label(parent, text="AIRFIELD CCR CIRCUIT", bg="black",fg = "Yellow",  width=27, font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=2)
    tk.Label(parent, text="COM PORT", bg="black",fg = "Yellow", width=15,font=("Arial", 9, "bold")).grid(row=0, column=1, padx=5, pady=2)
    tk.Label(parent, text="CONNECT", bg="black",fg = "Yellow", width=20,font=("Arial", 9, "bold")).grid(row=0, column=2, padx=5, pady=2)
    tk.Label(parent, text="STATUS", bg="black",fg = "Yellow", width=15,font=("Arial", 9, "bold")).grid(row=0, column=3, padx=5, pady=2)

    for idx, name in enumerate(light_list):
        light_id = start_id + idx
        light_names[light_id] = name
        row_num = idx + 1

        # Light name (label) with click to select
        lbl = tk.Label(parent, text=name, width=27,height =2, anchor="center", relief="ridge", bd=1)
        lbl.grid(row=row_num, column=0, padx=5, pady=2)
        lbl.bind("<Button-1>", lambda e, lid=light_id: toggle_light(lid))

        # COM port dropdown
        port_combo = ttk.Combobox(parent, values=ports, state="readonly", width=15)
        port_combo.grid(row=row_num, column=1, padx=5, pady=2)

        # Connect button
        btn_connect = tk.Button(parent, text="Connect",
                                command=lambda lid=light_id, combo=port_combo: connect(lid, combo),
                                width=15)
        btn_connect.grid(row=row_num, column=2, padx=5, pady=2)

        # Status label
        status_label = tk.Label(parent, text="Status: Unknown", width=15, anchor="w")
        status_label.grid(row=row_num, column=3, padx=5, pady=2)

        # Save references
        light_status_labels[light_id] = status_label
        light_selected[light_id] = False
        light_frames[light_id] = lbl  # Use the label itself to change bg when selected
        
def toggle_light(light_id):
    light_selected[light_id] = not light_selected.get(light_id, False)
    frame = light_frames[light_id]
    if light_selected[light_id]:
        frame.config(bg="lightgreen")
    else:
        frame.config(bg="SystemButtonFace")


def build_gui():
    # Title
    title = tk.Label(root, text="Vardhman Airport Solution'S-Airfield Lighting Control and Monitoring System (ALCMS)",
                     bg="yellow", fg="red", font=("Arial", 20, "bold"),pady=5)
    title.pack(fill="x")

    # Two panels side by side
    panel_frame = tk.Frame(root)
    panel_frame.pack(fill="both", expand=True, padx=5, pady=5)

    left_panel = tk.Frame(panel_frame, bd=2, relief="solid")
    left_panel.pack(side="left", fill="both", expand=True, padx=5)

    right_panel = tk.Frame(panel_frame, bd=2, relief="solid")
    right_panel.pack(side="right", fill="both", expand=True, padx=5)

    build_light_panel(left_panel, LEFT_LIGHT_NAMES, 1)
    build_light_panel(right_panel, RIGHT_LIGHT_NAMES, len(LEFT_LIGHT_NAMES) + 1)

    # Bottom control buttons
    control_frame = tk.Frame(root)
    control_frame.pack(fill="x", pady=0)

    controls = [
        ("On", "ON"),
        ("Off", "OFF"),
        ("2.8A", "2.8A"),
        ("3.4A", "3.4A"),
        ("4.1A", "4.1A"),
        ("5.2A", "5.2A"),
        ("6.6A", "6.6A")
    ]

    for label, cmd in controls:
        btn = tk.Button(control_frame, text=label,font=("Arial", 14, "bold"),bg="black",fg = "Yellow",
                        width=14, height=4,	
                        command=lambda c=cmd: send_command(c))
        btn.pack(side="left", padx=5, pady=5)

# --- GUI START ---
root = tk.Tk()
root.title("Vardhman Airport Solution ")
# root.geometry("800x600")
root.attributes('-fullscreen', True)
   

build_gui()

root.mainloop()

# # Close all ports on exit
for ser in ser_connections.values():
    if ser and ser.is_open:
        ser.close()
