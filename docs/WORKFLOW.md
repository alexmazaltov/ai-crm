# Daily CRM Workflow

## Morning Routine (15 min)

### 1. Check Follow-ups
```bash
# People with follow-up due today
grep "$(date +%Y-%m-%d)" sales/crm/crm_people_master.csv | grep "next_followup"
```

Or ask Cursor:
> "Show people where next_followup_date is today"

### 2. Check Hot Leads
```bash
grep ",hot," sales/crm/crm_people_master.csv | grep ",new,\|,researched,"
```

Or ask Cursor:
> "Show hot leads that haven't been contacted yet"

---

## Research Flow

### Step 1: Pick a Lead
- Priority: hot > medium > low
- Status: new (needs research)

### Step 2: Research Checklist

For each lead, check:

1. **Company website**
   - What do they do?
   - What technology?
   - Any recent news?

2. **LinkedIn Company Page**
   - Size/employees
   - Recent posts
   - Job openings (signals!)

3. **LinkedIn Person Profile**
   - Current role
   - Background
   - Recent activity (posts, comments)
   - Mutual connections
   - Featured section

4. **Funding/Signals**
   - Crunchbase
   - TechCrunch
   - Recent announcements

### Step 3: Document Findings

Update CRM record:
- `personalization_hook` = 1 sentence hook
- `hook_source_url` = where you found it
- `notes` = additional context
- `status` = researched
- `last_updated` = today

---

## Outreach Flow

### Step 1: Check History
> "What's the conversation history with [person]?"

Look for:
- Previous messages
- Previous responses
- Previous rejections

### Step 2: Draft Message

Use `sales/outreach/OUTREACH_PROMPT.md` template:
- Scenario A = First contact
- Scenario B = Follow-up (no response)
- Scenario C = Re-engagement (after rejection)

### Step 3: Send & Log

After sending:
1. Log in crm_outreach_activities.csv:
   - linkedin_url
   - date = today
   - channel = linkedin/email/etc
   - activity_type = dm/followup/etc
   - message_preview (first 100 chars)
   - result = sent
   - audience_segment
   - hook_type

2. Update person:
   - status = contacted
   - last_contact_date = today
   - next_followup_date = +7 days
   - last_updated = today

---

## Response Handling

### When you get a response:

1. **Update activity** with response_quality:
   - meeting = they want to meet
   - positive = interested, asking questions
   - neutral = polite but non-committal
   - negative = not interested

2. **Update person status**:
   - → responded (if positive/neutral)
   - → meeting (if meeting scheduled)
   - → lost (if explicitly rejected)

3. **Set next action**:
   - Schedule meeting
   - Send info
   - Follow up in X days

---

## Weekly Review (30 min)

### 1. Update Learnings
```bash
python3 sales/learnings/update_salience.py --recalc
```

### 2. Review Metrics

Ask Cursor:
> "How many leads did I contact this week?"
> "What's my response rate?"
> "Which hooks got responses?"

### 3. Clean Up

- Mark stale leads as cold
- Archive lost opportunities
- Update priorities based on learnings

---

## New Hypothesis Workflow

When exploring a new market segment:

### 1. Create Folder
```bash
mkdir sales/leads/[hypothesis_name]
```

### 2. Collect Raw Data
- Scrape/collect companies
- Save to `sales/leads/[hypothesis]/companies.csv`

### 3. Validate & Dedupe
- Check each company is real
- Check for duplicates in master

### 4. Merge to Master
Ask Cursor:
> "Merge companies from [hypothesis] to CRM, tag with source [hypothesis_name]"

### 5. Find Decision Makers
> "Find CEO and CTO for these companies on LinkedIn"

### 6. Research & Outreach
Follow normal flow.

---

## Common Requests to Cursor

### Finding Leads
- "Find YC W2025 AI startups"
- "Search LinkedIn for ML engineers at [company]"
- "Find companies hiring for data labeling"

### CRM Queries
- "Show all hot leads"
- "Count leads by status"
- "Who haven't I contacted in 2 weeks?"

### Research
- "Research [person name] at [company]"
- "Find recent news about [company]"
- "Check [person]'s recent LinkedIn posts"

### Outreach
- "Draft a message for [person] based on their recent post"
- "Write a follow-up for [person] - they didn't respond"
- "Log that I contacted [person] via LinkedIn"

### Analysis
- "What's my response rate this month?"
- "Which audience segment converts best?"
- "Show me learnings report"
