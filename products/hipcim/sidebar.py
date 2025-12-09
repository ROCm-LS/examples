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
import streamlit as st
from streamlit_option_menu import option_menu  # for icon support

from components.diagnostics import error, exception, warning, note, info
from components.io import file_upload_widget, render_markdown
from components.tooltips import tooltips
from components.utility import get_image_shape
from components.state import (
    session_state_get,
    session_state_set,
)

from products.hipcim.console import CONSOLE_LOG_KEY
from products.hipcim.styles import COMPACT_SIDEBAR_CSS

from cucim import CuImage

# Icon map for transformations
ICON_MAP = {
    "stain_separation": "🧪",
    "gabor_filter": "🔀",
    "sobel_edges": "🪓",
    "binary_dilation": "✴️",
    "remove_small_objects": "🧹",
    "rotate": "🔄",
    "warp_affine": "🎯",
}

OP_CATALOG = {
    "stain_separation": {"stain": ["hematoxylin", "eosin", "dab"]},
    "gabor_filter": {"frequency": (0.1, 0.9), "theta": (0, 180)},
    "sobel_edges": {},
    "binary_dilation": {"iterations": (1, 10)},
    "remove_small_objects": {"min_size": (10, 1000)},
    "rotate": {"angle": (0, 360)},
    "warp_affine": {},
}

# Initialize hipCIM transformation pipeline
if 'pipeline' not in st.session_state:
    st.session_state['pipeline'] = []

# Layout the hipCIM sidebar control panel
def hipcim_sidebar():
    render_markdown("markdown/hipcim_sidebar_header.md")
    selected_wsi_filename, selected_wsi_filepath = file_upload_widget()

    # Current tile size and positioning
    tile_max_dimension = session_state_get('tile_max_dimension')
    tile_size = session_state_get('tile_size')
    x = session_state_get('position_x')
    y = session_state_get('position_y')

    # Sliders in a compact expander
    st.markdown(COMPACT_SIDEBAR_CSS, unsafe_allow_html=True)
    with st.expander("**Tile Controls**", expanded=True):
        if not selected_wsi_filepath:
            error(CONSOLE_LOG_KEY,
                  "failed to retrieve wsi filepath (missing sample_images/?)")
        else:
            img_width, img_height = get_image_shape(selected_wsi_filepath)
            tile_size_initial = int(min(128, img_width // 2, img_height // 2))
            tile_size = st.slider(
                "Tile Size", 
                int(min(128, img_width/2, img_height/2)), 
                min(tile_max_dimension, img_width - 1, img_height - 1),
                tile_size_initial,
                help=tooltips['tile_size']
            )

            # Dynamically set initial X/Y centered on image 
            # based on uploaded image size and tile size
            x_initial = max(img_width // 2 - tile_size, 0)
            x_max = max(img_width - tile_size, 0)
            x = st.slider(
                "X position", 
                0, x_max, x_initial, step=32,
                help=tooltips['x_position']
            )
            y_initial = max(img_height // 2 - tile_size, 0)
            y_max = max(img_height - tile_size, 0)
            y = st.slider(
                "Y position", 
                0, y_max, y_initial, step=32,
                help=tooltips['y_position']
            )

            # Update session state with loaded image details
            session_state_set('selected_wsi', selected_wsi_filepath)
            session_state_set('wsi_width', img_width)
            session_state_set('wsi_height', img_height)
            session_state_set('tile_size', tile_size)
            session_state_set('position_x', x)
            session_state_set('position_y', y)

            # Squirrel off the CuImage into the session state
            try:
                cuImage = CuImage(session_state_get('selected_wsi'))
                session_state_set('cuImage', cuImage)
            except Exception as e:
                session_state_set('cuImage', None)
                exception(CONSOLE_LOG_KEY,
                          f"failed to load {session_state_get('selected_wsi')} using hipCIM: {e}")

    st.caption(f"Tile size: {tile_size}  |  X: {x}  |  Y: {y}")

    # Pipeline builder UI
    with st.expander("**Transformation Pipeline**", expanded=True):
        with st.expander("Add Transformation Step"):
            op_names = [f"{ICON_MAP[op]} {op.replace('_', ' ').title()}" for op in OP_CATALOG.keys()]
            selected_idx = st.selectbox("Choose operation", list(range(len(OP_CATALOG))), format_func=lambda i: op_names[i])
            op_key = list(OP_CATALOG.keys())[selected_idx]
            param_defs = OP_CATALOG[op_key]
            params = {}

            # For demonstration, allow simple numeric params
            for pname, pdef in param_defs.items():
                if isinstance(pdef, tuple):  # range slider
                    params[pname] = st.slider(
                        pname.title(), float(pdef[0]), float(pdef[1]),
                        float(pdef[0]), key=f"param_{op_key}_{pname}")
                elif isinstance(pdef, list):
                    params[pname] = st.selectbox(
                        pname.title(), pdef, key=f"param_{op_key}_{pname}")
            if st.button(f"➕ Add '{op_key.replace('_', ' ').title()}' to Pipeline"):
                step = {"op": op_key, "params": params.copy()}
                st.session_state['pipeline'].append(step)

        # Render active pipeline
        st.markdown("###### Current Pipeline")
        if not st.session_state['pipeline']:
            st.info("No steps added yet. Use the palette above ⬆️ to build your workflow.")
        else:
            for i, step in enumerate(st.session_state['pipeline']):
                op_key = step['op']
                with st.expander(f"{ICON_MAP[op_key]} {op_key.replace('_', ' ').title()}"):
                    st.write("Parameters:", step['params'] if step['params'] else "None")
                    cols = st.columns([1, 1, 1])
                    with cols[0]:
                        if st.button("🗑️", key=f"remove_{i}", help="Remove"):
                            st.session_state['pipeline'].pop(i)
                    with cols[1]:
                        if i > 0 and st.button("⬆️", key=f"up_{i}", help="Move Up"):
                            st.session_state['pipeline'][i-1], st.session_state['pipeline'][i] = (
                                st.session_state['pipeline'][i], st.session_state['pipeline'][i-1]
                            )
                    with cols[2]:
                        if i < len(st.session_state['pipeline'])-1 and st.button("⬇️", key=f"down_{i}", help="Move Down"):
                            st.session_state['pipeline'][i+1], st.session_state['pipeline'][i] = (
                                st.session_state['pipeline'][i], st.session_state['pipeline'][i+1]
                            )
                    st.caption("Remove, move up/down, reorder as needed. Add/configure more steps in the builder above.")

    return selected_wsi_filename, selected_wsi_filepath, tile_size, x, y
