"""
ClinicalTrials.gov Crawler - 100% FREE, NO API KEY REQUIRED
Finds researchers running clinical trials related to liver safety
"""

import requests
from datetime import datetime
import time

class ClinicalTrialsCrawler:
    """Crawls ClinicalTrials.gov for investigators"""
    
    API_URL = "https://clinicaltrials.gov/api/v2/studies"
    
    def __init__(self):
        self.leads = []
    
    def search(self, query, max_results=50):
        """Search ClinicalTrials.gov"""
        print(f"[ClinicalTrials] Searching: {query[:80]}...")
        
        params = {
            "query.term": query,
            "pageSize": min(max_results, 100),
            "format": "json",
            "fields": "NCTId,BriefTitle,OverallStatus,LeadSponsorName,LocationCity,LocationState,LocationCountry,ResponsiblePartyInvestigatorFullName,ResponsiblePartyInvestigatorAffiliation,StartDate,Condition,InterventionName"
        }
        
        try:
            time.sleep(1)
            response = requests.get(
                self.API_URL,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            studies = data.get("studies", [])
            print(f"[ClinicalTrials] Found {len(studies)} studies")
            return studies
            
        except Exception as e:
            print(f"[ClinicalTrials] Search error: {e}")
            return []
    
    def _extract_lead(self, study):
        """Extract lead from study"""
        
        protocol = study.get("protocolSection", {})
        
        # Get investigator info
        id_module = protocol.get("identificationModule", {})
        sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
        
        # Try to get responsible party investigator
        name = ""
        affiliation = ""
        
        # Check responsible party
        if "responsibleParty" in sponsor_module:
            resp = sponsor_module["responsibleParty"]
            name = resp.get("investigatorFullName", "")
            affiliation = resp.get("investigatorAffiliation", "")
        
        # If no investigator, use lead sponsor
        if not name:
            lead_sponsor = sponsor_module.get("leadSponsor", {})
            name = lead_sponsor.get("name", "")
            if name:
                affiliation = name  # Sponsor is the company
        
        if not name:
            return None
        
        # Location info
        locations_module = protocol.get("contactsLocationsModule", {})
        locations = locations_module.get("locations", [])
        
        person_location = ""
        company_hq = ""
        if locations:
            loc = locations[0]
            city = loc.get("city", "")
            state = loc.get("state", "")
            country = loc.get("country", "")
            person_location = f"{city}, {state}".strip(", ")
            company_hq = f"{city}, {state}, {country}".strip(", ")
        
        # Study info
        title = id_module.get("briefTitle", "")
        
        # Start date
        status_module = protocol.get("statusModule", {})
        start_date = status_module.get("startDateStruct", {}).get("date", "")
        year = start_date[:4] if start_date else ""
        
        # Check for in-vitro (rare in clinical trials, but check anyway)
        desc_module = protocol.get("descriptionModule", {})
        brief_summary = desc_module.get("briefSummary", "")
        full_text = f"{title} {brief_summary}".lower()
        invitro_keywords = ["3d", "in vitro", "organ-on-chip", "spheroid"]
        uses_invitro = any(kw in full_text for kw in invitro_keywords)
        
        # Check for liver/hepatic focus
        conditions = protocol.get("conditionsModule", {}).get("conditions", [])
        liver_related = any("liver" in c.lower() or "hepat" in c.lower() for c in conditions)
        
        return {
            "name": name.strip(),
            "title": "Clinical Investigator",
            "company": affiliation if affiliation else "Unknown",
            "person_location": person_location,
            "company_hq": company_hq,
            "funding_stage": "Clinical Trial",
            "publication_topic": title[:200],
            "publication_year": year,
            "uses_invitro": "Yes" if uses_invitro else ("Liver Focus" if liver_related else "No"),
            "email": "",
            "work_mode": "Unknown",
            "company_in_hub": "",
            "source": "ClinicalTrials.gov"
        }
    
    def crawl(self, keywords, max_results=50):
        """Main crawl method"""
        
        # Build query for liver/hepatic safety studies
        query = " OR ".join(keywords[:3])
        query += " AND (liver OR hepatic OR hepatotoxicity)"
        
        # Search
        results = self.search(query, max_results)
        
        # Extract leads
        self.leads = []
        for study in results:
            lead = self._extract_lead(study)
            if lead:
                self.leads.append(lead)
        
        print(f"[ClinicalTrials] ✓ Extracted {len(self.leads)} leads")
        return self.leads


# Test
if __name__ == "__main__":
    crawler = ClinicalTrialsCrawler()
    keywords = ["drug safety", "liver injury"]
    leads = crawler.crawl(keywords, max_results=10)
    
    print(f"\nFound {len(leads)} leads:")
    for lead in leads[:3]:
        print(f"  - {lead['name']} at {lead['company']}")