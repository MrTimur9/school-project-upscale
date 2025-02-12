import tkinter as tk
from tkinter import filedialog
from time import sleep
import threading


omg_slovar = {'input_file' : None, 'output_file' : None}


root = tk.Tk()  # Creates the main window (the “root” widget)
root.title("Пон")  # Sets the window title

text_entry = tk.Entry(root, width=40)
text_entry.pack(pady=5)

status_label = tk.Label(root, width=40, text='Status')
status_label.pack(pady=5)

def on_button_click() -> None:
    user_text = text_entry.get()
    print(user_text)
    button.config(text=user_text)

def choose_input_file():
    omg_slovar['input_file'] = filedialog.askopenfilename(
        title="Select Input Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    print(omg_slovar['input_file'])

def choose_output_file():
    omg_slovar['output_file'] = filedialog.asksaveasfilename(
        title="Select Input Image",
        defaultextension=".png",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")],
        initialfile='upscaled_image.png'
    )
    print(omg_slovar['output_file'])

def loading():
    status_label.config(text='Loading fr')
    sleep(10)
    
    status_label.config(text='Done')
    sleep(1)
    status_label.config(text='Status')

def start():

    
    threading.Thread(target=loading).start()

button_start = tk.Button(
    root,
    text='Start Process',
    width=40,
    command=start
)
button_start.pack(pady=5)

button = tk.Button(
    root,
    text='submit',
    width=40,
    command=choose_input_file
)
button.pack(pady=5)

button1 = tk.Button(
    root,
    text='save as file',
    width=40,
    command=choose_output_file
)
button1.pack(pady=5)




root.mainloop()