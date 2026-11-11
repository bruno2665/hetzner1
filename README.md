# hetzner1

Statische Website + Uptime Kuma + Postgres auf einem Hetzner VPS mit Docker Compose.

| Container     | Aufgabe                                          | Öffentlich |
|---------------|--------------------------------------------------|------------|
| `caddy`       | Reverse Proxy **und** Webserver (HTTPS automatisch) | 80 / 443   |
| `uptime-kuma` | Monitoring, erreichbar über `STATUS_DOMAIN`      | nur via Caddy |
| `postgres`    | Datenbank (internes Netz, kein Port nach außen)  | nein       |

## Ablauf

1. Änderungen an `site/` (oder `Caddyfile`) nach `main` pushen
2. GitHub Actions baut das Image `ghcr.io/bruno2665/hetzner1:latest` (amd64 + arm64)
3. Auf dem VPS: `docker compose pull && docker compose up -d`

## Einmalige Einrichtung auf dem VPS

```bash
# Docker installieren
curl -fsSL https://get.docker.com | sh

# Repo holen
git clone https://github.com/bruno2665/hetzner1.git
cd hetzner1

# Konfiguration
cp .env.example .env
nano .env        # GHCR_OWNER, DOMAIN, STATUS_DOMAIN, POSTGRES_PASSWORD setzen

# Nur bei privatem Repo/Paket: bei ghcr.io anmelden
# (Personal Access Token mit Scope "read:packages")
# echo <TOKEN> | docker login ghcr.io -u bruno2665 --password-stdin

# Starten
docker compose pull
docker compose up -d
docker compose logs -f caddy
```

Danach sofort `https://<STATUS_DOMAIN>` öffnen und den Uptime-Kuma-Admin anlegen.

## Aktionen aktualisieren

Die Website (`site/index.html`) wird aus einer CSV-Datei erzeugt:

```bash
# neue CSV nach tools/denner_aktionen.csv kopieren, dann:
python tools/build.py tools/denner_aktionen.csv tools/template.html site/index.html
git add -A && git commit -m "Aktionen aktualisiert" && git push
```

GitHub Actions baut danach das Image neu. Auf dem VPS: `docker compose pull && docker compose up -d`.

## Updates

```bash
cd hetzner1
git pull                 # falls sich docker-compose.yml geändert hat
docker compose pull
docker compose up -d
```

## Firewall

Hetzner Cloud Firewall: eingehend nur 22, 80, 443 (TCP) und 443 (UDP) erlauben.
Docker umgeht `ufw` – deshalb die Hetzner-Firewall nutzen.

## Backup Postgres

```bash
docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup_$(date +%F).sql
```
