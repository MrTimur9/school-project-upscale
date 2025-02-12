import tkinter as tk
from tkinter import filedialog
from time import sleep
import threading
import torch
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet # model itself
from realesrgan import RealESRGANer # framework that used it


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

def upscale_process():
    status_label.config(text='Loading fr')

    model_path = 'RealESRGAN_x4plus.pth'

    state_dict = torch.load(model_path, map_location=torch.device('cpu'))['params_ema']

    model = RRDBNet(
        num_in_ch=3, 
        num_out_ch=3, 
        num_feat=64, 
        num_block=23, 
        num_grow_ch=32, 
        scale=4
        )
    model.load_state_dict(state_dict, strict=True)

    upsampler = RealESRGANer(
        scale=4,
        model_path=model_path,
        model=model,
        tile=0,
        pre_pad=0,
        half=False
    )

    
    picture_path = omg_slovar['input_file']


    input_img = Image.open(picture_path).convert('RGB')

    img = np.array(input_img)

    output, _ = upsampler.enhance(img, outscale=4)

    output_img = Image.fromarray(output)
    output_img.save(omg_slovar['output_file'])

    status_label.config(text='Done')

def start():

    
    threading.Thread(target=upscale_process).start()

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