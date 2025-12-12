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
from PIL import Image

from components.utility import (
    get_cpu_info,
    get_gpu_info,
    get_package_version
)
from components.tooltips import tooltips
from components.io import render_markdown
from components.styles import POWERED_BY_HTML, POWERED_BY_CSS
from components.console_log import console_log_init, console_log_view

from products.hipcim.sidebar import hipcim_sidebar
from products.hipcim.main import hipcim_main

CONSOLE_LOG_KEY="hipCIM_CONSOLE_LOG"

def hipcim_layout():
    # Initialize the console log
    console_log_init(CONSOLE_LOG_KEY)
    
    # Design the hipCIM top-level layout
    hipcim_lsb_col, hipcim_main_col, hipcim_rsb_col = st.columns([1, 6, 1.5])

    # --- Sidebar Controls ---
    with hipcim_lsb_col:
        selected_wsi_filename, selected_wsi_filepath, tile_size, x, y = hipcim_sidebar()

    # --- Main Panel ---
    with hipcim_main_col:
        hipcim_main()

    # --- Right Sidebar with Footer Info ---
    with hipcim_rsb_col:
        render_markdown("markdown/hipcim_intro.md")

        # Footer
        console_log_view(CONSOLE_LOG_KEY)  # Displays the current session_state['console_log']
        cpu_details = get_cpu_info()
        gpu_details = get_gpu_info()
        hipcim_details = get_package_version("amd-hipcim")
        st.markdown(POWERED_BY_CSS, unsafe_allow_html=True)
        st.markdown(
            POWERED_BY_HTML.format(
                cpu=cpu_details,
                gpu=gpu_details,
                hipcim=hipcim_details
            ),
            unsafe_allow_html=True
        )

