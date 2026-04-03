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

ARG BASE_IMAGE=rocm/dev-ubuntu-24.04:7.2-complete
FROM ${BASE_IMAGE}

COPY . /rocm-ls-examples

WORKDIR /rocm-ls-examples
RUN ls -l /rocm-ls-examples
RUN ls -l requirements.txt
RUN ls -l supervisord.conf

# Set ROCm environment variables
ENV HIP_PATH=/opt/rocm
ENV PATH=$HIP_PATH/bin:$PATH
ENV ROCM_PATH=/opt/rocm
ENV LD_LIBRARY_PATH=$HIP_PATH/lib:$LD_LIBRARY_PATH
ENV ROCM_HOME=/opt/rocm

# Install system dependencies for hipCIM and MONAI

RUN apt-get update && \
    apt-get install -y software-properties-common lsb-release gnupg && \
    apt-key adv --fetch-keys https://apt.kitware.com/keys/kitware-archive-latest.asc && \
    add-apt-repository -y "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main" && \
    apt-get update && \
    apt-get install -y git wget gcc g++ ninja-build git-lfs \
                       yasm libopenslide-dev python3 python3-venv \
                       python3-dev libpython3-dev \
                       cmake libvips supervisor && \
    if ! dpkg -s amdgpu-install >/dev/null 2>&1; then \
        rm -f /etc/apt/sources.list.d/amdgpu.list /etc/apt/sources.list.d/rocm.list && \
        ROCM_VERSION=$(cat /opt/rocm/.info/version) && \
        UBUNTU_CODENAME=$(lsb_release -cs) && \
        echo "Detected ROCm version: ${ROCM_VERSION}, Ubuntu codename: ${UBUNTU_CODENAME}" && \
        MAJOR=$(echo ${ROCM_VERSION} | cut -d. -f1) && \
        MINOR=$(echo ${ROCM_VERSION} | cut -d. -f2) && \
        PATCH=$(echo ${ROCM_VERSION} | cut -d. -f3) && \
        PATCH=${PATCH:-0} && \
        VERNUM=$((MAJOR * 10000 + MINOR * 100 + PATCH)) && \
        if [ "${PATCH}" = "0" ]; then SHORT_VERSION="${MAJOR}.${MINOR}"; else SHORT_VERSION="${MAJOR}.${MINOR}.${PATCH}"; fi && \
        AMDGPU_URL="https://repo.radeon.com/amdgpu-install/${SHORT_VERSION}/ubuntu/${UBUNTU_CODENAME}/amdgpu-install_${SHORT_VERSION}.${VERNUM}-1_all.deb" && \
        echo "Downloading: ${AMDGPU_URL}" && \
        wget "${AMDGPU_URL}" -O amdgpu-install.deb && \
        apt-get update && \
        DEBIAN_FRONTEND=noninteractive apt-get install -y ./amdgpu-install.deb && \
        rm -f amdgpu-install.deb; \
    else \
        echo "amdgpu-install already present, skipping install"; \
    fi && \
    apt-get update && \
    apt-get install -y --no-install-recommends amdgpu-lib && \
    apt-get install -y --no-install-recommends rocjpeg rocjpeg-dev rocthrust-dev \
                    hipcub hipblas hipblas-dev hipfft hipsparse \
                    hiprand rocsolver rocrand-dev rocm-hip-sdk && \
    rm -rf /var/lib/apt/lists/*


# Set up Python venv
WORKDIR /rocm-ls-examples
RUN python3 -m venv /venv

# Upgrade pip, setuptools, and wheel first
RUN /venv/bin/python -m pip install --upgrade pip setuptools wheel

# Install PyTorch first, then remaining requirements
RUN ROCM_FULL=$(cat /opt/rocm/.info/version | cut -d. -f1,2,3) && \
    ROCM_SHORT=$(echo ${ROCM_FULL} | cut -d. -f1,2) && \
    echo "Installing PyTorch for ROCm ${ROCM_SHORT}" && \
    /venv/bin/pip install torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/rocm${ROCM_SHORT} && \
    echo "Installing remaining requirements for ROCm ${ROCM_FULL}" && \
    /venv/bin/pip install \
        --extra-index-url https://pypi.amd.com/rocm-${ROCM_FULL}/simple/ \
        -r requirements.txt

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set venv in PATH for runtime (after all build steps are complete)
ENV PATH="/venv/bin:$PATH"

# Expose Streamlit port
EXPOSE 8501

# Entrypoint: set CPATH dynamically at runtime
# Using shell form to allow variable expansion
CMD CLANG_VER=$(ls /opt/rocm/lib/llvm/lib/clang 2>/dev/null | sort -V | tail -1) && \
    echo "=========================================" && \
    if [ -n "$CLANG_VER" ]; then \
        export CPATH="/opt/rocm/lib/llvm/lib/clang/${CLANG_VER}/include" && \
        echo "  CLANG_VER: ${CLANG_VER}" && \
        echo "  CPATH: ${CPATH}"; \
    else \
        echo "  WARNING: Could not detect Clang version in /opt/rocm/lib/llvm/lib/clang" && \
        echo "  CPATH not set"; \
    fi && \
    echo "=========================================" && \
    exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
