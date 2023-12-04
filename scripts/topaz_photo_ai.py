import sys
import os
import subprocess
import tempfile

from PIL import Image

from modules.upscaler import Upscaler, UpscalerData

class UpscalerTopazPhotoAI(Upscaler):
    scalers = []

    def do_upscale(self, img, selected_model=None):
        fp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(fp)
        fp.close()

        try:
            result = subprocess.run(
                ["C:\\Program Files\\Topaz Labs LLC\\Topaz Photo AI\\tpai.exe", "--overwrite", fp.name],
                shell=True,
                check=True,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        except subprocess.CalledProcessError:
            print('Error: ' + result.stderr)
            return img

        upscaled = Image.open(fp.name)
        new_img = upscaled.copy()

        upscaled.close()
        os.remove(fp.name)

        return new_img

    def load_model(self, _):
        pass

    def __init__(self, dirname=None):
        super().__init__(False)
        self.name = "Topaz Photo AI"
        self.scalers = [UpscalerData("Topaz Photo AI", None, self)]
