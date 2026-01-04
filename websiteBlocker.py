import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime as dt
import threading
import time

class WebsiteBlockerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Mode: Website Blocker")
        self.root.geometry("400x500")

        # Configuration
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect = "127.0.0.1"
        self.website_list = ["www.facebook.com", "www.youtube.com", "www.instagram.com", "x.com"]
        self.running = False

        self.setup_ui()

    def setup_ui(self):
        # Time Selection
        time_frame = tk.LabelFrame(self.root, text="Blocking Hours (24h Format)", padx=10, pady=10)
        time_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(time_frame, text="Start Hour:").grid(row=0, column=0)
        self.start_hour = tk.Spinbox(time_frame, from_=0, to=23, width=5)
        self.start_hour.delete(0, "end")
        self.start_hour.insert(0, "8")
        self.start_hour.grid(row=0, column=1, padx=5)

        tk.Label(time_frame, text="End Hour:").grid(row=0, column=2)
        self.end_hour = tk.Spinbox(time_frame, from_=0, to=23, width=5)
        self.end_hour.delete(0, "end")
        self.end_hour.insert(0, "19")
        self.end_hour.grid(row=0, column=3, padx=5)

        # Website Management
        list_frame = tk.LabelFrame(self.root, text="Blocked Websites", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.site_entry = tk.Entry(list_frame)
        self.site_entry.pack(fill="x", pady=2)
        
        btn_add = tk.Button(list_frame, text="Add Website", command=self.add_site)
        btn_add.pack(fill="x", pady=2)

        self.site_listbox = tk.Listbox(list_frame)
        for site in self.website_list:
            self.site_listbox.insert(tk.END, site)
        self.site_listbox.pack(fill="both", expand=True, pady=2)

        btn_remove = tk.Button(list_frame, text="Remove Selected", command=self.remove_site)
        btn_remove.pack(fill="x", pady=2)

        # Control Button
        self.status_var = tk.StringVar(value="Status: Idle")
        tk.Label(self.root, textvariable=self.status_var).pack()

        self.toggle_btn = tk.Button(self.root, text="Start Blocker", bg="green", fg="white", 
                                   command=self.toggle_blocker, height=2)
        self.toggle_btn.pack(fill="x", padx=10, pady=10)

    def add_site(self):
        site = self.site_entry.get().strip()
        if site and site not in self.website_list:
            self.website_list.append(site)
            self.site_listbox.insert(tk.END, site)
            self.site_entry.delete(0, tk.END)

    def remove_site(self):
        try:
            selection = self.site_listbox.curselection()
            site = self.site_listbox.get(selection)
            self.website_list.remove(site)
            self.site_listbox.delete(selection)
        except:
            pass

    def toggle_blocker(self):
        if not self.running:
            self.running = True
            self.toggle_btn.config(text="Stop Blocker", bg="red")
            self.status_var.set("Status: Active")
            # Run the blocking logic in a separate thread so the GUI doesn't freeze
            threading.Thread(target=self.blocker_loop, daemon=True).start()
        else:
            self.running = False
            self.toggle_btn.config(text="Start Blocker", bg="green")
            self.status_var.set("Status: Idle (Cleaning hosts...)")
            self.clean_hosts()

    def blocker_loop(self):
        while self.running:
            now = dt.now()
            start = int(self.start_hour.get())
            end = int(self.end_hour.get())
            
            start_time = dt(now.year, now.month, now.day, start)
            end_time = dt(now.year, now.month, now.day, end)

            try:
                if start_time < now < end_time:
                    with open(self.hosts_path, 'r+') as file:
                        content = file.read()
                        for website in self.website_list:
                            if website not in content:
                                file.write(f"{self.redirect} {website}\n")
                else:
                    self.clean_hosts()
            except PermissionError:
                messagebox.showerror("Error", "Please run this app as Administrator!")
                self.running = False
                break
            
            time.sleep(10) # Checks every 10 seconds while running

    def clean_hosts(self):
        try:
            with open(self.hosts_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if not any(site in line for site in self.website_list):
                        file.write(line)
                file.truncate()
        except PermissionError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteBlockerGUI(root)
    root.mainloop()