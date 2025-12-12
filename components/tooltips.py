# Copyright © Advanced Micro Devices, Inc., or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
tooltips = {
    # Sidebar > Tile Control
    'tile_size': (
        "Adjust the size of the tile to extract from the image (in pixels). "
        "Typical values are 128, 256, or 512. Larger tiles show more context, but may reduce detail."
    ),

    'x_position': (
        "Specify the X-coordinate (in pixels) for the top-left corner of the tile. "
        "This determines the horizontal offset from the image origin."
    ),

    'y_position': (
        "Specify the Y-coordinate (in pixels) for the top-left corner of the tile. "
        "This determines the vertical offset from the image origin."
    ),

    # Sidebar > Stain Separation
    'stain_option': (
        "Select a stain to separate its contribution from the image. This is useful in histological analysis:\n"
        "- **None**: No stain separation.\n"
        "- **Eosin**: Highlights cytoplasm and extracellular matrix in pink.\n"
        "- **Hematoxylin**: Stains nuclei blue/purple.\n"
        "- **DAB**: Highlights specific antigens using a brown chromogen in immunohistochemistry."
    ),

    # Sidebar > Feature Extraction
    'gabor': (
        "Apply Gabor filter to highlight texture-rich patterns. "
        "Useful for detecting oriented structures like collagen fibers or muscle layers."
    ),

    'sobel': (
        "Apply Sobel filter to detect edges by computing the intensity gradient. "
        "Helps isolate boundaries and structural features."
    ),

    # Sidebar > Morphology
    'dilation': (
        "Perform binary dilation to expand bright (foreground) regions. "
        "Useful for connecting fragmented structures or filling small gaps."
    ),

    'smallobjs': (
        "Remove small, disconnected components from a binary mask. "
        "Effective for eliminating noise or irrelevant regions based on size thresholding."
    ),

    # Sidebar > Geometric Transformations
    'rotate': (
        "Rotate the image counter-clockwise by 45 degrees. "
        "This is a fixed-angle rotation centered on the tile."
    ),

    'warp': (
        "Apply affine transformations (scale, rotate, shear, translate) "
        "to spatially distort the tile. Useful for data augmentation or geometric corrections."
    ),
}
