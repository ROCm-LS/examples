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
import plotly.graph_objects as go

from components.state import session_state_get

# Display performance graph as a tile
def display_performance_graph():
    tile_display_size_offset = 50 # Arbitrary magic number
    graph_height = (session_state_get('tile_display_size') 
                    - 
                    tile_display_size_offset)

    # Initialize graph display parameters
    labels = ['']
    data_values = []
    colors = ['orange']
    x_title = 'No Transformations Applied!'

    # If there are transformations applied, include them in the graph
    pipeline = session_state_get('pipeline')
    if pipeline:
        n_tr = len(session_state_get('pipeline'))
        if n_tr:
            x_title = f"Performance of {n_tr} transform(s)"

            # Get latest times for the last operation
            latest_gpu = session_state_get('gpu_times')[-1]
            latest_cpu = session_state_get('cpu_times')[-1]
            last_ratio = latest_cpu / latest_gpu
        
            # Create a bar chart
            data_values = [last_ratio]

    # Initialize the performance graph
    fig = go.Figure()

    # Add performance bars
    fig.add_trace(go.Bar(
        x=labels,
        y=data_values,
        name='GPU Speedup',
        orientation='v',
        marker_color=colors
    ))

    # Update layout
    fig.update_layout(
        barmode='group',  # Bars appear side-by-side
        height=graph_height,
        xaxis_title=dict(
            text=x_title,
            font=dict(
                family="Arial, sans-serif",
                size=12,
            )
        ),
        yaxis_title='Speedup (CPU/GPU, x)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    # Render the chart
    st.plotly_chart(fig)

