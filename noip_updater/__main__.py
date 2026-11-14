"""Envia la IP pública actual a No-IP.

Ús:
    python3 -m noip_updater            actualitza
    python3 -m noip_updater --dry-run  només mostra la IP, no envia res
"""
import base64
import ipaddress
import sys
import urllib.parse
import urllib.request

from . import load_config

IP_SERVICES = [
    "https://api.ipify.org",
    "https://checkip.amazonaws.com",
    "https://icanhazip.com",
]
UPDATE_URL = "https://dynupdate.no-ip.com/nic/update"
USER_AGENT = "noip-updater-mac/1.0"

MESSAGES = {
    "nohost": "El nom de host no existeix en aquest compte.",
    "badauth": "Usuari o contrasenya incorrectes.",
    "badagent": "No-IP ha rebutjat el client.",
    "!donator": "Opció no disponible per a aquest compte.",
    "abuse": "El host està bloquejat per abús.",
    "911": "No-IP té problemes. Torna-ho a provar d'aquí a 30 minuts.",
}


def get_public_ip():
    for url in IP_SERVICES:
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                ip = ipaddress.IPv4Address(r.read().decode().strip())
                return str(ip)
        except Exception:
            continue
    raise SystemExit("No s'ha pogut obtenir la IP pública.")


def update(cfg, ip):
    query = urllib.parse.urlencode({"hostname": cfg["hostname"], "myip": ip})
    token = base64.b64encode(f"{cfg['username']}:{cfg['password']}".encode()).decode()
    req = urllib.request.Request(
        f"{UPDATE_URL}?{query}",
        headers={"Authorization": f"Basic {token}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode().strip()
    except urllib.error.HTTPError as e:
        return e.read().decode().strip() or f"HTTP {e.code}"


def main():
    dry_run = "--dry-run" in sys.argv[1:]
    cfg = load_config()
    ip = get_public_ip()
    print(f"IP pública: {ip}")

    if dry_run:
        print(f"(dry-run) S'enviaria {cfg['hostname']} -> {ip}")
        return

    resp = update(cfg, ip)
    code = resp.split()[0] if resp else ""
    if code in ("good", "nochg"):
        estat = "actualitzat" if code == "good" else "ja tenia aquesta IP"
        print(f"OK: {cfg['hostname']} {estat} ({resp})")
    else:
        print(f"ERROR: {MESSAGES.get(code, 'Resposta inesperada.')} ({resp})")
        sys.exit(1)


if __name__ == "__main__":
    main()
