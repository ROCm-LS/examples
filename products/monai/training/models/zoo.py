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
#
# List of MONAI models from the Model Zoo supported for demo
#

MODEL_ZOO = {
    "Spleen CT Segmentation": {
        "id": "spleen_ct_seg",
        "description": "A 3D segmentation model for spleen delineation in CT images. The model processes 96x96x96 pixel patches and provides segmentation masks for spleen tissue.",
        "url": "https://monai.io/model-zoo.html#/model/spleen_ct_segmentation",
        "dataset": "Medical Segmentation Decathlon (MSD) - Spleen",
        "dataurl": "https://medicaldecathlon.com/dataaws/",
        "params": {
            "learning_rate": {"type": "slider", "min": 1e-5, "max": 3e-3, "step": 1e-5, "default": 1e-4},
            "batch_size": {"type": "slider", "min": 1, "max": 8, "step": 1, "default": 2},
            "epochs": {"type": "slider", "min": 1, "max": 100, "step": 1, "default": 10},
        },
    },

    "Pathology Tumor Detection": {
        "id": "pathology_tumor_detection",
        "description": "A deep learning model for detecting metastatic tissue in whole-slide pathology images. The model processes 224x224 pixel RGB patches and provides probability scores for metastasis detection.  Trained on the Camelyon16 dataset",
        "url": "https://monai.io/model-zoo.html#/model/pathology_tumor_detection",
        "dataset": "CAncer MEtastases in LYmph nOdes challeNge (CAMELYON)",
        "dataurl": "https://registry.opendata.aws/camelyon/",
        "params": {  
            "learning_rate": {"type": "slider", "min": 1e-5, "max": 3e-3, "step": 1e-5, "default": 1e-4},
            "batch_size": {"type": "slider", "min": 1, "max": 100, "step": 1, "default": 32},
            "epochs": {"type": "slider", "min": 1, "max": 100, "step": 1, "default": 2},
            "backend": {"type": "selectbox", "options": ["cucim", "numpy"], "default": "cucim"},
            "grid_shape": {"type": "slider", "min": 1, "max": 8, "step": 1, "default": 3},
            "patch_size": {"type":"slider", "min": 200, "max": 220, "step": 1, "default": 224},
            "prob": {"type":"slider", "min": 0.1, "max": 1.0, "step": .01, "default": 0.5},
            "gpu": {"type": "slider", "min": 0, "max": 7, "step": 1, "default": 0},
        },
    },

    # Add more models here
}
