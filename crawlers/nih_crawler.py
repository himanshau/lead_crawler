"""
NIH RePORTER Crawler - 100% FREE, NO API KEY REQUIRED
Uses public NIH RePORTER API v2
"""

import requests
from datetime import datetime
import time

class NIHReporterCrawler:
    """Crawls NIH RePORTER for grant recipients (Principal Investigators)"""
    
    API_URL = "https://api.reporter.nih.gov/v2/projects/search"
    
    def __init__(self):
        self.leads = []
    
    def search(self, query, max_results=50):
        """Search NIH RePORTER for grants"""
        print(f"[NIH] Searching: {query[:80]}...")
        
        current_year = datetime.now().year
        fiscal_years = list(range(current_year - 2, current_year + 1))
        
        payload = {
            "criteria": {
                "advanced_text_search": {
                    "search_text": query,
                    "operator": "or",
                    "search_field": "projecttitle,terms"
                },
                "fiscal_years": fiscal_years,
                "exclude_subprojects": True
            },
            "include_fields": [
                "project_num",
                "project_title",
                "contact_pi_name",
                "principal_investigators",
                "org_name",
                "org_city",
                "org_state",
                "org_country",
                "project_start_date",
                "project_end_date",
                "award_amount",
                "terms"
            ],
            "offset": 0,
            "limit": max_results,
            "sort_field": "project_start_date",
            "sort_order": "desc"
        }
        
        try:
            time.sleep(1)
            response = requests.post(
                self.API_URL,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            total = data.get("meta", {}).get("total", 0)
            
            print(f"[NIH] Found {total} total grants, fetched {len(results)}")
            return results
            
        except Exception as e:
            print(f"[NIH] Search error: {e}")
            return []
    
    def _extract_lead(self, grant):
        """Extract lead from grant record"""
        
        # Get PI name
        name = grant.get("contact_pi_name", "")
        
        if not name:
            pis = grant.get("principal_investigators", [])
            if pis:
                pi = pis[0]
                first = pi.get("first_name", "")
                last = pi.get("last_name", "")
                name = f"{first} {last}".strip()
        
        if not name:
            return None
        
        # Organization info
        company = grant.get("org_name", "Unknown")
        city = grant.get("org_city", "")
        state = grant.get("org_state", "")
        country = grant.get("org_country", "USA")
        
        person_location = f"{city}, {state}".strip(", ")
        company_hq = f"{city}, {state}, {country}".strip(", ")
        
        # Project info
        project_title = grant.get("project_title", "")
        
        # Year
        start_date = grant.get("project_start_date", "")
        year = ""
        if start_date:
            try:
                year = start_date.split("-")[0] if "-" in start_date else start_date[:4]
            except:
                pass
        
        # Check for in-vitro
        terms = grant.get("terms", "") or ""
        full_text = f"{project_title} {terms}".lower()
        invitro_keywords = ["3d", "in vitro", "organ-on-chip", "spheroid", "organoid"]
        uses_invitro = any(kw in full_text for kw in invitro_keywords)
        
        return {
            "name": name.strip(),
            "title": "Principal Investigator",
            "company": company,
            "person_location": person_location,
            "company_hq": company_hq,
            "funding_stage": "NIH Grant",
            "publication_topic": project_title[:200],
            "publication_year": year,
            "uses_invitro": "Yes" if uses_invitro else "No",
            "email": "",
            "work_mode": "Unknown",
            "company_in_hub": "",
            "source": "NIH RePORTER"
        }
    
    def crawl(self, keywords, max_results=50):
        """Main crawl method"""
        
        # Build query
        query = " OR ".join([f'"{kw}"' for kw in keywords[:5]])
        
        # Search
        results = self.search(query, max_results)
        
        # Extract leads
        self.leads = []
        for grant in results:
            lead = self._extract_lead(grant)
            if lead:
                self.leads.append(lead)
        
        print(f"[NIH] ✓ Extracted {len(self.leads)} leads")
        return self.leads


# Test
if __name__ == "__main__":
    crawler = NIHReporterCrawler()
    keywords = ["drug-induced liver injury", "hepatotoxicity"]
    leads = crawler.crawl(keywords, max_results=10)
    
    print(f"\nFound {len(leads)} leads:")
    for lead in leads[:3]:
        print(f"  - {lead['name']} at {lead['company']}")