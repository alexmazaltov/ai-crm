#!/usr/bin/env python3
"""
Weekly learning loop: derive outreach learnings from crm_outreach_activities.csv.

PURPOSE:
  Track which hooks work best for which audience segments.
  Prioritize research: check high-salience hooks first during lead research.

INPUTS (from crm_outreach_activities.csv):
  - audience_segment: yc_founder/big_tech_alumni/ukrainian/enterprise/seed_stage/series_a/other
  - hooks_checked: comma-separated (funding,mutual,post,pain_point)
  - hooks_available: comma-separated (funding,mutual)
  - hook_type: funding/job_signal/mutual_connection/recent_post/pain_point/other
  - response_quality: none/negative/neutral/positive/meeting

OUTPUT (to learnings.csv):
  learning_id, type, audience_segment, insight, salience, evidence_count, created_date, last_validated

SCORING:
  meeting  -> +0.3
  positive -> +0.2
  neutral  -> +0.1
  none     -> -0.05
  negative -> -0.1

TIME DECAY:
  -0.02/week since last activity date in that bucket

USAGE:
  python3 sales/learnings/update_salience.py --recalc
  python3 sales/learnings/update_salience.py --report   # just show stats
"""

from __future__ import annotations

import argparse
import uuid
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

import pandas as pd


# Use relative paths from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ACTIVITIES = BASE_DIR / "sales/crm/crm_outreach_activities.csv"
LEARNINGS_DIR = BASE_DIR / "sales/learnings"
LEARNINGS_FILE = LEARNINGS_DIR / "learnings.csv"


# Response quality weights
WEIGHTS = {
    "meeting": 0.3,
    "positive": 0.2,
    "neutral": 0.1,
    "none": -0.05,
    "negative": -0.1,
}

# Valid audience segments
AUDIENCE_SEGMENTS = {
    "yc_founder",
    "techstars",
    "big_tech_alumni",
    "ukrainian",
    "enterprise",
    "seed_stage",
    "series_a",
    "other",
    "all",  # default/aggregate
}

# Valid hook types
HOOK_TYPES = {
    "funding",
    "job_signal",
    "mutual_connection",
    "recent_post",
    "pain_point",
    "other",
}


def today_iso() -> str:
    return date.today().isoformat()


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def normalize_response_quality(row: dict) -> str:
    """Normalize response_quality, with fallback to legacy result field."""
    rq = str(row.get("response_quality") or "").strip().lower()
    if rq in WEIGHTS:
        return rq

    # Fallback heuristic from legacy `result`
    res = str(row.get("result") or "").strip().lower()
    if any(k in res for k in ["meeting", "call_scheduled", "demo", "booked"]):
        return "meeting"
    if any(k in res for k in ["replied", "accepted", "responded", "positive"]):
        return "positive"
    if any(k in res for k in ["neutral"]):
        return "neutral"
    if any(k in res for k in ["rejected", "not_interested", "blocked", "spam", "negative"]):
        return "negative"
    return "none"


def normalize_hook_type(row: dict) -> str:
    """Normalize hook_type to allowed values."""
    ht = str(row.get("hook_type") or "").strip().lower()
    
    # Map job_signal variations
    if "job" in ht or "hiring" in ht:
        return "job_signal"
    if "fund" in ht:
        return "funding"
    if "mutual" in ht or "connection" in ht:
        return "mutual_connection"
    if "post" in ht or "activity" in ht:
        return "recent_post"
    if "pain" in ht:
        return "pain_point"
    
    return ht if ht in HOOK_TYPES else "other"


def normalize_audience(row: dict) -> str:
    """Normalize audience_segment to allowed values."""
    aud = str(row.get("audience_segment") or "").strip().lower()
    
    # Map variations
    if "yc" in aud:
        return "yc_founder"
    if "techstars" in aud:
        return "techstars"
    if "big" in aud and "tech" in aud:
        return "big_tech_alumni"
    if "ukr" in aud:
        return "ukrainian"
    if "enterprise" in aud:
        return "enterprise"
    if "seed" in aud:
        return "seed_stage"
    if "series" in aud:
        return "series_a"
    
    return aud if aud in AUDIENCE_SEGMENTS else "other"


def parse_activity_date(row: dict) -> date | None:
    """Parse date from row, checking multiple possible columns."""
    for col in ["date", "ts_iso"]:
        d = str(row.get(col) or "").strip()
        if d:
            try:
                return datetime.fromisoformat(d[:10]).date()
            except Exception:
                try:
                    return datetime.strptime(d[:10], "%Y-%m-%d").date()
                except Exception:
                    continue
    return None


@dataclass
class BucketStats:
    """Statistics for a hook+audience bucket."""
    n: int = 0
    sum_delta: float = 0.0
    last_date: date | None = None
    responses: dict = field(default_factory=lambda: defaultdict(int))
    
    @property
    def avg_delta(self) -> float:
        return self.sum_delta / self.n if self.n > 0 else 0.0
    
    @property
    def response_rate(self) -> float:
        """Rate of positive+ responses."""
        positive = self.responses.get("meeting", 0) + self.responses.get("positive", 0)
        return positive / self.n if self.n > 0 else 0.0


def compute_bucket_stats(df: pd.DataFrame) -> dict[tuple[str, str], BucketStats]:
    """
    Compute stats grouped by (hook_type, audience_segment).
    Returns dict with key (hook, audience) -> BucketStats
    """
    stats: dict[tuple[str, str], BucketStats] = {}
    
    for _, row in df.iterrows():
        hook = row.get("hook_type_norm", "other")
        audience = row.get("audience_norm", "other")
        rq = row.get("response_quality_norm", "none")
        delta = WEIGHTS.get(rq, 0.0)
        act_date = row.get("activity_date")
        
        key = (hook, audience)
        if key not in stats:
            stats[key] = BucketStats()
        
        s = stats[key]
        s.n += 1
        s.sum_delta += delta
        s.responses[rq] += 1
        if act_date and (s.last_date is None or act_date > s.last_date):
            s.last_date = act_date
        
        # Also aggregate to "all" audience
        key_all = (hook, "all")
        if key_all not in stats:
            stats[key_all] = BucketStats()
        s_all = stats[key_all]
        s_all.n += 1
        s_all.sum_delta += delta
        s_all.responses[rq] += 1
        if act_date and (s_all.last_date is None or act_date > s_all.last_date):
            s_all.last_date = act_date
    
    return stats


def ensure_learnings_file() -> None:
    """Ensure learnings directory and file exist."""
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    if not LEARNINGS_FILE.exists():
        LEARNINGS_FILE.write_text(
            "learning_id,type,audience_segment,insight,salience,evidence_count,created_date,last_validated\n",
            encoding="utf-8",
        )


def load_learnings() -> pd.DataFrame:
    """Load existing learnings."""
    ensure_learnings_file()
    df = pd.read_csv(LEARNINGS_FILE)
    required_cols = [
        "learning_id", "type", "audience_segment", "insight",
        "salience", "evidence_count", "created_date", "last_validated",
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
    return df


def calculate_salience(s: BucketStats) -> float:
    """
    Calculate salience score for a bucket.
    Base: 0.5, adjusted by average delta, with time decay.
    """
    salience = 0.5 + s.avg_delta
    
    # Time decay from last activity
    if s.last_date is not None:
        weeks = max(0.0, (date.today() - s.last_date).days / 7.0)
        salience -= 0.02 * weeks
    
    return clamp01(salience)


def generate_report(stats: dict[tuple[str, str], BucketStats]) -> str:
    """Generate human-readable report."""
    lines = [
        "=" * 60,
        "📊 LEARNING LOOP REPORT",
        "=" * 60,
        "",
        "### BY HOOK TYPE (all audiences)",
        "",
    ]
    
    # Sort by salience
    all_hooks = [(k, s) for k, s in stats.items() if k[1] == "all"]
    all_hooks.sort(key=lambda x: calculate_salience(x[1]), reverse=True)
    
    lines.append(f"{'Hook':<20} {'N':>5} {'Salience':>10} {'Response%':>10}")
    lines.append("-" * 50)
    for (hook, _), s in all_hooks:
        sal = calculate_salience(s)
        rr = s.response_rate * 100
        lines.append(f"{hook:<20} {s.n:>5} {sal:>10.2f} {rr:>9.1f}%")
    
    # By audience
    lines.extend(["", "### BY AUDIENCE SEGMENT", ""])
    
    audiences = set(k[1] for k in stats.keys() if k[1] != "all")
    for aud in sorted(audiences):
        aud_stats = [(k, s) for k, s in stats.items() if k[1] == aud]
        if not aud_stats:
            continue
        
        aud_stats.sort(key=lambda x: calculate_salience(x[1]), reverse=True)
        
        lines.append(f"\n**{aud.upper()}**")
        lines.append(f"{'Hook':<20} {'N':>5} {'Salience':>10} {'Response%':>10}")
        lines.append("-" * 50)
        for (hook, _), s in aud_stats:
            sal = calculate_salience(s)
            rr = s.response_rate * 100
            lines.append(f"{hook:<20} {s.n:>5} {sal:>10.2f} {rr:>9.1f}%")
    
    # Research priority recommendation
    lines.extend(["", "### 🎯 RESEARCH PRIORITY (check hooks in this order)", ""])
    
    for aud in sorted(audiences):
        aud_stats = [(k[0], calculate_salience(s)) for k, s in stats.items() if k[1] == aud]
        aud_stats.sort(key=lambda x: x[1], reverse=True)
        
        hooks_order = [h for h, _ in aud_stats if h != "other"]
        lines.append(f"{aud}: {' → '.join(hooks_order)}")
    
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Update learning loop salience scores")
    ap.add_argument("--recalc", action="store_true", help="Recompute salience from scratch")
    ap.add_argument("--report", action="store_true", help="Just show report, don't save")
    args = ap.parse_args()

    if not ACTIVITIES.exists():
        print(f"No activities file yet: {ACTIVITIES}")
        print("Start logging outreach activities to build learnings.")
        return

    # Load activities
    acts = pd.read_csv(ACTIVITIES)
    if acts.empty:
        print("No activities found. Nothing to do.")
        return

    # Ensure required columns exist
    for col in ["hook_type", "response_quality", "audience_segment"]:
        if col not in acts.columns:
            acts[col] = ""

    # Normalize columns
    acts["hook_type_norm"] = acts.apply(lambda r: normalize_hook_type(r.to_dict()), axis=1)
    acts["response_quality_norm"] = acts.apply(lambda r: normalize_response_quality(r.to_dict()), axis=1)
    acts["audience_norm"] = acts.apply(lambda r: normalize_audience(r.to_dict()), axis=1)
    acts["activity_date"] = acts.apply(lambda r: parse_activity_date(r.to_dict()), axis=1)

    # Compute stats
    stats = compute_bucket_stats(acts)
    
    # Print report
    report = generate_report(stats)
    print(report)
    
    if args.report:
        return
    
    # Update learnings.csv
    learn = load_learnings()
    today = today_iso()

    def upsert_learning(hook: str, audience: str, s: BucketStats) -> None:
        nonlocal learn
        
        kind = "hook"
        insight = hook
        
        mask = (
            (learn["type"].astype(str) == kind) &
            (learn["insight"].astype(str) == insight) &
            (learn["audience_segment"].astype(str) == audience)
        )
        
        if mask.any():
            i = learn.index[mask][0]
            created = str(learn.at[i, "created_date"] or today)
            learning_id = str(learn.at[i, "learning_id"] or uuid.uuid4())
        else:
            i = None
            created = today
            learning_id = str(uuid.uuid4())

        salience = calculate_salience(s)

        row = {
            "learning_id": learning_id,
            "type": kind,
            "audience_segment": audience,
            "insight": insight,
            "salience": round(float(salience), 4),
            "evidence_count": int(s.n),
            "created_date": created,
            "last_validated": today,
        }

        if i is None:
            learn = pd.concat([learn, pd.DataFrame([row])], ignore_index=True)
        else:
            for k, v in row.items():
                learn.at[i, k] = v

    # Upsert all hook+audience combinations
    for (hook, audience), s in stats.items():
        upsert_learning(hook, audience, s)

    # Save
    learn.to_csv(LEARNINGS_FILE, index=False)
    print(f"\n✅ Updated {LEARNINGS_FILE}")
    print(f"Total learnings: {len(learn)}")


if __name__ == "__main__":
    main()
