# noip-updater

Petit programa en Python (sense dependències) que envia la IP pública actual a **No-IP** per mantenir actualitzat el host de DNS dinàmic `vmixcentral.ddns.net`. Fa servir l'API oficial de No-IP, així que no cal entrar a la web.

S'executa a mà, sota demanda (per exemple, un cop per setmana).

## Què fa

1. Obté la IP pública consultant diversos serveis (ipify, Amazon, icanhazip). Si un falla, prova el següent.
2. L'envia a `https://dynupdate.no-ip.com/nic/update` amb l'usuari i la contrasenya de `config.json`.
3. Mostra el resultat: `good` (actualitzat), `nochg` (ja tenia aquesta IP) o un error explicat en català.

## Configuració

Les credencials es desen a `config.json`, a l'arrel del projecte:

```json
{
  "username": "usuari-o-correu",
  "password": "...",
  "hostname": "vmixcentral.ddns.net"
}
```

- **No és al repositori** (és al `.gitignore`).
- Es crea amb permisos `600` (només el teu usuari el pot llegir).
- La contrasenya hi és en text pla perquè No-IP la necessita real a cada actualització (un hash no serviria).

Crea-la o canvia-la amb:

```bash
python3 -m noip_updater.config
```

## Ús

Des de la carpeta del projecte (`~/Developer/noip-updater`):

```bash
python3 -m noip_updater            # actualitza la IP
python3 -m noip_updater --dry-run  # només mostra la IP, no envia res
```

### Comanda `noip`

Per executar-lo des de qualsevol lloc, afegeix a `~/.zshrc`:

```bash
noip() {
  local dir="$HOME/Developer/noip-updater"
  if [ "$1" = "config" ]; then
    PYTHONPATH="$dir" python3 -m noip_updater.config
  else
    PYTHONPATH="$dir" python3 -m noip_updater "$@"
  fi
}
```

i recarrega amb `source ~/.zshrc`. Després:

```bash
noip            # actualitza
noip --dry-run  # només mostra la IP
noip config     # desa o canvia les credencials
```

## Notes

- Amb el pla gratuït, No-IP demana confirmar el host cada 30 dies per correu. Aquest programa no ho evita.
- Si No-IP respon `badauth`, `nohost` o `abuse`, revisa `config.json` abans de tornar-ho a provar: insistir pot fer que No-IP bloquegi el compte.

## Estructura

```
noip_updater/
  __init__.py   # ruta de config.json i lectura
  __main__.py   # obté la IP i l'envia a No-IP
  config.py     # crea/actualitza config.json
```
