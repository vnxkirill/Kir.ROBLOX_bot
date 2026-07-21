# Деплой GameCore AI на сервер

Бот работает 24/7 на VPS — твой компьютер не нужен.

## Шаг 1. Арендуй VPS (~5 минут, ~300–400 ₽/мес)

Подойдёт любой хостинг с Ubuntu 24.04. Например:

- [Timeweb Cloud](https://timeweb.cloud) — от 200 ₽/мес
- [Beget VPS](https://beget.com/ru/vps) — от 350 ₽/мес
- [Hetzner](https://www.hetzner.com/cloud) — €4.5/мес (нужна зарубежная карта)

Конфигурация: минимальная (1 CPU, 1–2 GB RAM, Ubuntu 24.04).
После оплаты хостинг покажет: **IP-адрес**, логин **root** и **пароль**.

## Шаг 2. Подключись и запусти установку

В PowerShell на своём компе:

```powershell
ssh root@IP_АДРЕС      # введи пароль из письма хостинга
```

На сервере одной командой:

```bash
curl -fsSL https://raw.githubusercontent.com/vnxkirill/Kir.ROBLOX_bot/main/deploy/server/setup.sh | bash
```

Скрипт сам поставит всё нужное и попросит заполнить `.env`:

```bash
nano /opt/gamecore/.env    # впиши BOT_TOKEN, BOT_OWNER_ID, OPENROUTER_API_KEY
```

И запусти скрипт ещё раз — бот заработает:

```bash
curl -fsSL https://raw.githubusercontent.com/vnxkirill/Kir.ROBLOX_bot/main/deploy/server/setup.sh | bash
```

## Шаг 3. Автодеплой из GitHub (опционально, но удобно)

Чтобы каждый пуш в `main` сам обновлял сервер:

1. Сгенерируй ключ на своём компе: `ssh-keygen -t ed25519 -f gamecore_deploy`
2. Добавь публичный ключ на сервер: содержимое `gamecore_deploy.pub` → в `/root/.ssh/authorized_keys`
3. В GitHub: Settings → Secrets and variables → Actions → New repository secret:
   - `SSH_HOST` — IP сервера
   - `SSH_USER` — `root`
   - `SSH_KEY` — содержимое файла `gamecore_deploy` (приватный ключ)

Готово: push → CI → деплой → бот перезапущен.

## Управление ботом на сервере

```bash
systemctl status gamecore     # статус
journalctl -u gamecore -f     # живые логи
systemctl restart gamecore    # перезапуск
```
