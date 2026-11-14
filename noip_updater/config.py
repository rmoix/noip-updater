"""Crea o actualitza config.json amb les credencials de No-IP.

Ús:
    python3 -m noip_updater.config
"""
import getpass
import json
import os

from . import CONFIG_PATH, DEFAULT_HOSTNAME


def ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    return input(f"{prompt}{suffix}: ").strip() or default


def main():
    current = {}
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open() as f:
            current = json.load(f)

    username = ask("Usuari o correu de No-IP", current.get("username", ""))
    hostname = ask("Nom de host", current.get("hostname", DEFAULT_HOSTNAME))

    password = getpass.getpass("Contrasenya (deixa en blanc per mantenir l'actual): ")
    if password:
        if getpass.getpass("Repeteix la contrasenya: ") != password:
            raise SystemExit("Les contrasenyes no coincideixen.")
    else:
        password = current.get("password", "")
    if not username or not password:
        raise SystemExit("Cal usuari i contrasenya.")

    data = {"username": username, "password": password, "hostname": hostname}
    # Fitxer llegible només pel teu usuari (permisos 600)
    fd = os.open(CONFIG_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.chmod(CONFIG_PATH, 0o600)
    print(f"Desat a {CONFIG_PATH}")


if __name__ == "__main__":
    main()
