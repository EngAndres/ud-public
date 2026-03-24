FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# ── System dependencies ────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget ca-certificates gnupg \
    python3 python3-pip \
    r-base r-base-dev \
    libcurl4-openssl-dev libssl-dev libxml2-dev libfontconfig1-dev \
    build-essential pkg-config cmake \
    && rm -rf /var/lib/apt/lists/*

# ── Python / Jupyter ───────────────────────────────────────────────────────────
RUN pip3 install --no-cache-dir jupyter jupyterlab ipykernel && \
    python3 -m ipykernel install --sys-prefix --display-name "Python 3"

# ── R packages + IRkernel ──────────────────────────────────────────────────────
RUN Rscript -e "\
    install.packages( \
        c('IRkernel', 'jsonlite', 'ggplot2'), \
        repos = 'https://cloud.r-project.org', quiet = TRUE \
    ); \
    IRkernel::installspec(user = FALSE)"

# ── Rust via rustup ────────────────────────────────────────────────────────────
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --no-modify-path --default-toolchain stable

# ── evcxr Rust Jupyter kernel ──────────────────────────────────────────────────
RUN cargo install evcxr_jupyter && evcxr_jupyter --install

# ── Set working directory ──────────────────────────────────────────────────────
WORKDIR /workspaces/data_analysis_programming
