# CRM Schema Reference

## Overview

| Table | Primary Key | Description |
|-------|-------------|-------------|
| crm_companies_master.csv | website | All companies |
| crm_people_master.csv | linkedin_url | All contacts |
| crm_outreach_activities.csv | activity_id | Activity log |
| crm_sources.csv | linkedin_url + source_tag | Source tracking |

---

## crm_companies_master.csv

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| company_id | UUID | Yes | Unique identifier |
| company_name | string | Yes | Company name |
| website | string | Yes (PK) | Company website (unique identifier) |
| linkedin_company_url | string | No | LinkedIn company page URL |
| stage | enum | No | seed / series_a / series_b / growth |
| funding_amount | string | No | e.g., "$5M", "$500K" |
| funding_date | YYYY-MM | No | When funding was announced |
| ai_focus | string | No | AI/ML focus area |
| vertical | string | No | Industry vertical |
| geo | string | No | Geographic location |
| signal_type | enum | No | funding / hiring / product_launch / partnership |
| signal_source_url | URL | If signal_type set | Source of the signal |
| primary_source | string | No | Main source (one value) |
| source_tags | string | No | Comma-separated source tags |
| status | enum | Yes | new / researched / contacted / meeting / won / lost |
| priority | enum | Yes | hot / medium / low |
| contact_email | string | No | General contact email |
| notes | string | No | Free-form notes |
| created_date | YYYY-MM-DD | Yes | When record was created |
| last_updated | YYYY-MM-DD | Yes | When record was last modified |
| lead_status | enum | No | Lead funnel stage |
| next_action | string | No | Next action to take |
| next_action_due | YYYY-MM-DD | No | When next action is due |
| next_action_owner | string | No | Who owns the action |
| last_inbound_date | YYYY-MM-DD | No | Last inbound contact |
| last_outbound_date | YYYY-MM-DD | No | Last outbound contact |

---

## crm_people_master.csv

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| person_id | UUID | Yes | Unique identifier |
| linkedin_url | string | Yes (PK) | LinkedIn profile URL (must contain "linkedin.com") |
| first_name | string | Yes | First name |
| last_name | string | Yes | Last name |
| company_website | string | No | FK to crm_companies_master |
| company_name | string | No | Company name |
| role | string | No | Job title |
| email | string | No | Email address |
| connection_degree | enum | No | 1 / 2 / 3 |
| mutual_connections_count | integer | No | Number of mutual connections |
| primary_source | string | No | Main source (one value) |
| source_tags | string | No | Comma-separated source tags |
| status | enum | Yes | new / researched / contacted / responded / meeting / won / lost |
| priority | enum | Yes | hot / medium / low |
| personalization_hook | string | No | 1 sentence personalization hook |
| hook_source_url | URL | No | Source of the hook |
| notes | string | No | Free-form notes |
| last_contact_date | YYYY-MM-DD | No | When last contacted |
| next_followup_date | YYYY-MM-DD | No | When to follow up |
| created_date | YYYY-MM-DD | Yes | When record was created |
| last_updated | YYYY-MM-DD | Yes | When record was last modified |

---

## crm_outreach_activities.csv

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| activity_id | UUID | Yes | Unique identifier |
| linkedin_url | string | Yes | FK to crm_people_master |
| date | YYYY-MM-DD | Yes | When activity happened |
| channel | enum | Yes | linkedin / email / twitter / intro |
| activity_type | enum | Yes | dm / request_intro / followup / email_sent / call / research_done |
| message_preview | string | No | First 100 chars of message |
| result | enum | No | sent / bounced / replied / no_response / accepted / rejected |
| next_followup_date | YYYY-MM-DD | No | When to follow up |
| notes | string | No | Free-form notes |
| audience_segment | enum | No | yc_founder / big_tech_alumni / ukrainian / enterprise / seed_stage / series_a / other |
| hooks_checked | string | No | Comma-separated list of hooks checked |
| hooks_available | string | No | Comma-separated list of available hooks |
| hook_type | enum | No | funding / job_signal / mutual_connection / recent_post / pain_point / other |
| response_quality | enum | No | none / negative / neutral / positive / meeting |

---

## crm_sources.csv

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| linkedin_url | string | Yes | FK to crm_people_master |
| source_tag | string | Yes | Source identifier |
| source_date | YYYY-MM-DD | Yes | When source was added |

---

## Status Values

### Company/Person Status (Funnel)
```
new → researched → contacted → responded → meeting → won
                                                   ↘ lost
```

### Priority
```
hot    = High priority, contact ASAP
medium = Normal priority
low    = Low priority, can wait
```

### Channel
```
linkedin = LinkedIn DM or connection request
email    = Email
twitter  = Twitter/X DM
intro    = Introduction via mutual connection
```

### Activity Type
```
dm             = Direct message
request_intro  = Asked for introduction
followup       = Follow-up message
email_sent     = Email sent
call           = Phone/video call
research_done  = Research completed
```

### Response Quality (for Learning Loop)
```
meeting  = Scheduled a meeting (+0.3)
positive = Positive response (+0.2)
neutral  = Neutral response (+0.1)
none     = No response (-0.05)
negative = Negative response (-0.1)
```

### Audience Segment
```
yc_founder      = YC alumni
techstars       = Techstars alumni
big_tech_alumni = Ex-FAANG
ukrainian       = Ukrainian founder
enterprise      = Enterprise company
seed_stage      = Seed stage startup
series_a        = Series A+ startup
other           = Other
```

### Hook Type
```
funding           = Recent funding announcement
job_signal        = Hiring for relevant role
mutual_connection = Shared connection
recent_post       = Recent LinkedIn/Twitter activity
pain_point        = Hypothesis about their pain
other             = Other hook
```

---

## Validation Rules

### Before adding a Company:
- [ ] website OR company_name is not empty
- [ ] If signal_type is set, signal_source_url must be set
- [ ] Check if website already exists (dedupe)
- [ ] Set created_date and last_updated to today

### Before adding a Person:
- [ ] linkedin_url contains "linkedin.com"
- [ ] first_name is not empty
- [ ] last_name is not empty
- [ ] Check if linkedin_url already exists (dedupe)
- [ ] Set created_date and last_updated to today

### When updating any record:
- [ ] ALWAYS update last_updated to today
