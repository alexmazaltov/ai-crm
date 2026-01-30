#!/usr/bin/env python3
"""
Validate CRM CSV files for common issues.

Usage:
    python3 scripts/validate_csv.py
    python3 scripts/validate_csv.py --fix  # Auto-fix what can be fixed
"""

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
CRM_DIR = BASE_DIR / "sales/crm"


def today_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def validate_companies(fix: bool = False) -> list[str]:
    """Validate crm_companies_master.csv"""
    errors = []
    path = CRM_DIR / "crm_companies_master.csv"
    
    if not path.exists():
        return ["companies file not found"]
    
    df = pd.read_csv(path)
    
    if df.empty:
        return []  # Empty is OK for starter
    
    # Check required fields
    for i, row in df.iterrows():
        # company_name or website required
        if pd.isna(row.get("company_name")) and pd.isna(row.get("website")):
            errors.append(f"Row {i+2}: company_name or website required")
        
        # If signal_type set, signal_source_url required
        if pd.notna(row.get("signal_type")) and pd.isna(row.get("signal_source_url")):
            errors.append(f"Row {i+2}: signal_type set but signal_source_url missing")
        
        # Check last_updated
        if pd.isna(row.get("last_updated")):
            if fix:
                df.at[i, "last_updated"] = today_iso()
            else:
                errors.append(f"Row {i+2}: last_updated missing")
    
    if fix and errors:
        df.to_csv(path, index=False)
        print(f"Fixed {len(errors)} issues in companies")
    
    return errors


def validate_people(fix: bool = False) -> list[str]:
    """Validate crm_people_master.csv"""
    errors = []
    path = CRM_DIR / "crm_people_master.csv"
    
    if not path.exists():
        return ["people file not found"]
    
    df = pd.read_csv(path)
    
    if df.empty:
        return []  # Empty is OK for starter
    
    for i, row in df.iterrows():
        # linkedin_url required and must contain linkedin.com
        url = str(row.get("linkedin_url") or "")
        if not url or "linkedin.com" not in url.lower():
            errors.append(f"Row {i+2}: linkedin_url missing or invalid")
        
        # first_name required
        if pd.isna(row.get("first_name")) or not str(row.get("first_name")).strip():
            errors.append(f"Row {i+2}: first_name missing")
        
        # last_name required
        if pd.isna(row.get("last_name")) or not str(row.get("last_name")).strip():
            errors.append(f"Row {i+2}: last_name missing")
        
        # Check last_updated
        if pd.isna(row.get("last_updated")):
            if fix:
                df.at[i, "last_updated"] = today_iso()
            else:
                errors.append(f"Row {i+2}: last_updated missing")
    
    # Check for duplicates
    if "linkedin_url" in df.columns:
        dupes = df[df["linkedin_url"].duplicated(keep=False)]
        if not dupes.empty:
            dupe_urls = dupes["linkedin_url"].unique()
            for url in dupe_urls:
                errors.append(f"Duplicate linkedin_url: {url}")
    
    if fix and errors:
        df.to_csv(path, index=False)
        print(f"Fixed some issues in people")
    
    return errors


def validate_activities() -> list[str]:
    """Validate crm_outreach_activities.csv"""
    errors = []
    path = CRM_DIR / "crm_outreach_activities.csv"
    
    if not path.exists():
        return ["activities file not found"]
    
    df = pd.read_csv(path)
    
    if df.empty:
        return []
    
    valid_channels = {"linkedin", "email", "twitter", "intro"}
    valid_types = {"dm", "request_intro", "followup", "email_sent", "call", "research_done"}
    
    for i, row in df.iterrows():
        # linkedin_url required
        if pd.isna(row.get("linkedin_url")):
            errors.append(f"Row {i+2}: linkedin_url missing")
        
        # date required
        if pd.isna(row.get("date")):
            errors.append(f"Row {i+2}: date missing")
        
        # channel validation
        channel = str(row.get("channel") or "").lower()
        if channel and channel not in valid_channels:
            errors.append(f"Row {i+2}: invalid channel '{channel}'")
        
        # activity_type validation
        atype = str(row.get("activity_type") or "").lower()
        if atype and atype not in valid_types:
            errors.append(f"Row {i+2}: invalid activity_type '{atype}'")
    
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate CRM CSV files")
    parser.add_argument("--fix", action="store_true", help="Auto-fix what can be fixed")
    args = parser.parse_args()
    
    print("=" * 50)
    print("CRM VALIDATION REPORT")
    print("=" * 50)
    
    all_errors = []
    
    # Companies
    print("\n📋 Validating companies...")
    errors = validate_companies(fix=args.fix)
    if errors:
        print(f"  ❌ {len(errors)} issues:")
        for e in errors[:5]:
            print(f"     - {e}")
        if len(errors) > 5:
            print(f"     ... and {len(errors) - 5} more")
    else:
        print("  ✅ OK")
    all_errors.extend(errors)
    
    # People
    print("\n👤 Validating people...")
    errors = validate_people(fix=args.fix)
    if errors:
        print(f"  ❌ {len(errors)} issues:")
        for e in errors[:5]:
            print(f"     - {e}")
        if len(errors) > 5:
            print(f"     ... and {len(errors) - 5} more")
    else:
        print("  ✅ OK")
    all_errors.extend(errors)
    
    # Activities
    print("\n📝 Validating activities...")
    errors = validate_activities()
    if errors:
        print(f"  ❌ {len(errors)} issues:")
        for e in errors[:5]:
            print(f"     - {e}")
        if len(errors) > 5:
            print(f"     ... and {len(errors) - 5} more")
    else:
        print("  ✅ OK")
    all_errors.extend(errors)
    
    # Summary
    print("\n" + "=" * 50)
    if all_errors:
        print(f"❌ Total: {len(all_errors)} issues found")
        if not args.fix:
            print("   Run with --fix to auto-fix what can be fixed")
    else:
        print("✅ All validations passed!")
    
    return len(all_errors)


if __name__ == "__main__":
    exit(main())
