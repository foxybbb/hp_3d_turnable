import serial
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class TurntableGUI:
    STEPS_PER_DEGREE = 31.205  # 1 degree = 31.205 steps

    def __init__(self, master):
        self.master = master
        self.master.title("Turntable Control")

        # Port settings
        tk.Label(master, text="COM Port:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, "COM3")  # Change if necessary
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(master, text="Baud Rate:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.baud_entry = tk.Entry(master)
        self.baud_entry.insert(0, "9600")  # Set the required baud rate
        self.baud_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Connect button
        self.connect_button = tk.Button(master, text="Connect", command=self.connect_port)
        self.connect_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky="ns")

        # Log window
        self.log_area = scrolledtext.ScrolledText(master, width=60, height=10, state='disabled')
        self.log_area.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Current angle in degrees
        self.current_angle = 0
        self.angle_label = tk.Label(master, text=f"Current angle: {self.current_angle}°")
        self.angle_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Predefined movement buttons (+1, +5, +10, +45, +90 and their negatives)
        moves = [1, 5, 10, 45, 90]
        frame_moves = tk.Frame(master)
        frame_moves.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        for i, val in enumerate(moves):
            btn_plus = tk.Button(frame_moves, text=f"+{val}°",
                                 command=lambda v=val: self.move_table(v))
            btn_minus = tk.Button(frame_moves, text=f"-{val}°",
                                  command=lambda v=-val: self.move_table(v))
            btn_plus.grid(row=0, column=i, padx=3, pady=3)
            btn_minus.grid(row=1, column=i, padx=3, pady=3)

        # Custom angle input
        tk.Label(master, text="Custom Angle (°):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.custom_angle_entry = tk.Entry(master)
        self.custom_angle_entry.grid(row=5, column=1, padx=5, pady=5)
        self.custom_move_button = tk.Button(master, text="Move Custom", command=self.move_custom_angle)
        self.custom_move_button.grid(row=5, column=2, padx=5, pady=5)

        # Button to return to 0°
        self.reset_button = tk.Button(master, text="Return to 0°", command=self.reset_angle)
        self.reset_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Disconnect button
        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_port)
        self.disconnect_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        # Serial port variables
        self.serial_port = None
        self.read_thread = None
        self.stop_reading = False

    def connect_port(self):
        """Connect to the specified COM port."""
        if self.serial_port and self.serial_port.is_open:
            self.write_log("Already connected.")
            return
        
        port = self.port_entry.get()
        baud = self.baud_entry.get()
        try:
            self.serial_port = serial.Serial(port, int(baud), timeout=0.1)
            self.write_log(f"Connected to {port} at {baud} baud.")
            self.stop_reading = False
            self.read_thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.read_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open port: {e}")

    def disconnect_port(self):
        """Disconnect from the port and stop reading."""
        self.stop_reading = True
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.write_log("Port closed.")

    def read_from_port(self):
        """Read incoming data from the port in a separate thread."""
        while not self.stop_reading and self.serial_port and self.serial_port.is_open:
            try:
                data = self.serial_port.readline()
                if data:
                    text = data.decode(errors='ignore').strip()
                    self.write_log(f"Received: {text}")
            except:
                pass

    def move_table(self, degrees):
        """Move the turntable by the specified number of degrees."""
        if not (self.serial_port and self.serial_port.is_open):
            self.write_log("Please connect to a port first.")
            return
        steps = degrees * self.STEPS_PER_DEGREE
        cmd_to_send = f"move {steps}\n"
        self.serial_port.write(cmd_to_send.encode())
        self.write_log(f"Sent: move {steps:.3f} steps (~ {degrees}°)")
        self.current_angle += degrees
        self.update_angle_label()

    def move_custom_angle(self):
        """Move the turntable using a custom angle from the input box."""
        try:
            custom_angle = float(self.custom_angle_entry.get())
        except ValueError:
            self.write_log("Invalid custom angle value.")
            return
        self.move_table(custom_angle)

    def reset_angle(self):
        """Return the turntable to zero degrees."""
        if not (self.serial_port and self.serial_port.is_open):
            self.write_log("Please connect to a port first.")
            return
        if self.current_angle != 0:
            steps_back = -self.current_angle * self.STEPS_PER_DEGREE
            cmd_to_send = f"move {steps_back}\n"
            self.serial_port.write(cmd_to_send.encode())
            self.write_log(f"Sent: move {steps_back:.3f} steps (return to 0°)")
            self.current_angle = 0
            self.update_angle_label()
        else:
            self.write_log("The turntable is already at 0°.")

    def update_angle_label(self):
        """Update the label showing the current angle."""
        self.angle_label.config(text=f"Current angle: {self.current_angle}°")

    def write_log(self, message):
        """Write a message to the log window."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')


def main():
    root = tk.Tk()
    app = TurntableGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
