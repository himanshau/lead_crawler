import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import re

class PubMedCrawler:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    def __init__(self, email="student@university.edu"):
        self.email = email
        self.leads = []
    
    def search(self, query, max_results=50):
        print(f"[PubMed] Searching: {query[:80]}...")
        
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email,
            "sort": "date"
        }
        
        try:
            time.sleep(1)  # Be nice to the server
            response = requests.get(
                self.BASE_URL + "esearch.fcgi",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            print(f"[PubMed] Found {len(id_list)} articles")
            return id_list
        except Exception as e:
            print(f"[PubMed] Search error: {e}")
            return []
    
    def fetch_details(self, id_list):
        if not id_list:
            return []
        
        print(f"[PubMed] Fetching {len(id_list)} article details...")
        
        # Batch into groups of 50 to avoid timeout
        all_leads = []
        batch_size = 50
        
        for i in range(0, len(id_list), batch_size):
            batch = id_list[i:i + batch_size]
            
            params = {
                "db": "pubmed",
                "id": ",".join(batch),
                "retmode": "xml",
                "email": self.email
            }
            
            try:
                time.sleep(1)
                response = requests.get(
                    self.BASE_URL + "efetch.fcgi",
                    params=params,
                    timeout=60
                )
                response.raise_for_status()
                leads = self._parse_xml(response.text)
                all_leads.extend(leads)
                print(f"[PubMed] Processed batch {i//batch_size + 1}, total leads: {len(all_leads)}")
            except Exception as e:
                print(f"[PubMed] Fetch error: {e}")
        
        return all_leads
    
    def _parse_xml(self, xml_text):
        """Parse PubMed XML and extract author information"""
        leads = []
        
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            print(f"[PubMed] XML parse error: {e}")
            return []
        
        for article in root.findall(".//PubmedArticle"):
            lead = self._extract_lead(article)
            if lead:
                leads.append(lead)
        
        return leads
    
    def _extract_lead(self, article):
        """Extract lead info from single article"""
        
        # Article title
        title = article.findtext(".//ArticleTitle", default="")
        
        # Publication year
        year = self._get_year(article)
        
        # Get corresponding/first author
        authors = article.findall(".//Author")
        if not authors:
            return None
        
        # Try to find author with affiliation (often corresponding author)
        chosen_author = None
        author_email = ""
        affiliation = ""
        
        for author in authors:
            aff_info = author.find(".//AffiliationInfo")
            if aff_info is not None:
                aff_text = aff_info.findtext("Affiliation", default="")
                if aff_text:
                    chosen_author = author
                    affiliation = aff_text
                    # Try to extract email from affiliation
                    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', aff_text)
                    if email_match:
                        author_email = email_match.group()
                    break
        
        if not chosen_author:
            chosen_author = authors[0]
            aff_info = chosen_author.find(".//AffiliationInfo")
            if aff_info is not None:
                affiliation = aff_info.findtext("Affiliation", default="")
        
        # Get name
        last_name = chosen_author.findtext("LastName", default="")
        fore_name = chosen_author.findtext("ForeName", default="")
        name = f"{fore_name} {last_name}".strip()
        
        if not name:
            name = chosen_author.findtext("CollectiveName", default="")
        
        if not name:
            return None
        
        # Parse affiliation for company and location
        company, person_location, company_hq = self._parse_affiliation(affiliation)
        
        # Check for in-vitro keywords
        uses_invitro = self._check_invitro(title + " " + affiliation)
        
        return {
            "name": name.strip(),
            "title": "Researcher / Author",
            "company": company,
            "person_location": person_location,
            "company_hq": company_hq,
            "funding_stage": "Unknown",
            "publication_topic": title[:200],  # Truncate long titles
            "publication_year": year,
            "uses_invitro": "Yes" if uses_invitro else "No",
            "email": author_email,
            "work_mode": "Unknown",
            "company_in_hub": "",
            "source": "PubMed"
        }
    
    def _get_year(self, article):
        """Extract publication year"""
        pub_date = article.find(".//PubDate")
        if pub_date is not None:
            year = pub_date.findtext("Year")
            if year:
                return year
            medline = pub_date.findtext("MedlineDate", default="")
            if medline:
                return medline[:4]
        return ""
    
    def _parse_affiliation(self, affiliation):
        """Parse affiliation string into company, location"""
        if not affiliation:
            return "Unknown", "", ""
        
        # Split by comma
        parts = [p.strip() for p in affiliation.split(",") if p.strip()]
        
        if len(parts) >= 3:
            company = parts[0]
            person_location = parts[-2]
            company_hq = parts[-1]
        elif len(parts) == 2:
            company = parts[0]
            person_location = parts[1]
            company_hq = parts[1]
        elif len(parts) == 1:
            company = parts[0]
            person_location = ""
            company_hq = ""
        else:
            company = affiliation[:100]
            person_location = ""
            company_hq = ""
        
        # Clean up
        company = company[:100]  # Truncate long company names
        
        return company, person_location, company_hq
    
    def _check_invitro(self, text):
        """Check if text mentions in-vitro/3D methods"""
        if not text:
            return False
        text_lower = text.lower()
        keywords = ["3d", "in vitro", "in-vitro", "organ-on-chip",
                   "spheroid", "organoid", "microphysiological"]
        return any(kw in text_lower for kw in keywords)
    
    def crawl(self, keywords, max_results=50):
        """Main crawl method"""
        
        # Build search query
        query_parts = [f'"{kw}"[Title/Abstract]' for kw in keywords[:5]]  # Limit keywords
        query = " OR ".join(query_parts)
        
        # Add date filter (last 3 years)
        current_year = datetime.now().year
        query += f" AND {current_year-2}:{current_year}[pdat]"
        
        # Search and fetch
        id_list = self.search(query, max_results)
        self.leads = self.fetch_details(id_list)
        
        print(f"[PubMed] ✓ Extracted {len(self.leads)} leads")
        return self.leads


# Test
if __name__ == "__main__":
    crawler = PubMedCrawler(email="test@test.com")
    keywords = ["drug-induced liver injury", "hepatotoxicity in vitro"]
    leads = crawler.crawl(keywords, max_results=10)
    
    print(f"\nFound {len(leads)} leads:")
    for lead in leads[:3]:
        print(f"  - {lead['name']} at {lead['company']}")