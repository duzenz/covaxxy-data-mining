import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from PIL import ImageTk, Image


class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.file_label = tk.Label(self, text="")
        self.file_label.pack()

        self.select_file_button = tk.Button(self, text="Select File", command=self.select_file)
        self.select_file_button.pack()

        self.run_script_button = tk.Button(self, text="Run Script", command=self.run_script_create_networks)
        self.run_script_button.pack()

        self.create_communities_button = tk.Button(self, text="Find Communities", command=self.run_script_find_communities)
        self.create_communities_button.pack()

        self.calculate_centrality_button = tk.Button(self, text="Calculate Centralities", command=self.run_script_calculate_metrics)
        self.calculate_centrality_button.pack()

        self.find_misinformation_button = tk.Button(self, text="Find Misinformation", command=self.run_script_find_misinformation)
        self.find_misinformation_button.pack()

        self.show_networks_button = tk.Button(self, text="Show Networks", command=self.show_network)
        self.show_networks_button.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.master.quit)
        self.quit_button.pack()

        self.progress_bar = tk.ttk.Progressbar(self, mode='indeterminate')

        self.log_text = tk.Text(self, height=20, width=50)
        self.log_text.pack()

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=self.file_path)

    def show_network(self):
        try:
            img1 = ImageTk.PhotoImage(Image.open("networks/replies_communities.png"))
            self.image_label_1.config(image=img1)
            self.image_label_1.image = img1
            self.image_label_1.pack(side="left")
        except FileNotFoundError:
            self.log_text.insert(tk.END, "Error: Could not find replies_communities.png.\n")
            self.log_text.see(tk.END)

        try:
            img2 = ImageTk.PhotoImage(Image.open("networks/mentions_communities.png"))
            self.image_label_2.config(image=img2)
            self.image_label_2.image = img2
            self.image_label_2.pack(side="left")
        except FileNotFoundError:
            self.log_text.insert(tk.END, "Error: Could not find mentions_communities.png.\n")
            self.log_text.see(tk.END)

        try:
            img3 = ImageTk.PhotoImage(Image.open("networks/retweets_communities.png"))
            self.image_label_3.config(image=img3)
            self.image_label_3.image = img3
            self.image_label_3.pack(side="left")
        except FileNotFoundError:
            self.log_text.insert(tk.END, "Error: Could not find retweets_communities.png.\n")
            self.log_text.see(tk.END)

    def run_script_create_networks(self):
        if self.file_path:
            self.run_script_button.config(state='disabled')
            self.select_file_button.config(state='disabled')
            self.progress_bar.pack()
            self.progress_bar.start()

            t = threading.Thread(target=self.run_script_create_networks_thread)
            t.start()

    def run_script_create_networks_thread(self):
        self.log_text.insert(tk.END, "Processing started\n")
        self.log_text.insert(tk.END, "Selected file: " + self.file_path + "\n")

        create_network_script = subprocess.Popen([sys.executable, "create_networks.py", self.file_path], stdout=subprocess.PIPE)
        for line in iter(create_network_script.stdout.readline, b''):
            self.log_text.insert(tk.END, line.decode('utf-8'))
        create_network_script.communicate()

        self.run_script_button.config(state='normal')
        self.select_file_button.config(state='normal')
        self.progress_bar.pack_forget()

    def run_script_find_communities(self):
        self.run_script_button.config(state='disabled')
        self.select_file_button.config(state='disabled')
        self.progress_bar.pack()
        self.progress_bar.start()
        t = threading.Thread(target=self.run_script_find_communities_thread)
        t.start()

    def run_script_find_communities_thread(self):
        self.log_text.insert(tk.END, "Processing started\n")
        self.log_text.insert(tk.END, "Process communities" + "\n")

        process = subprocess.Popen([sys.executable, "read_networks_find_communities.py"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            self.log_text.insert(tk.END, line.decode('utf-8'))
        process.communicate()

        self.run_script_button.config(state='normal')
        self.select_file_button.config(state='normal')
        self.progress_bar.pack_forget()

    def run_script_find_misinformation(self):
        t = threading.Thread(target=self.run_script_find_misinformation_thread)
        t.start()

    def run_script_find_misinformation_thread(self):
        process = subprocess.Popen([sys.executable, "find_misinformation.py"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            self.log_text.insert(tk.END, line.decode('utf-8'))
        process.communicate()

    def run_script_calculate_metrics(self):
        # disable buttons
        t = threading.Thread(target=self.run_script_calculate_metrics_thread)
        t.start()

    def run_script_calculate_metrics_thread(self):
        process = subprocess.Popen([sys.executable, "calculate_metrics_for_networks.py"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            self.log_text.insert(tk.END, line.decode('utf-8'))
        process.communicate()


root = tk.Tk()
root.title("Misinformation Framework")
root.maxsize(900, 600)
root.config(bg="skyblue")

app = App(master=root)
app.mainloop()


