"""A resize whose target ratio is far from the source's must not crop the
image down to zero height or width.

See issue #4: a 16x16 source asked for at 800x20 came back blank because
auto_crop() rounded the crop height to 0 and the engine then resized an
empty image.
"""

from tests.base import TestCase
from tests.fixtures.transformer_test_data import TestData
from thumbor.transformer import Transformer


class AutoCropNonZeroTestCase(TestCase):
    def test_extreme_target_ratio_crop_is_not_empty(self):
        # 16x16 source, 800x20 target: the target ratio is far from the
        # source's, which is what makes the auto crop round down to 0.
        data = TestData(
            source_width=16,
            source_height=16,
            target_width=800,
            target_height=20,
            halign="center",
            valign="middle",
            focal_points=[],
            crop_left=None,
            crop_top=None,
            crop_right=None,
            crop_bottom=None,
        )
        context = data.to_context()

        transformer = Transformer(context)
        transformer._calculate_target_dimensions()
        transformer.adjust_focal_points()
        transformer.auto_crop()

        crops = data.engine.calls["crop"]
        assert crops, "the transformer should have cropped the image"

        crop = crops[-1]
        width = crop["right"] - crop["left"]
        height = crop["bottom"] - crop["top"]

        assert width >= 1, f"crop width is empty: {crop}"
        assert height >= 1, f"crop height is empty: {crop}"
