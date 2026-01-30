# Telegram API (Telethon)

Cursor читає та пише повідомлення в Telegram через офіційний API.

## Що це дає

- ✅ Читати повідомлення з чатів/груп
- ✅ Відправляти повідомлення
- ✅ Керувати групами (створювати, перейменовувати)
- ✅ Шукати контакти

---

## Крок 1: Отримати API credentials

1. Відкрий https://my.telegram.org
2. Залогінься через номер телефону
3. Перейди в **API development tools**
4. Створи новий додаток:
   - App title: `MyCRM` (будь-яка назва)
   - Short name: `mycrm`
   - Platform: `Desktop`
5. Скопіюй **App api_id** і **App api_hash**

---

## Крок 2: Встановити залежності

```bash
pip3 install telethon python-dotenv qrcode
```

---

## Крок 3: Створити .env файл

```bash
# .env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
```

⚠️ Додай `.env` в `.gitignore`!

---

## Крок 4: Авторизація через QR

Створи файл `telegram_login.py`:

```python
from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

client = TelegramClient(
    'telegram_session',
    int(os.getenv('TELEGRAM_API_ID')),
    os.getenv('TELEGRAM_API_HASH')
)

async def main():
    await client.connect()
    
    if not await client.is_user_authorized():
        qr_login = await client.qr_login()
        
        # Показати QR код в терміналі
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(qr_login.url)
        qr.print_ascii(invert=True)
        
        print("\n📱 Скануй QR в Telegram:")
        print("   Settings → Devices → Link Desktop Device")
        
        await qr_login.wait(timeout=120)
    
    me = await client.get_me()
    print(f"\n✅ Залогінено як: {me.first_name} (@{me.username})")
    await client.disconnect()

asyncio.run(main())
```

Запусти:
```bash
python3 telegram_login.py
```

Скануй QR код в Telegram на телефоні. Сесія збережеться в `telegram_session.session`.

---

## Використання в Cursor

Після авторизації можеш просити Cursor:

> "Покажи останні 10 повідомлень з групи [назва]"

> "Відправ повідомлення @username: Привіт!"

> "Знайди всі чати де є слово 'проект'"

---

## Приклади коду

### Прочитати повідомлення

```python
async with client:
    async for message in client.iter_messages('username', limit=10):
        print(f"{message.sender.first_name}: {message.text}")
```

### Відправити повідомлення

```python
async with client:
    await client.send_message('username', 'Привіт!')
```

### Отримати список чатів

```python
async with client:
    async for dialog in client.iter_dialogs():
        print(dialog.name)
```

---

## Rate Limits (важливо!)

| Параметр | Значення |
|----------|----------|
| Повідомлень підряд новим контактам | 10-15 max |
| Затримка між повідомленнями | 5 секунд мінімум |
| Пауза після ліміту | 5-30 хвилин |

```python
import asyncio
from telethon.errors import FloodWaitError

try:
    await client.send_message(user, text)
except FloodWaitError as e:
    print(f"Чекаємо {e.seconds} секунд...")
    await asyncio.sleep(e.seconds)
```

---

## Troubleshooting

### QR код не сканується
- Переконайся що Telegram на телефоні оновлений
- Спробуй збільшити яскравість екрану

### Session expired
- Видали `telegram_session.session`
- Запусти `telegram_login.py` знову

### FloodWaitError
- Зачекай вказану кількість секунд
- Зменш частоту повідомлень
