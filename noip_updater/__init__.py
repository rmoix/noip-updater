"""Actualitzador manual del DNS dinàmic de No-IP."""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"
DEFAULT_HOSTNAME = "vmixcentral.ddns.net"


def load_config():
    if not CONFIG_PATH.exists():
        raise SystemExit(
            f"No existeix {CONFIG_PATH.name}. Crea'l amb: python3 -m noip_updater.config"
        )
    with CONFIG_PATH.open() as f:
        return json.load(f)
