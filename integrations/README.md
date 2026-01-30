# Інтеграції для Cursor CRM

Підключи месенджери та пошту до Cursor — читай повідомлення, відправляй outreach, керуй CRM голосом з телефону.

## Доступні інтеграції

| Інтеграція | Що дає | Складність |
|------------|--------|------------|
| [Telegram API](telegram_api.md) | Читати/писати повідомлення, керувати групами | ⭐⭐ Середня |
| [Telegram Remote](telegram_remote.md) | Керувати Cursor з телефону | ⭐ Легка |
| [Gmail](gmail.md) | Читати пошту, шукати листи | ⭐⭐ Середня |
| [WhatsApp](whatsapp.md) | Читати чати та групи | ⭐⭐⭐ Складна |

---

## Що потрібно для всіх інтеграцій

1. **Python 3.10+**
2. **Cursor IDE** з налаштованим CRM
3. **API ключі** (створюєш сам, інструкції в кожному файлі)

---

## Швидкий старт

### Хочу читати Telegram
→ [telegram_api.md](telegram_api.md)

### Хочу керувати Cursor з телефону
→ [telegram_remote.md](telegram_remote.md)

### Хочу бачити пошту в CRM
→ [gmail.md](gmail.md)

### Хочу читати WhatsApp
→ [whatsapp.md](whatsapp.md)

---

## Безпека

⚠️ **Ніколи не комітьте API ключі в git!**

Всі ключі зберігай в `.env` файлах. Додай в `.gitignore`:

```
.env
*.session
token.json
credentials.json
```

---

## Структура файлів після налаштування

```
your-project/
├── .env                    ← API ключі (НЕ комітити!)
├── telegram_session.session ← Telegram сесія
├── token.json              ← Gmail токен
└── credentials.json        ← Gmail OAuth credentials
```
