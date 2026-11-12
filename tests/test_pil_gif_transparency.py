from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def make_transparent_palette_gif():
    # 20x20 palette GIF. Palette index 0 is transparent (the corner),
    # index 1 is a solid blue square in the middle.
    img = Image.new("P", (20, 20), 0)
    palette = [0, 0, 0, 0, 0, 255] + [0, 0, 0] * 254
    img.putpalette(palette)
    for x in range(5, 15):
        for y in range(5, 15):
            img.putpixel((x, y), 1)
    buf = BytesIO()
    img.save(buf, "GIF", transparency=0)
    return buf.getvalue()


def test_resized_gif_keeps_transparent_background():
    config = Config(PILLOW_PRESERVE_INDEXED_MODE=True)
    context = Context(config=config)
    engine = Engine(context)
    engine.load(make_transparent_palette_gif(), ".gif")

    engine.resize(40, 40)
    result = engine.read(".gif")

    out = Image.open(BytesIO(result)).convert("RGBA")
    # The corner was transparent in the source and must stay transparent.
    assert out.getpixel((0, 0))[3] == 0
