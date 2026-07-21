#!/usr/bin/env bash
# GameCore AI — первичная настройка Ubuntu-сервера (запускать от root один раз).
#
#   curl -fsSL https://raw.githubusercontent.com/vnxkirill/Kir.ROBLOX_bot/main/deploy/server/setup.sh | bash
#
# После окончания скрипт попросит заполнить /opt/gamecore/.env и запустит бота.

set -euo pipefail

REPO_URL="https://github.com/vnxkirill/Kir.ROBLOX_bot.git"
APP_DIR="/opt/gamecore"
APP_USER="gamecore"

echo "=== 1/6. Пакеты ==="
apt-get update -qq
apt-get install -y -qq git curl

echo "=== 2/6. Пользователь ${APP_USER} ==="
id -u "${APP_USER}" &>/dev/null || useradd --system --create-home --shell /bin/bash "${APP_USER}"

echo "=== 3/6. Код из GitHub ==="
if [ -d "${APP_DIR}/.git" ]; then
    git -C "${APP_DIR}" pull --ff-only
else
    git clone "${REPO_URL}" "${APP_DIR}"
fi
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"

echo "=== 4/6. uv + Python 3.13 + зависимости ==="
sudo -u "${APP_USER}" bash -c "
    curl -fsSL https://astral.sh/uv/install.sh | sh
    cd '${APP_DIR}'
    ~/.local/bin/uv sync --frozen
"

echo "=== 5/6. .env ==="
if [ ! -f "${APP_DIR}/.env" ]; then
    cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
    chown "${APP_USER}:${APP_USER}" "${APP_DIR}/.env"
    chmod 600 "${APP_DIR}/.env"
    echo
    echo "!!! Заполни ${APP_DIR}/.env (BOT_TOKEN, BOT_OWNER_ID, OPENROUTER_API_KEY):"
    echo "    nano ${APP_DIR}/.env"
    echo "И запусти этот скрипт ещё раз."
    exit 0
fi

echo "=== 6/6. Миграции + systemd ==="
sudo -u "${APP_USER}" bash -c "cd '${APP_DIR}' && ~/.local/bin/uv run alembic upgrade head"
cp "${APP_DIR}/deploy/server/gamecore.service" /etc/systemd/system/gamecore.service
systemctl daemon-reload
systemctl enable gamecore
systemctl restart gamecore
sleep 3
systemctl --no-pager status gamecore

echo
echo "✅ Готово! Бот работает. Полезные команды:"
echo "   systemctl status gamecore     — статус"
echo "   journalctl -u gamecore -f     — живые логи"
echo "   systemctl restart gamecore    — перезапуск"
