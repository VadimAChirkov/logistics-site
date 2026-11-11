# План обновления OpenClaw на Pi (с откатом)

> Передано с ноутбука (agent main2) для бота на Pi. Дата: 2026-11-11.
> Цель: обновить OpenClaw `2026.5.27` → `2026.11.2`, НЕ положив Telegram-бота.

## 🛡️ ПРАВИЛО №0: НЕ СЛОМАТЬ VPN + Tailscale (SSH-доступ)

На Pi настроен split-tunnel через AmneziaWG (`awg0`), VPN включён по умолчанию (автозапуск). **Tailscale работает В ОБХОД VPN** — это единственный путь SSH-доступа к Pi.

### Что идёт в обход VPN (напрямую):
- `100.64.0.0/10` — **Tailscale** (CGNAT) ← SSH-доступ, критично
- `192.168.0.0/16` — локальная сеть
- `80.71.150.167/32` — сам endpoint VPS (антипетля)

### Файлы/юниты, которые НЕЛЬЗЯ трогать при обновлении:
- `/etc/amnezia/amneziawg/awg0.conf` (конфиг VPN с AllowedIPs)
- `awg-quick@awg0.service` (VPN, автозапуск enabled)
- `tailscaled.service` (Tailscale, enabled)

### Почему это безопасно:
Обновление Node (`apt install nodejs`) и `openclaw update` затрагивают **только** пакеты nodejs/openclaw — они физически отдельны от VPN-конфига и Tailscale. SSH по Tailscale (`100.98.207.88`) НЕ зависит от VPN и остаётся доступным на любом этапе обновления.

### Единственная точка пересечения:
Рестарт `openclaw-gateway.service` делать **только при поднятом VPN** (иначе Telegram-бот не поднимется из РФ — Telegram блокируется). Сам SSH-доступ по Tailscale при этом сохраняется всегда, независимо от состояния VPN.

---

## ⚠️ КЛЮЧЕВОЙ БЛОКЕР (Pi-бот упустил это в «подготовке»)

Свежий OpenClaw требует **Node ≥ 24.16.0**, а на Pi стоит **Node 22.23.3**.

`openclaw update --yes` без апгрейда Node = после обновления gateway **не запустится**, бот ляжет. Бэкап и `doctor --lint` это НЕ проверяют.

**Порядок обязателен:** сначала Node 22 → 24, потом обновление OpenClaw, потом рестарт.

## Текущее состояние Pi (проверено по SSH)

| Параметр | Значение |
|---|---|
| OS | Debian 13 (trixie), arm64 |
| Node | `22.23.3-1nodesource1` (репозиторий `node_22.x`, NodeSource) |
| OpenClaw | `2026.5.27`, установлен системно `/usr/lib/node_modules/openclaw` (root) |
| Gateway | `systemctl --user openclaw-gateway.service` (user `vadimchi`), порт 18789 |
| ExecStart | `/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789` |
| EnvironmentFile | `~/.openclaw/gateway.systemd.env` (924 б, содержит API-ключи — не терять) |
| sudo | ✅ работает без пароля |
| RAM / диск | 7.9 ГБ / 41 ГБ свободно |
| Отдельный процесс | `telegram_quotes_bot.py` (котировки) — НЕ трогать |
| Бэкап | `~/Backups/2026-11-11T11-18-53.744+03-00-openclaw-backup.tar.gz` (449 МБ, verified) |

## Основной план (апгрейд)

### Шаг 0. Убедиться, что бэкап на месте
```bash
ls -la ~/Backups/2026-11-11T11-18-53.744+03-00-openclaw-backup.tar.gz
```

### Шаг 1. Зафиксировать текущие версии для отката
```bash
node -v                          # ожидаем v22.23.3
dpkg -l | grep nodejs            # 22.23.3-1nodesource1
openclaw --version               # 2026.5.27
```

### Шаг 2. Обновить Node 22 → 24 (NodeSource)
```bash
# заменить репозиторий node_22.x на node_24.x
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get update
sudo apt-get install -y nodejs
node -v    # ожидаем v24.x
```
Проверка совместимости: Debian 13 (trixie) glibc ≥ 2.41 — подходит для Node 24.

### Шаг 3. Обновить OpenClaw
```bash
sudo openclaw update --yes
# или явно через npm (если update не подхватит Node 24):
# sudo npm install -g openclaw@latest
openclaw --version    # ожидаем 2026.11.2
```

### Шаг 4. Перезапустить gateway
```bash
systemctl --user restart openclaw-gateway.service
systemctl --user status openclaw-gateway.service
```
⚠️ После подъёма VPN на Pi — **обязательно** перезапустить `openclaw-gateway.service` (Telegram в РФ заблокирован, бот идёт через VPS 80.71.150.167).

### Шаг 5. Проверить, что бот жив
- `systemctl --user status openclaw-gateway.service` → `active (running)`.
- Написать `@VadimOpenclawPibot` в Telegram, убедиться что отвечает.
- `ss -tlnp | grep 18789` → порт слушается.

## Откат (если что-то пошло не так)

### Откат Node 24 → 22
```bash
# вернуть репозиторий node_22.x
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get update
sudo apt-get install -y nodejs=22.23.3-1nodesource1
node -v    # ожидаем v22.23.3
```

### Откат OpenClaw к 2026.5.27
```bash
sudo npm install -g openclaw@2026.5.27
openclaw --version
systemctl --user restart openclaw-gateway.service
```

### Полный откат из бэкапа (крайний случай)
```bash
systemctl --user stop openclaw-gateway.service
openclaw backup restore ~/Backups/2026-11-11T11-18-53.744+03-00-openclaw-backup.tar.gz
systemctl --user start openclaw-gateway.service
```

## Риски и замечания

1. **Node 22 → 24 — мажорный скачок.** Другие Node-потребители на Pi? Только OpenClaw (python-бот котировок Node не использует). Риск минимален, но проверить `ls /usr/lib/node_modules/` после апгрейда.
2. **Старый OpenClaw на новом Node:** не перезапускать gateway между шагом 2 и 3 (пока не обновлён OpenClaw). Запущенный процесс продолжит работать на старом Node в памяти, пока мы не сделаем рестарт в шаге 4.
3. **`EnvironmentFile` с ключами не трогать** — он в бэкапе, на диске, и update его не заденет.
4. **VPN:** после апгрейда обязательно перезапуск gateway-юнита, иначе Telegram не поднимется.

## Рекомендация по времени

Делать не «на бегу». Полный цикл 20–30 минут с проверкой бота в Telegram. При малейшем сбое — откат Node+OpenClaw или restore из бэкапа.
