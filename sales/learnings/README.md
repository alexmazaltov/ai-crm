# Learning Loop System

## Purpose

Analyze which hooks work for which audience.
When researching a new lead — look for signals that work best.

---

## How It Works

### 1. When RESEARCHING a new lead

Check hooks **by priority** (based on salience for this audience):

```
1. Is there a funding signal? → If YES — use this hook
2. Is there a mutual connection? → If YES — use it
3. Is there a recent post/activity? → If YES — use it
4. Pain point hypothesis → Always available (fallback)
```

**Important**: DON'T invent hooks that don't exist! If there was no funding — don't write about funding.

### 2. When doing OUTREACH — log in CRM

```csv
audience_segment: yc_founder | techstars | big_tech_alumni | ukrainian | enterprise | seed_stage | series_a | other
hooks_checked: funding,mutual,post   (which you checked)
hooks_available: funding,mutual      (which were available)
hook_type: funding                   (which you used)
response_quality: none | negative | neutral | positive | meeting
```

### 3. Weekly — run the script

```bash
python3 sales/learnings/update_salience.py --recalc
```

Shows:
- Which hooks work (salience 0-1)
- For which audience
- Response rate for each
- Recommended research priority

---

## Files

| File | Description |
|------|-------------|
| `crm_outreach_activities.csv` | Log of all outreach with hook_type, audience, response |
| `learnings.csv` | Calculated salience by hook+audience |
| `update_salience.py` | Script for recalculation |

---

## Salience Formula

```
base = 0.5
+ meeting:  +0.3
+ positive: +0.2
+ neutral:  +0.1
+ none:     -0.05
+ negative: -0.1

time_decay: -0.02 per week without activity
```

---

## Example Output

```
📊 LEARNING LOOP REPORT

### BY HOOK TYPE (all audiences)

Hook                     N   Salience  Response%
--------------------------------------------------
funding                 15       0.72      26.7%
mutual_connection        8       0.65      12.5%
job_signal              12       0.58      16.7%
recent_post             20       0.48       5.0%
pain_point              25       0.42       4.0%

### BY AUDIENCE SEGMENT

**YC_FOUNDER**
funding                  5       0.85      40.0%
mutual_connection        3       0.70      33.3%

**UKRAINIAN**
mutual_connection        4       0.91      50.0%
funding                  2       0.65      50.0%

### 🎯 RESEARCH PRIORITY

yc_founder: funding → mutual_connection → job_signal
ukrainian: mutual_connection → funding → pain_point
enterprise: pain_point → job_signal → funding
```

---

## How to Read

- **Salience > 0.7** = works well, search for this hook first
- **Salience 0.5-0.7** = average, use if nothing better available
- **Salience < 0.5** = works poorly, avoid

---

## Research Flow by Audience

### YC Founder
1. ✅ Funding (fresh round, YC batch)
2. ✅ Mutual (other YC founders)
3. ⏭️ Pain point

### Ukrainian Founder
1. ✅ Mutual 🇺🇦 connection
2. ✅ Funding
3. ⏭️ Pain point

### Big Tech Alumni
1. ✅ Mutual (ex-colleagues)
2. ✅ Recent post (thought leadership)
3. ⏭️ Pain point

### Enterprise
1. ✅ Pain point (specific use case)
2. ✅ Job signal (hiring for relevant role)
3. ⏭️ Funding
