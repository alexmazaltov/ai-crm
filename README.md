# AI CRM

**AI-native CRM that runs in your IDE.** No SaaS, no dashboards — just talk to your sales data.

![AI CRM Demo](https://img.shields.io/badge/Alef%20Invest%20™-CRM-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

---

## Why AI CRM?

Traditional CRMs are built for managers who want dashboards. **AI CRM is built for founders who want to close deals.**

| Traditional CRM | AI CRM |
|-----------------|------------|
| Click through 10 screens to log a call | Say "log call with John, he's interested" |
| Export to CSV to analyze | Ask "which hooks work best for Series A?" |
| Pay $50-500/month | Free, runs locally |
| Data locked in vendor | Your data, your files |
| Learn complex UI | Just talk to AI |

---

## What You Get

### 🗂️ Simple CSV-Based CRM
- **Companies** — track leads, status, signals
- **People** — contacts, roles, personalization hooks
- **Activities** — every touchpoint logged
- **Learnings** — what messages work, what doesn't

### 🤖 AI-Native Workflow
```
You: "Show hot leads that haven't been contacted"
Cursor: [shows filtered list from CRM]

You: "Draft a message for John based on his recent LinkedIn post"
Cursor: [researches, writes personalized outreach]

You: "Log that I sent it and set follow-up for next week"
Cursor: [updates CRM, sets reminder]
```

### 📱 Integrations
- **Telegram** — read/send messages via API
- **Gmail** — search emails, see client history  
- **WhatsApp** — read chats and groups
- **Remote Control** — run Cursor from your phone

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/alexmazaltov/ai-crm.git
cd ai-crm
```

### 2. Open in Cursor

```bash
cursor .
```

### 3. Configure for your business

Edit `.cursorrules` — replace placeholders:

```
Company: [YOUR_COMPANY_NAME]
Product: [YOUR_PRODUCT_DESCRIPTION]  
Target: [YOUR_ICP]
```

### 4. Start using

Ask Cursor:
- "Add company Acme Inc to CRM, they just raised Series A"
- "Find the CEO on LinkedIn and add as contact"
- "Show me all hot leads"

---

## Project Structure

```
ai-crm/
├── .cursorrules              ← AI rules (schema, skills, validation)
├── sales/
│   ├── crm/
│   │   ├── crm_companies_master.csv    ← All companies
│   │   ├── crm_people_master.csv       ← All contacts
│   │   ├── crm_outreach_activities.csv ← Activity log
│   │   └── crm_sources.csv             ← Source tracking
│   ├── leads/
│   │   ├── leads_companies_raw.csv     ← Raw intake
│   │   └── leads_people_raw.csv        ← Raw intake
│   ├── learnings/
│   │   └── learnings.csv               ← What works
│   └── outreach/
│       └── OUTREACH_PROMPT.md          ← Message templates
├── integrations/                        ← Setup guides
│   ├── telegram_api.md
│   ├── telegram_remote.md
│   ├── gmail.md
│   └── whatsapp.md
├── docs/
│   ├── SCHEMA.md                        ← Field definitions
│   └── WORKFLOW.md                      ← Daily workflow
└── scripts/
    └── validate_csv.py                  ← Data validation
```

---

## Key Concepts

### Two-Stage Pipeline

```
Sources → leads_*_raw.csv → crm_*_master.csv
           (staging)          (validated)
```

Raw data goes to `leads/` first. After validation & dedup, it merges to `crm/` master tables.

### Status vs Priority

**Status** = Where they are in funnel:
- `new` → `researched` → `contacted` → `responded` → `meeting` → `won`/`lost`

**Priority** = How hot:
- `hot` / `medium` / `low`

### Learning Loop

1. Log outreach with hooks and results
2. Script calculates what works
3. AI prioritizes best-performing approaches

---

## Integrations

Connect your communication channels so Cursor can see everything:

| Integration | What it does | Guide |
|-------------|--------------|-------|
| Telegram API | Read/send messages, manage groups | [Setup](integrations/telegram_api.md) |
| Telegram Remote | Control Cursor from your phone | [Setup](integrations/telegram_remote.md) |
| Gmail | Search emails, read threads | [Setup](integrations/gmail.md) |
| WhatsApp | Read chats via Baileys | [Setup](integrations/whatsapp.md) |

---

## Common Commands

### Find leads
```
"Show hot leads ready for outreach"
"Find companies that raised funding this month"
"Who haven't I contacted in 2 weeks?"
```

### Research
```
"Research John Smith at Acme — check LinkedIn, recent posts"
"What's the conversation history with Acme?"
"Find news about Acme's recent funding"
```

### Outreach
```
"Draft a message for John based on his AI infrastructure post"
"Write a follow-up — he didn't respond to my first message"
"Log that I contacted John via LinkedIn"
```

### Analysis
```
"What's my response rate this month?"
"Which hooks work best for Series A companies?"
"Show learnings report"
```

---

## Requirements

- **Cursor IDE** (free or pro)
- **Python 3.10+** 
- **pandas** (`pip install pandas`)

For integrations:
- Telegram: `pip install telethon`
- Gmail: `pip install google-auth google-api-python-client`
- WhatsApp: Node.js + Baileys

---

## Philosophy

1. **Your data stays yours** — CSV files, version controlled, no vendor lock-in
2. **AI does the work** — research, draft, log, analyze
3. **Simple beats complex** — if you need Salesforce, this isn't for you
4. **Learn what works** — built-in feedback loop on outreach effectiveness

---

## Who This Is For

✅ Solo founders doing outreach  
✅ Small teams (1-5 people) without dedicated sales ops  
✅ Developers who live in their IDE  
✅ Anyone tired of bloated CRM software  

❌ Enterprise teams needing complex workflows  
❌ People who want pretty dashboards  
❌ Teams requiring strict compliance/audit trails  

---

## Contributing

PRs welcome! Areas that need help:
- More integrations (Twitter/X, LinkedIn API)
- Better learning algorithms
- UI for non-technical users

---

## License

MIT — use freely, adapt to your business.

---

## Credits

Built by [@alexmazaltov](https://github.com/alexmazaltov) while doing sales for [Oleksii](https://oleksii.ch).

Inspired by the "Cursor CRM" movement and frustration with traditional CRMs.
