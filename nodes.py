from .comfy_annotations import ComfyFunc, ImageTensor, NumberInput, Choice
from .utilities.scale_utils import oe_downscale, downscale
from .utilities.quantization_utils import palette_quantization, palette_swap
from .utilities.tensor_utils import tensor2pil, pil2tensor


@ComfyFunc(
    category="Pixel Image Processing",
    display_name="Pixel Image Downscale By",
    is_output_node=True,
)
def scale_by(
    image: ImageTensor,
    downscale_factor: int = NumberInput(8, 1, 4096, 1, "number"),
    scale_method: str = Choice(["k-centroid", "nearest-neighbors"]),
    outline_expansion: bool = False,
) -> ImageTensor:
    """Rescale an image by dividing it's current size by the downscale factor."""

    image = tensor2pil(image)
    new_image: ImageTensor
    match outline_expansion:
        case True:
            new_image = oe_downscale(image, downscale_factor, scale_method)
        case False:
            new_image = downscale(image, downscale_factor, scale_method)

    return pil2tensor(new_image)


@ComfyFunc(
    category="Pixel Image Processing",
    display_name="Pixel Image Reduce Palette",
    is_output_node=True,
)
def palette_reduce_node(
    image: ImageTensor,
    palette_size: int = NumberInput(1, 1, 256, 1, "number"),
    method: str = Choice(
        [
            "Quantize.MEDIANCUT",
            "Quantize.MAXCOVERAGE",
            "Quantize.FASTOCTREE",
            "cv2.kmeans",
        ]
    ),
) -> ImageTensor:
    """Reduce the palette of an image to the specified size."""

    image = tensor2pil(image)
    new_image = palette_quantization(image, palette_size, method, elbow_method=False)
    return pil2tensor(new_image)


@ComfyFunc(
    category="Pixel Image Processing",
    display_name="Pixel Image Palette Swap",
    is_output_node=True,
)
def palette_swap_node(
    image: ImageTensor,
    palette_image: ImageTensor,
) -> ImageTensor:
    """Swap the palette of an image to the specified size."""

    image = tensor2pil(image)
    palette_image = tensor2pil(palette_image)
    new_image = palette_swap(image, palette_image=palette_image)
    return pil2tensor(new_image)
