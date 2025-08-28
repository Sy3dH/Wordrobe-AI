import os
import glob
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer

OUTPUT_DIR = os.path.join("src", "output", "upscale_service")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def upscale_realesrgan(input_path, outscale=4.0, face_enhance=False,
                       tile=0, tile_pad=10, pre_pad=0,
                       fp32=False, gpu_id=None,
                       ext='auto', suffix='out'):
    """
    Upscale images using RealESRGAN_x4plus and save to fixed output directory.
    """
    model_name = 'RealESRGAN_x4plus'
    netscale = 4
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                    num_block=23, num_grow_ch=32, scale=netscale)
    file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']

    # Ensure weights exist
    model_path = os.path.join('weights', model_name + '.pth')
    if not os.path.isfile(model_path):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        for url in file_url:
            model_path = load_file_from_url(url=url,
                                            model_dir=os.path.join(ROOT_DIR, 'weights'),
                                            progress=True, file_name=None)

    # Create upsampler
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        model=model,
        tile=tile,
        tile_pad=tile_pad,
        pre_pad=pre_pad,
        half=not fp32,
        gpu_id=gpu_id
    )

    # Face enhancer
    face_enhancer = None
    if face_enhance:
        from gfpgan import GFPGANer
        face_enhancer = GFPGANer(
            model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
            upscale=outscale,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=upsampler
        )

    # Prepare input
    paths = [input_path] if os.path.isfile(input_path) else sorted(glob.glob(os.path.join(input_path, '*')))
    results = []

    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print(f"Processing {idx}: {imgname}")
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        img_mode = 'RGBA' if (len(img.shape) == 3 and img.shape[2] == 4) else None

        try:
            if face_enhancer:
                _, _, output = face_enhancer.enhance(img, has_aligned=False,
                                                     only_center_face=False, paste_back=True)
            else:
                output, _ = upsampler.enhance(img, outscale=outscale)
        except RuntimeError as error:
            print(f"Error: {error}")
            continue

        # Save image
        extension = 'png' if img_mode == 'RGBA' else (ext if ext != 'auto' else extension[1:])
        save_path = os.path.join(OUTPUT_DIR, f"{imgname}_{suffix}.{extension}" if suffix else f"{imgname}.{extension}")
        cv2.imwrite(save_path, output)
        results.append(save_path)

    return results

if __name__ == "__main__":
    upscale_realesrgan("D:\9D Tech Work\Wardrobe-POC\POC-2\Wordrobe-AI\src\\upscale\sherwani.jpg", outscale=2, face_enhance=True)