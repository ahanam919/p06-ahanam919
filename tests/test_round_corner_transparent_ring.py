from thumbor.ext.filters import _round_corner

WIDTH = 40
HEIGHT = 40
RADIUS = 10
WHITE = (255, 255, 255)


def test_transparent_round_corner_edge_is_not_darkened():
    # Solid white RGBA picture, rounded corners, transparent flag set.
    buf = bytes([255, 255, 255, 255] * WIDTH * HEIGHT)
    out = _round_corner.apply(
        1, "RGBA", RADIUS, RADIUS, 0, 0, 0, WIDTH, HEIGHT, buf, 1
    )

    # A pixel that is still fully opaque must keep the picture's own color.
    # The dark ring bug leaves opaque edge pixels with color scaled toward black.
    offenders = []
    for i in range(0, len(out), 4):
        r, g, b, a = out[i], out[i + 1], out[i + 2], out[i + 3]
        if a == 255 and (r, g, b) != WHITE:
            offenders.append(i // 4)

    assert offenders == []
