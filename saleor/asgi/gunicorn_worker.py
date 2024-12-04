import os
from uvicorn.workers import UvicornWorker as BaseUvicornWorker


class UvicornWorker(BaseUvicornWorker):
    # Override default config args, that cannot be passed as gunicorn parameters.
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        "lifespan": "off",
        "ws": "none",
        "root_path": os.environ.get("SALEOR_ROOT_PATH", "/"),
    }
