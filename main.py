#!/usr/bin/env python3
"""
==============================================
3D IN-VITRO MODELS LEAD GENERATOR
Complete Web Crawler - NO API KEYS REQUIRED
==============================================

This script crawls FREE public data sources:
- PubMed (scientific publications)
- NIH RePORTER (grant database)
- Europe PMC (European publications)
- ClinicalTrials.gov (clinical trials)
- Google Scholar (optional, rate limited)

Output: CSV and Excel files with ranked leads

Usage:
    python main.py
    
    or with options:
    python main.py --max-results 100 --skip-scholar
"""

import os
import sys
import argparse
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configuration
OUTPUT_DIR = "output"
YOUR_EMAIL = "student@university.edu"  # Change this to your email

# Keywords to search
RESEARCH_KEYWORDS = [
    "drug-induced liver injury",
    "hepatotoxicity in vitro",
    "3D liver model",
    "organ-on-chip liver",
    "hepatic spheroids toxicity",
    "liver toxicity models",
    "DILI prediction"
]

def create_output_dir():
    """Create output directory"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def crawl_pubmed(keywords, max_results):
    """Crawl PubMed"""
    from crawlers.pubmed_crawler import PubMedCrawler
    
    try:
        crawler = PubMedCrawler(email=YOUR_EMAIL)
        return crawler.crawl(keywords, max_results)
    except Exception as e:
        print(f"[PubMed] Error: {e}")
        return []

def crawl_nih(keywords, max_results):
    """Crawl NIH RePORTER"""
    from crawlers.nih_crawler import NIHReporterCrawler
    
    try:
        crawler = NIHReporterCrawler()
        return crawler.crawl(keywords, max_results)
    except Exception as e:
        print(f"[NIH] Error: {e}")
        return []

def crawl_europe_pmc(keywords, max_results):
    """Crawl Europe PMC"""
    from crawlers.europe_pmc_crawler import EuropePMCCrawler
    
    try:
        crawler = EuropePMCCrawler()
        return crawler.crawl(keywords, max_results)
    except Exception as e:
        print(f"[Europe PMC] Error: {e}")
        return []

def crawl_clinical_trials(keywords, max_results):
    """Crawl ClinicalTrials.gov"""
    from crawlers.clinical_trials_crawler import ClinicalTrialsCrawler
    
    try:
        crawler = ClinicalTrialsCrawler()
        return crawler.crawl(keywords, max_results)
    except Exception as e:
        print(f"[ClinicalTrials] Error: {e}")
        return []

def crawl_google_scholar(keywords, max_results):
    """Crawl Google Scholar (optional)"""
    from crawlers.google_scholar_crawler import GoogleScholarCrawler
    
    try:
        crawler = GoogleScholarCrawler()
        return crawler.crawl(keywords, max_results)
    except Exception as e:
        print(f"[Google Scholar] Error: {e}")
        return []

def enrich_emails(leads):
    """Add email addresses to leads"""
    from crawlers.email_generator import EmailGenerator
    
    try:
        generator = EmailGenerator()
        return generator.enrich_leads(leads)
    except Exception as e:
        print(f"[Email] Error: {e}")
        return leads

def score_leads(leads):
    """Score and rank leads"""
    from scoring.probability_engine import ProbabilityEngine
    
    try:
        engine = ProbabilityEngine()
        return engine.score_leads(leads)
    except Exception as e:
        print(f"[Scoring] Error: {e}")
        return leads

def remove_duplicates(leads):
    """Remove duplicate leads based on name + company"""
    print("\n[Dedup] Removing duplicates...")
    
    seen = set()
    unique_leads = []
    
    for lead in leads:
        key = (lead.get("name", "").lower(), lead.get("company", "").lower())
        if key not in seen:
            seen.add(key)
            unique_leads.append(lead)
    
    removed = len(leads) - len(unique_leads)
    print(f"[Dedup] ✓ Removed {removed} duplicates, {len(unique_leads)} unique leads")
    
    return unique_leads

def save_to_csv(leads, filename):
    """Save leads to CSV"""
    df = pd.DataFrame(leads)
    
    # Reorder columns to match expected format
    columns = [
        "name", "title", "company", "person_location", "company_hq",
        "funding_stage", "publication_topic", "publication_year",
        "uses_invitro", "email", "work_mode", "company_in_hub",
        "probability_score", "rank"
    ]
    
    # Add missing columns
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    
    # Reorder
    df = df[columns]
    
    # Save
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.csv")
    df.to_csv(filepath, index=False)
    print(f"\n✓ Saved CSV: {filepath}")
    
    return filepath

def save_to_excel(leads, filename):
    """Save leads to Excel"""
    df = pd.DataFrame(leads)
    
    # Reorder columns
    columns = [
        "name", "title", "company", "person_location", "company_hq",
        "funding_stage", "publication_topic", "publication_year",
        "uses_invitro", "email", "work_mode", "company_in_hub",
        "probability_score", "rank"
    ]
    
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    
    df = df[columns]
    
    # Save
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.xlsx")
    df.to_excel(filepath, index=False, sheet_name="Leads")
    print(f"✓ Saved Excel: {filepath}")
    
    return filepath

def print_summary(leads):
    """Print summary statistics"""
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"Total leads: {len(leads)}")
    
    if leads:
        scores = [l.get("probability_score", 0) for l in leads]
        print(f"Average score: {sum(scores)/len(scores):.1f}")
        print(f"High-quality (≥70): {sum(1 for s in scores if s >= 70)}")
        print(f"Medium (40-69): {sum(1 for s in scores if 40 <= s < 70)}")
        print(f"Low (<40): {sum(1 for s in scores if s < 40)}")
        
        # Source breakdown
        sources = {}
        for lead in leads:
            src = lead.get("source", "Unknown")
            sources[src] = sources.get(src, 0) + 1
        
        print("\nBy source:")
        for src, count in sorted(sources.items(), key=lambda x: -x[1]):
            print(f"  {src}: {count}")
        
        # Top leads
        print("\nTop 5 leads:")
        for lead in leads[:5]:
            print(f"  #{lead.get('rank', '?')} ({lead.get('probability_score', 0)}) {lead.get('name', 'Unknown')} - {lead.get('company', 'Unknown')[:30]}")

def main():
    """Main function"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="3D In-Vitro Lead Generator")
    parser.add_argument("--max-results", type=int, default=50, help="Max results per source")
    parser.add_argument("--skip-scholar", action="store_true", help="Skip Google Scholar (faster)")
    parser.add_argument("--output-name", type=str, default=None, help="Output filename")
    args = parser.parse_args()
    
    # Banner
    print("=" * 60)
    print("🔬 3D IN-VITRO MODELS LEAD GENERATOR")
    print("   Web Crawler - NO API KEYS REQUIRED")
    print("=" * 60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Max results per source: {args.max_results}")
    print("=" * 60)
    
    # Create output directory
    create_output_dir()
    
    # Collect all leads
    all_leads = []
    
    # 1. PubMed
    print("\n📚 SOURCE 1: PubMed (Scientific Publications)")
    print("-" * 40)
    pubmed_leads = crawl_pubmed(RESEARCH_KEYWORDS, args.max_results)
    all_leads.extend(pubmed_leads)
    
    # 2. NIH RePORTER
    print("\n💰 SOURCE 2: NIH RePORTER (Grants)")
    print("-" * 40)
    nih_leads = crawl_nih(RESEARCH_KEYWORDS, args.max_results)
    all_leads.extend(nih_leads)
    
    # 3. Europe PMC
    print("\n🇪🇺 SOURCE 3: Europe PMC (European Publications)")
    print("-" * 40)
    epmc_leads = crawl_europe_pmc(RESEARCH_KEYWORDS, args.max_results)
    all_leads.extend(epmc_leads)
    
    # 4. ClinicalTrials.gov
    print("\n🏥 SOURCE 4: ClinicalTrials.gov")
    print("-" * 40)
    ct_leads = crawl_clinical_trials(RESEARCH_KEYWORDS, args.max_results)
    all_leads.extend(ct_leads)
    
    # 5. Google Scholar (optional)
    if not args.skip_scholar:
        print("\n📖 SOURCE 5: Google Scholar (Optional - may be slow)")
        print("-" * 40)
        scholar_leads = crawl_google_scholar(RESEARCH_KEYWORDS, min(args.max_results, 20))
        all_leads.extend(scholar_leads)
    else:
        print("\n[Google Scholar] Skipped (use --skip-scholar=false to include)")
    
    # Check if we got any leads
    if not all_leads:
        print("\n⚠️ No leads found! Check your internet connection or try different keywords.")
        return
    
    print(f"\n📊 Total raw leads collected: {len(all_leads)}")
    
    # Remove duplicates
    all_leads = remove_duplicates(all_leads)
    
    # Enrich with emails
    all_leads = enrich_emails(all_leads)
    
    # Score and rank
    all_leads = score_leads(all_leads)
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = args.output_name or f"3d_invitro_leads_{timestamp}"
    
    # Save outputs
    print("\n💾 SAVING OUTPUT FILES")
    print("-" * 40)
    csv_path = save_to_csv(all_leads, filename)
    excel_path = save_to_excel(all_leads, filename)
    
    # Print summary
    print_summary(all_leads)
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE!")
    print("=" * 60)
    print(f"Output files saved to: {OUTPUT_DIR}/")
    print(f"  - {filename}.csv")
    print(f"  - {filename}.xlsx")
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()