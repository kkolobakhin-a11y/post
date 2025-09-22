# NULL — Канал 0 (Пустота): Автопостинг

Минималистичная система автопостинга для Telegram-канала проекта NULL.
- 4 поста в день: 2×атмосфера, 1×челлендж, 1×CTA
- Контент из `templates.json` (просто добавляйте новые фразы)
- Ротация по дню года + соль слота → без повторов в ближайшей перспективе
- Полный автозапуск через GitHub Actions (cron + ручной запуск)

## Секреты (GitHub → Settings → Secrets and variables → Actions → New repository secret)
- `BOT_TOKEN` — токен Telegram-бота (bot token)
- `CHANNEL_ID` — ID канала (например, `@your_channel` или числовой ID со знаком `-100...`)
- `BOT_LINK` — ссылка на бота для CTA (например, `https://t.me/your_bot`)

## Структура
```text
.github/workflows/
  atmo_morning.yml
  atmo_evening.yml
  challenge.yml
  cta.yml
main.py
templates.json
README.md
```

## Локальный тест
```bash
pip install requests
export BOT_TOKEN=xxx CHANNEL_ID=@your_channel BOT_LINK=https://t.me/your_bot
python main.py atmo1
python main.py atmo2
python main.py challenge
python main.py cta
```

## Изменить расписание
Правьте `on.schedule.cron` в нужном `.yml` внутри `.github/workflows/`.
Расписание задаётся в UTC.
