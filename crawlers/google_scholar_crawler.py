"""
Google Scholar Crawler - FREE (with rate limiting)
Uses scholarly library to search Google Scholar
Note: Google may block if too many requests - use carefully
"""

import time

# Try to import scholarly, but handle if not installed
try:
    from scholarly import scholarly
    SCHOLARLY_AVAILABLE = True
except ImportError:
    SCHOLARLY_AVAILABLE = False
    print("[Google Scholar] scholarly library not installed. Run: pip install scholarly")

class GoogleScholarCrawler:
    """Crawls Google Scholar for authors (use sparingly - rate limited)"""
    
    def __init__(self):
        self.leads = []
    
    def search_authors(self, keywords, max_results=20):
        """Search for authors by keyword"""
        
        if not SCHOLARLY_AVAILABLE:
            print("[Google Scholar] Skipping - scholarly library not available")
            return []
        
        print(f"[Google Scholar] Searching for authors (this may be slow)...")
        
        leads = []
        
        try:
            # Search for publications first
            query = " ".join(keywords[:3])
            search_query = scholarly.search_pubs(query)
            
            count = 0
            for pub in search_query:
                if count >= max_results:
                    break
                
                time.sleep(3)  # Important: rate limiting to avoid being blocked
                
                try:
                    # Get publication details
                    bib = pub.get("bib", {})
                    
                    title = bib.get("title", "")
                    authors = bib.get("author", "")
                    year = bib.get("pub_year", "")
                    venue = bib.get("venue", "")
                    
                    # Get first author
                    if isinstance(authors, str):
                        author_list = [a.strip() for a in authors.split(" and ")]
                    elif isinstance(authors, list):
                        author_list = authors
                    else:
                        continue
                    
                    if not author_list:
                        continue
                    
                    name = author_list[0]
                    
                    # Check for in-vitro keywords
                    full_text = f"{title} {venue}".lower()
                    invitro_keywords = ["3d", "in vitro", "organ-on-chip", "spheroid"]
                    uses_invitro = any(kw in full_text for kw in invitro_keywords)
                    
                    lead = {
                        "name": name.strip(),
                        "title": "Researcher / Author",
                        "company": venue if venue else "Unknown",
                        "person_location": "",
                        "company_hq": "",
                        "funding_stage": "Unknown",
                        "publication_topic": title[:200],
                        "publication_year": str(year),
                        "uses_invitro": "Yes" if uses_invitro else "No",
                        "email": "",
                        "work_mode": "Unknown",
                        "company_in_hub": "",
                        "source": "Google Scholar"
                    }
                    leads.append(lead)
                    count += 1
                    print(f"[Google Scholar] Found: {name}")
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"[Google Scholar] Search error: {e}")
            print("[Google Scholar] This is normal - Google may be rate limiting")
        
        print(f"[Google Scholar] ✓ Extracted {len(leads)} leads")
        return leads
    
    def crawl(self, keywords, max_results=20):
        """Main crawl method"""
        self.leads = self.search_authors(keywords, max_results)
        return self.leads


# Test
if __name__ == "__main__":
    crawler = GoogleScholarCrawler()
    keywords = ["drug-induced liver injury", "hepatotoxicity"]
    leads = crawler.crawl(keywords, max_results=5)
    
    print(f"\nFound {len(leads)} leads:")
    for lead in leads[:3]:
        print(f"  - {lead['name']}")