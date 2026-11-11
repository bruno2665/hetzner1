# Caddy = Reverse Proxy + Webserver fuer die statische Seite
FROM caddy:2-alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY site/ /srv/

# Konfiguration beim Build pruefen (Platzhalter-Domains nur fuer den Test)
RUN DOMAIN=example.com STATUS_DOMAIN=status.example.com \
    caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
