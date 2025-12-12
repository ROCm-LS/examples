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
# Style strings for various downstream components
#
# Usage example:
#   from components.styles import CONSOLE_LOG_CSS, IMAGE_PLACEHOLDER_CSS
#   import streamlit as st
#   
#   st.markdown(CONSOLE_LOG_CSS, unsafe_allow_html=True)
#   # ... your console log code
#   
#   st.markdown(IMAGE_PLACEHOLDER_CSS, unsafe_allow_html=True)
#   # ... your image placeholder code
#

# Live best metric
BEST_METRIC_HTML = """
<p align="center">
    <strong>Best {metric_name}</strong>
</p>
<font size="4" color="red" face="Monospace">
    <p align="center">
        {metric_value}
    </p>
</font>
"""

# Training device identification
TRAINING_DEVICE_ID_HTML = """
<strong>Training on Device:
<font size="4" color="red" face="Monospace">
{device_type} [torch.device("{device}")]
</font>
</p>
</strong> 
"""

# Inference device identification
INFERENCE_DEVICE_ID_HTML = """
<strong>Inference on Device:
<font size="4" color="red" face="Monospace">
{device_type}
</font>
</p>
</strong> 
"""

# Missing image marker
TRAINING_SAMPLE_MISSING_HTML = """
<div style="
    background:#eee;
    height:80px;
    border-radius:6px;
    color:#aaa;
    display:flex;
    align-items:center;
    justify-content:center;
">
No Image
</div>
"""

# Random samples header
TRAINING_RANDOM_SAMPLE_HEADER_HTML = """
<div style="
    margin: 0px 0;
    padding: 0px 0;
    font-size: 10px;
    font-weight: bold;
    text-align: left;
    border-bottom: 0px solid #bbb;
">
    {group_name}
"""

# Training stats header
TRAINING_STATS_HEADER_HTML = """
<div style="
    margin: 0px 0;
    padding: 0px 0;
    font-size: 10px;
    font-weight: bold;
    text-align: left;
    border-bottom: 1px solid #bbb;
">
{group_name}
"""

# MONAI right sidebar footer
POWERED_BY_CSS = """
<style>
.powered-by-footer {
    color: #555;
    font-size: 14px;
    line-height: 1.2;
}
</style>
"""
POWERED_BY_HTML = """
<div class="powered-by-footer">
  <strong><u>Powered By</u></strong>
  <br>
  <small>
    <strong>CPU:</strong> {cpu}<br>
    <strong>GPU:</strong> {gpu}<br>
    <strong>CuPy:</strong> {cupy}<br>
    <strong>hipCIM:</strong> {hipcim}<br>
    <strong>MONAI:</strong> {monai}
  </small>
</div>
"""

# MONAI metadata tab
TRAINING_METADATA_TAB_CSS = """
<style>
.metadata-tab {
    color: #555;
    font-size: 12px;
    font-family: 'Fira Mono', 'Consolas', Monospace;
    line-height: 1.5;
}
</style>
"""
TRAINING_METADATA_TAB_HTML = """
<div class="metadata-tab">
    <strong>Model:</strong> <a href={url}>{model_name}</a><br>
    <strong>Description:</strong> {description}<br>
    <strong>Dataset:</strong> <a href={dataurl}>{dataset}</a><br>
    <br>
</div>
"""
