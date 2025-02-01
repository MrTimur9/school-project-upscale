import torch
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet # model itself
from realesrgan import RealESRGANer # framework that used it

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

input_img = Image.open('img/jackal1.png').convert('RGB')
img = np.array(input_img)

output, _ = upsampler.enhance(img, outscale=4)

output_img = Image.fromarray(output)
output_img.save('output1.png')