# Gmail API

Cursor читає пошту через Gmail API — шукай листи, дивись переписки з клієнтами.

## Що це дає

- ✅ Шукати листи (by sender, subject, date)
- ✅ Читати вміст листів
- ✅ Дивитись календар
- ❌ Відправляти листи (read-only для безпеки)

---

## Крок 1: Створити Google Cloud Project

1. Відкрий https://console.cloud.google.com
2. Створи новий проект (або вибери існуючий)
3. Назви його `CRM Integration` (або як хочеш)

---

## Крок 2: Увімкнути Gmail API

1. В Google Cloud Console → **APIs & Services** → **Library**
2. Знайди **Gmail API** → натисни **Enable**
3. Знайди **Google Calendar API** → натисни **Enable** (опціонально)

---

## Крок 3: Створити OAuth credentials

1. **APIs & Services** → **Credentials**
2. **Create Credentials** → **OAuth client ID**
3. Якщо просить — налаштуй **OAuth consent screen**:
   - User Type: **External**
   - App name: `CRM Integration`
   - User support email: твій email
   - Developer contact: твій email
   - Scopes: додай `gmail.readonly`, `calendar.readonly`
   - Test users: додай свій email
4. Повернись до **Credentials** → **Create Credentials** → **OAuth client ID**
5. Application type: **Desktop app**
6. Назва: `CRM Desktop`
7. **Download JSON** → збережи як `credentials.json`

---

## Крок 4: Встановити залежності

```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

---

## Крок 5: Авторизація

Створи файл `gmail_auth.py`:

```python
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def authenticate():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    print("✅ Авторизація успішна!")
    return creds

if __name__ == '__main__':
    authenticate()
```

Запусти:
```bash
python3 gmail_auth.py
```

Відкриється браузер — залогінься і дай дозволи. Токен збережеться в `token.json`.

---

## Крок 6: Додати в .gitignore

```
credentials.json
token.json
```

⚠️ Ніколи не комітьте ці файли!

---

## Використання в Cursor

Після авторизації можеш просити Cursor:

> "Покажи листи від john@company.com за останній тиждень"

> "Знайди всі листи з темою 'invoice'"

> "Яка остання переписка з клієнтом Blinkfire?"

---

## Приклади коду

### Пошук листів

```python
from googleapiclient.discovery import build

def search_emails(creds, query, max_results=10):
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    
    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()
        
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        print(f"From: {headers.get('From')}")
        print(f"Subject: {headers.get('Subject')}")
        print(f"Date: {headers.get('Date')}")
        print("---")

# Використання
creds = authenticate()
search_emails(creds, "from:client@example.com")
```

### Отримати події календаря

```python
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def get_calendar_events(creds, days=7):
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
    
    events = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    for event in events.get('items', []):
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start}: {event['summary']}")
```

---

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Переконайся що додав свій email в Test users
- OAuth consent screen має бути налаштований

### Token expired
- Видали `token.json`
- Запусти `gmail_auth.py` знову

### "Insufficient Permission"
- Перевір що додав правильні scopes
- Видали `token.json` і авторизуйся знову
