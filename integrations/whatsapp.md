# WhatsApp (Baileys)

Cursor читає WhatsApp чати через Baileys — неофіційну бібліотеку WhatsApp Web.

## Що це дає

- ✅ Читати повідомлення з чатів
- ✅ Читати групові чати
- ✅ Бачити список контактів
- ⚠️ Відправляти повідомлення (обережно з лімітами!)

---

## ⚠️ Важливо перед початком

1. **Baileys — неофіційна бібліотека**. WhatsApp може заблокувати акаунт при підозрілій активності
2. **Не спамте!** Використовуйте тільки для читання або рідких повідомлень
3. **Тримайте телефон онлайн** — WhatsApp Web потребує підключення до телефону

---

## Крок 1: Встановити Node.js

```bash
# macOS
brew install node

# Перевірити
node --version  # має бути 18+
npm --version
```

---

## Крок 2: Створити проект

```bash
mkdir whatsapp-integration
cd whatsapp-integration
npm init -y
npm install @whiskeysockets/baileys qrcode-terminal
```

---

## Крок 3: Створити скрипт авторизації

Створи файл `whatsapp_login.js`:

```javascript
const { default: makeWASocket, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');

async function main() {
    const { state, saveCreds } = await useMultiFileAuthState('./whatsapp_session');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });
    
    sock.ev.on('creds.update', saveCreds);
    
    sock.ev.on('connection.update', async (update) => {
        const { connection, qr } = update;
        
        if (qr) {
            console.log('\n📱 Скануй QR код в WhatsApp:');
            console.log('   WhatsApp → ⋮ → Linked Devices → Link a Device\n');
            qrcode.generate(qr, { small: true });
        }
        
        if (connection === 'open') {
            console.log('\n✅ Підключено до WhatsApp!');
            
            // Показати останні чати
            const chats = await sock.groupFetchAllParticipating();
            console.log(`\nГрупи: ${Object.keys(chats).length}`);
            
            for (const [jid, chat] of Object.entries(chats).slice(0, 5)) {
                console.log(`  • ${chat.subject}`);
            }
            
            console.log('\nСесія збережена в ./whatsapp_session');
            console.log('Можеш закрити скрипт (Ctrl+C)');
        }
        
        if (connection === 'close') {
            console.log('❌ Відключено');
        }
    });
}

main();
```

Запусти:
```bash
node whatsapp_login.js
```

Скануй QR код у WhatsApp на телефоні.

---

## Крок 4: Додати в .gitignore

```
whatsapp_session/
node_modules/
```

---

## Використання в Cursor

Після авторизації можеш просити Cursor:

> "Покажи останні повідомлення з групи [назва]"

> "Знайди чат з [ім'я контакту]"

> "Скільки непрочитаних повідомлень?"

---

## Приклади коду

### Отримати список чатів

```javascript
const chats = await sock.groupFetchAllParticipating();

for (const [jid, chat] of Object.entries(chats)) {
    console.log(`${chat.subject} (${jid})`);
}
```

### Прочитати повідомлення

```javascript
sock.ev.on('messages.upsert', async (m) => {
    const msg = m.messages[0];
    if (!msg.key.fromMe) {
        console.log(`Від: ${msg.pushName}`);
        console.log(`Текст: ${msg.message?.conversation}`);
    }
});
```

### Відправити повідомлення (обережно!)

```javascript
// Тільки для існуючих контактів!
await sock.sendMessage('380XXXXXXXXX@s.whatsapp.net', { 
    text: 'Привіт!' 
});
```

---

## Rate Limits та безпека

| Що | Рекомендація |
|----|--------------|
| Нові контакти | НЕ писати першим |
| Повідомлень на день | < 50 |
| Затримка між повідомленнями | 10+ секунд |
| Масові розсилки | ❌ Заборонено |

**Порушення лімітів = бан акаунту!**

---

## Troubleshooting

### QR код не сканується
- Переконайся що WhatsApp на телефоні оновлений
- Спробуй видалити `whatsapp_session/` і почати знову

### "Connection closed"
- Перевір інтернет на телефоні
- WhatsApp на телефоні має бути активний

### "Logged out"
- Сесія закінчилась
- Видали `whatsapp_session/` і авторизуйся знову

### Повідомлення не відправляються
- Перевір формат номера: `380XXXXXXXXX@s.whatsapp.net`
- Контакт має бути в телефонній книзі

---

## Альтернатива: WhatsApp Business API

Для серйозного бізнес-використання краще офіційний API:
- https://business.whatsapp.com/products/business-platform

Переваги:
- Офіційний, без ризику бану
- Більші ліміти
- Templates для розсилок

Мінуси:
- Платний
- Потрібна верифікація бізнесу
