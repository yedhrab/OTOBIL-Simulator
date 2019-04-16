from mss import mss
from PIL import Image


def capture_screenshot(dimension):
    # Capture entire screen
    with mss() as sct:
        monitor = monitor = {"top": dimension[1],
                             "left": dimension[0], "width": dimension[2] - dimension[0], "height": dimension[3] - dimension[1]}
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


img = capture_screenshot((1, 78, 646, 478))
img.show()


def capture_screenshot(dimension):
    # Capture entire screen
    with mss() as sct:
        monitor = monitor = {"top": dimension[1],
                             "left": dimension[0], "width": dimension[2] - dimension[0], "height": dimension[3] - dimension[1]}
        sct_img = sct.grab(monitor)
