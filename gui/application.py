import csv
import os
import subprocess
import sys
import threading
import tkinter
import tkinter as tk
from tkinter import filedialog, HORIZONTAL, VERTICAL, RIGHT, BOTTOM, Y, X, W, NO
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Frame, Label, Button

from PIL import ImageTk, Image
from PIL.Image import Resampling


class App(Frame):

    def __init__(self):
        super().__init__()
        self.open_report_button = None
        self.log_text = None
        self.progress_bar = None
        self.find_misinformation_button = None
        self.calculate_centrality_button = None
        self.create_communities_button = None
        self.file_path = None
        self.show_networks_button = None
        self.create_network_button = None
        self.select_file_button = None
        self.file_label = None
        self.create_widgets()

    def create_widgets(self):

        self.left_frame = Frame(root, width=250, height=500)
        self.left_frame.grid(row=0, column=0, padx=20, pady=5)

        self.right_frame_top = Frame(root, width=650, height=300)
        self.right_frame_top.grid(row=0, column=1, padx=10, pady=5)

        self.right_frame_bottom = Frame(root, width=650, height=200)
        self.right_frame_bottom.grid(row=1, column=1, padx=10, pady=5)

        self.file_label = Label(self, text="")
        self.select_file_button = Button(self.left_frame, text="Select File", command=self.select_file)
        self.select_file_button.grid(sticky="EW", row=0, column=0, padx=5, pady=5)
        self.create_network_button = Button(self.left_frame, text="Create Networks", command=self.run_script_create_networks)
        self.create_network_button.grid(sticky="EW", row=1, column=0, padx=5, pady=5)
        self.show_networks_button = Button(self.left_frame, text="Show Network Info", command=self.show_network)
        self.show_networks_button.grid(sticky="EW", row=2, column=0, padx=5, pady=5)
        self.create_communities_button = Button(self.left_frame, text="Find Communities", command=self.run_script_find_communities)
        self.create_communities_button.grid(sticky="EW", row=3, column=0, padx=5, pady=5)
        self.calculate_centrality_button = Button(self.left_frame, text="Calculate Centrality", command=self.run_script_calculate_metrics)
        self.calculate_centrality_button.grid(sticky="EW", row=4, column=0, padx=5, pady=5)
        self.find_misinformation_button = Button(self.left_frame, text="Find Misinformation", command=self.run_script_find_misinformation)
        self.find_misinformation_button.grid(sticky="EW", row=5, column=0, padx=5, pady=5)
        self.open_report_button = Button(self.left_frame, text="Open Report", command=self.open_report)
        self.open_report_button.grid(sticky="EW", row=6, column=0, padx=5, pady=5)
        self.open_report_button.grid_remove()
        self.progress_bar = tk.ttk.Progressbar(self.left_frame, mode='indeterminate')

        self.log_text = ScrolledText(self.right_frame_bottom, width=61, height=8, font=("Times New Roman", 15))
        self.log_text.grid(column=0, pady=10, padx=10)
        self.log_text.configure(state='disabled')

    def open_report(self):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        os.startfile(file_dir + '/report/importance-report.csv', 'open')

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=self.file_path)
            self.show_dataset_title = Label(self.right_frame_top, text="Dataset file: " + self.file_path.rsplit('/', 1)[1],
                                            font=('Helvetica', 14, 'bold'))
            self.show_dataset_title.place(x=150, y=10)

    def disable_buttons(self):
        self.select_file_button.config(state='disabled')
        self.create_network_button.config(state='disabled')
        self.show_networks_button.config(state='disabled')
        self.create_communities_button.config(state='disabled')
        self.calculate_centrality_button.config(state='disabled')
        self.find_misinformation_button.config(state='disabled')
        self.progress_bar.grid(sticky="EW", row=7, column=0, padx=5, pady=5)
        self.progress_bar.start()

    def enable_buttons(self):
        self.select_file_button.config(state='normal')
        self.create_network_button.config(state='normal')
        self.show_networks_button.config(state='normal')
        self.create_communities_button.config(state='normal')
        self.calculate_centrality_button.config(state='normal')
        self.find_misinformation_button.config(state='normal')
        self.progress_bar.stop()
        self.progress_bar.grid_remove()

    def insert_log(self, text):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def run_script_create_networks(self):
        if self.file_path is not None:
            self.disable_buttons()
            t = threading.Thread(target=self.run_script_create_networks_thread)
            t.start()
        else:
            self.insert_log("Tweets report is not selected\n")

    def run_script_create_networks_thread(self):
        self.insert_log("Processing started\n")
        self.insert_log("Selected file: " + self.file_path + "\n")

        create_network_script = subprocess.Popen([sys.executable, "create_networks.py", self.file_path], stdout=subprocess.PIPE)
        for line in iter(create_network_script.stdout.readline, b''):
            self.insert_log(line.decode('utf-8'))
        create_network_script.communicate()
        self.enable_buttons()

    def show_network(self):
        try:
            retweets_image = ImageTk.PhotoImage(Image.open("networks/retweets_communities.png").resize((200, 200), Resampling.LANCZOS))
            label1 = Label(self.right_frame_top, image=retweets_image, compound='top', text='Retweet Network')
            label1.image = retweets_image
            label1.place(x=25, y=50)
        except FileNotFoundError:
            self.insert_log("Error: Could not find retweets_communities.png.\n")

        try:
            mentions_image = ImageTk.PhotoImage(Image.open("networks/mentions_communities.png").resize((200, 200), Resampling.LANCZOS))
            label1 = Label(self.right_frame_top, image=mentions_image, compound='top', text='Mention Network')
            label1.image = mentions_image
            label1.place(x=225, y=50)
        except FileNotFoundError:
            self.insert_log("Error: Could not find mentions_communities.png.\n")

        try:
            replies_image = ImageTk.PhotoImage(Image.open("networks/replies_communities.png").resize((200, 200), Resampling.LANCZOS))
            label1 = Label(self.right_frame_top, image=replies_image, compound='top', text='Reply Network')
            label1.image = replies_image
            label1.place(x=425, y=50)
        except FileNotFoundError:
            self.insert_log("Error: Could not find replies_communities.png.\n")

    def run_script_find_communities(self):
        self.disable_buttons()
        t = threading.Thread(target=self.run_script_find_communities_thread)
        t.start()

    def run_script_find_communities_thread(self):
        self.insert_log("Processing started\n")
        self.insert_log("Process communities" + "\n")

        process = subprocess.Popen([sys.executable, "read_networks_find_communities.py"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            self.insert_log(line.decode('utf-8'))
        process.communicate()
        self.enable_buttons()

    def run_script_find_misinformation(self):
        if self.file_path is not None:
            self.open_report_button.grid_remove()
            self.disable_buttons()
            t = threading.Thread(target=self.run_script_find_misinformation_thread)
            t.start()
        else:
            self.insert_log("Data set file is not selected\n")

    def run_script_find_misinformation_thread(self):
        process = subprocess.Popen([sys.executable, "find_misinformation.py", self.file_path], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            self.insert_log(line.decode('utf-8'))
        process.communicate()
        self.enable_buttons()
        self.open_report_button.grid()

    def run_script_calculate_metrics(self):
        self.disable_buttons()
        t = threading.Thread(target=self.run_script_calculate_metrics_thread)
        t.start()

    def run_script_calculate_metrics_thread(self):
        process = subprocess.Popen([sys.executable, "calculate_metrics_for_networks.py"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            self.insert_log(line.decode('utf-8'))
        process.communicate()
        self.enable_buttons()


root = tk.Tk()
root.title("Misinformation Framework")
root.maxsize(1200, 600)
root.config(bg="#272C35")

app = App()
root.mainloop()
