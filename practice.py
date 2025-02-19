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

status_label = tk.Label(root, width=40, text='Status')
status_label.pack(pady=5)

def loading_fr(omg_thread : threading.Thread) -> None:
    omg_text = 'Loading'

    while omg_thread.is_alive():
        if omg_text.count('.') < 3:
            omg_text += ' . '
        else:
            omg_text = 'Loading'
        status_label.config(text=omg_text)
        sleep(0.5)
    status_label.config(text='Done')
    sleep(2)
    status_label.config(text='Status')

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

    button_start.config(state=tk.DISABLED)
    button.config(state=tk.DISABLED)
    button1.config(state=tk.DISABLED)

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

    sleep(1.5)

    button_start.config(state=tk.NORMAL)
    button.config(state=tk.NORMAL)
    button1.config(state=tk.NORMAL)

def start():

    
    thread_upscale = threading.Thread(target=upscale_process)
    thread_load = threading.Thread(target=loading_fr, args=(thread_upscale,))
    thread_upscale.start()
    thread_load.start()



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