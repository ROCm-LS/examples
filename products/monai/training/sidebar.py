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
import torch
import plotly.graph_objs as go
import importlib

from components.io import file_upload_widget, render_markdown
from components.tooltips import tooltips
from components.utility import get_image_shape
from components.console_log import append_console_log
from components.diagnostics import error, warning, note, info
from components.state import (
    session_state_get,
    session_state_set,
)

from products.monai.console import TRAIN_CONSOLE_LOG_KEY
from products.monai.training.models.zoo import MODEL_ZOO

# Layout the MONAI sidebar control panel
def monai_training_sidebar():
    render_markdown("markdown/monai_training_sidebar_header.md")
    selected_model = st.selectbox("**Select Model**", list(MODEL_ZOO.keys()))
    model_info = MODEL_ZOO[selected_model]
    model_info['name'] = selected_model

    # Device to be used for training
    # (disable if no GPU detected)
    device_selection_disabled=True
    device_index=2
    if torch.cuda.is_available():
        device_selection_disabled=False
        device_index=0
    else:
        warning(TRAIN_CONSOLE_LOG_KEY,
                "No GPU detected! Device selection disabled")
    selected_device = st.radio(label="**Select device**", 
                               options=['Auto', 'GPU', 'CPU'],
                               index=device_index,
                               horizontal=True,
                               help="Choose device for current workload",
                               disabled=device_selection_disabled,
    )

    # Setup the training device based on user selection
    if selected_device == "Auto":
        # Auto select the training device based on device availability
        selected_device = "GPU" if torch.cuda.is_available() else "CPU"
    if selected_device == "GPU":
        training_device = torch.device("cuda")
    else:
        training_device = torch.device("cpu")
    session_state_set("training_device", training_device)
    session_state_set("training_device_type", selected_device)

    # Hyperparameter tuning (example: learning rate, epochs, batch size)
    st.markdown(
        "<h6 style='font-family: Arial, sans-serif; color: #333;'>Hyperparameters</h6>", 
        unsafe_allow_html=True
    )
    params = {}
    for pname, pdef in model_info["params"].items():
        if pdef["type"] == "slider":
            params[pname] = st.slider(
                pname.replace("_", " ").title(),
                min_value=pdef["min"], 
                max_value=pdef["max"],
                step=pdef["step"], 
                value=pdef["default"], 
                format="%.5f" if "rate" in pname else "%d"
            )
        # You can add more widget types as needed (e.g. selectbox, checkbox, etc.)
        # ...

    # Squirrel away the selected model and hyperparameters
    session_state_set('monai_model', selected_model)
    session_state_set('monai_model_info', model_info)
    for k, v in params.items():
        session_state_set(f"monai_training_{k}", v)

