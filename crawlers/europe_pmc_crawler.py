import requests
from datetime import datetime
import time
import re

class EuropePMCCrawler:
    API_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    
    def __init__(self):
        self.leads = []
    
    def search(self, query, max_results=50):
        print(f"[Europe PMC] Searching: {query[:80]}...")
        
        params = {
            "query": query,
            "resultType": "core",
            "pageSize": min(max_results, 100),
            "format": "json",
            "sort": "P_PDATE_D desc"
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
            
            results = data.get("resultList", {}).get("result", [])
            hit_count = data.get("hitCount", 0)
            
            print(f"[Europe PMC] Found {hit_count} total, fetched {len(results)}")
            return results
            
        except Exception as e:
            print(f"[Europe PMC] Search error: {e}")
            return []
    
    def _extract_lead(self, article):
        authors = article.get("authorList", {}).get("author", [])
        if not authors:
            return None
        
        author = authors[0]
        for a in authors:
            if a.get("authorId"):
                author = a
                break
        
        first_name = author.get("firstName", "")
        last_name = author.get("lastName", "")
        name = f"{first_name} {last_name}".strip()
        
        if not name:
            name = author.get("fullName", "")
        
        if not name:
            return None
        
        affiliation = ""
        aff_list = author.get("affiliation", "")
        if isinstance(aff_list, str):
            affiliation = aff_list
        elif isinstance(aff_list, list) and aff_list:
            affiliation = aff_list[0] if isinstance(aff_list[0], str) else ""
        
        company, person_location, company_hq = self._parse_affiliation(affiliation)
        
        title = article.get("title", "")
        year = article.get("pubYear", "")
        
        abstract = article.get("abstractText", "") or ""
        full_text = f"{title} {abstract}".lower()
        invitro_keywords = ["3d", "in vitro", "organ-on-chip", "spheroid", "organoid"]
        uses_invitro = any(kw in full_text for kw in invitro_keywords)
        
        return {
            "name": name.strip(),
            "title": "Researcher / Author",
            "company": company,
            "person_location": person_location,
            "company_hq": company_hq,
            "funding_stage": "Unknown",
            "publication_topic": title[:200],
            "publication_year": year,
            "uses_invitro": "Yes" if uses_invitro else "No",
            "email": "",
            "work_mode": "Unknown",
            "company_in_hub": "",
            "source": "Europe PMC"
        }
    
    def _parse_affiliation(self, affiliation):
        if not affiliation:
            return "Unknown", "", ""
        
        parts = [p.strip() for p in affiliation.split(",") if p.strip()]
        
        if len(parts) >= 3:
            company = parts[0]
            person_location = parts[-2]
            company_hq = parts[-1]
        elif len(parts) == 2:
            company = parts[0]
            person_location = parts[1]
            company_hq = parts[1]
        else:
            company = affiliation[:100]
            person_location = ""
            company_hq = ""
        
        return company[:100], person_location, company_hq
    
    def crawl(self, keywords, max_results=50):
        query_parts = [f'"{kw}"' for kw in keywords[:5]]
        query = " OR ".join(query_parts)
        
        current_year = datetime.now().year
        query += f" AND (PUB_YEAR:[{current_year-2} TO {current_year}])"
        
        results = self.search(query, max_results)
        
        self.leads = []
        for article in results:
            lead = self._extract_lead(article)
            if lead:
                self.leads.append(lead)
        
        print(f"[Europe PMC] ✓ Extracted {len(self.leads)} leads")
        return self.leads