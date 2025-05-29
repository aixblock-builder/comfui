import subprocess
from pathlib import Path
from loguru import logger
import os

current_file_path = Path(__file__).resolve()
current_dir = current_file_path.parent
logger.info(f"Đường dẫn file đang chạy: {current_file_path}")
logger.info(f"Thư mục chứa file: {current_dir}")
original_cwd = Path.cwd()
os.chdir(current_dir)

def install_cloudflared():
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    filename = "cloudflared-linux-amd64.deb"

    # Tải file .deb
    logger.info("-= Downloading cloudflared =-")
    subprocess.run(["wget", url], check=True)

    # Cài đặt gói .deb
    logger.info("-= Installing cloudflared =-")
    subprocess.run(["dpkg", "-i", filename], check=True)

    logger.info("✅ cloudflared has been installed.")

def install_comfyui():
    pip_path = os.path.join(current_dir, "venv/bin/pip")
    python_path = os.path.join(current_dir, "venv/bin/python") 
    workspace = os.path.join(current_dir, "ComfyUI")
    WORKSPACE = Path(workspace)
    logger.info(WORKSPACE)
    REPO_URL = 'https://github.com/comfyanonymous/ComfyUI'

    # Clone repo nếu chưa tồn tại
    if not WORKSPACE.exists():
        logger.info("-= Initial setup ComfyUI =-")
        subprocess.run(["git", "clone", REPO_URL])

    # Chuyển thư mục làm việc
    os.chdir(WORKSPACE)

    # Cài dependencies chính
    logger.info("-= Install dependencies =-")
    subprocess.run([
        pip_path, "install", "-r", "requirements.txt",
        "--extra-index-url", "https://download.pytorch.org/whl/cu121"
    ])

    # Cài đặt aria2
    subprocess.run(["apt", "-y", "install", "-qq", "aria2"])
    os.chdir(original_cwd)

    # Cài đặt các custom nodes
    CUSTOM_NODES_DIR = WORKSPACE / "custom_nodes"
    os.chdir(CUSTOM_NODES_DIR)

    custom_repos = [
        ("https://github.com/ltdrdata/ComfyUI-Manager", True),
        ("https://github.com/melMass/comfy_mtb", True),
        ("https://github.com/bmad4ever/comfyui_bmad_nodes", True),
        ("https://github.com/Fannovel16/comfyui_controlnet_aux", True),
        ("https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet", False),
        ("https://github.com/cubiq/ComfyUI_essentials", True),
        ("https://github.com/cubiq/ComfyUI_FaceAnalysis", True),
        ("https://github.com/pythongosssss/ComfyUI-Custom-Scripts", False),
        ("https://github.com/kijai/ComfyUI-Florence2", True),
        ("https://github.com/ltdrdata/ComfyUI-Impact-Pack", True),
        ("https://github.com/kijai/ComfyUI-KJNodes", True),
        ("https://github.com/theUpsider/ComfyUI-Logic", False),
        ("https://github.com/kijai/ComfyUI-segment-anything-2", True),
        ("https://github.com/kijai/ComfyUI-SUPIR", True),
        ("https://github.com/un-seen/comfyui-tensorops", True),
        ("https://github.com/KoreTeknology/ComfyUI-Universal-Styler", False),
        ("https://github.com/Fannovel16/ComfyUI-Video-Matting", True),
        ("https://github.com/jags111/efficiency-nodes-comfyui", True),
        ("https://github.com/mav-rik/facerestore_cf", True),
        ("https://github.com/rgthree/rgthree-comfy", True),
        ("https://github.com/TRI3D-LC/tri3d-comfyui-nodes", True),
        ("https://github.com/WASasquatch/was-node-suite-comfyui", True),
        ("https://github.com/crystian/ComfyUI-Crystools", True),
        ("https://github.com/BlenderNeko/ComfyUI_ADV_CLIP_emb.git", False),
    ]

    for repo_url, has_requirements in custom_repos:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        if not (CUSTOM_NODES_DIR / repo_name).exists():
            subprocess.run(["git", "clone", repo_url])
            if has_requirements:
                req_path = CUSTOM_NODES_DIR / repo_name / "requirements.txt"
                if req_path.exists():
                    subprocess.run([pip_path, "install", "-r", str(req_path)])

    # Chạy script cài đặt riêng cho Impact-Pack
    impact_pack_script = CUSTOM_NODES_DIR / "ComfyUI-Impact-Pack" / "install.py"
    if impact_pack_script.exists():
        subprocess.run([python_path, str(impact_pack_script)])

    # Cài đặt thêm ultralytics
    subprocess.run([pip_path, "install", "ultralytics"])

    install_cloudflared()

install_comfyui()
os.chdir(original_cwd)
logger.info(f"-= Done. Returned to original directory: {original_cwd} =-")