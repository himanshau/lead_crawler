import re

class EmailGenerator:
    PATTERNS = [
        "{first}.{last}@{domain}",
        "{first}{last}@{domain}",
        "{f}{last}@{domain}",
        "{first}_{last}@{domain}",
        "{first}@{domain}",
        "{f}.{last}@{domain}"
    ]
    
    KNOWN_DOMAINS = {
        "pfizer": "pfizer.com",
        "novartis": "novartis.com",
        "roche": "roche.com",
        "merck": "merck.com",
        "johnson": "jnj.com",
        "astrazeneca": "astrazeneca.com",
        "gsk": "gsk.com",
        "glaxosmithkline": "gsk.com",
        "sanofi": "sanofi.com",
        "abbvie": "abbvie.com",
        "bristol": "bms.com",
        "lilly": "lilly.com",
        "eli lilly": "lilly.com",
        "amgen": "amgen.com",
        "gilead": "gilead.com",
        "biogen": "biogen.com",
        "regeneron": "regeneron.com",
        "moderna": "modernatx.com",
        "biontech": "biontech.de",
        "takeda": "takeda.com",
        "boehringer": "boehringer-ingelheim.com",
        "harvard": "harvard.edu",
        "mit": "mit.edu",
        "stanford": "stanford.edu",
        "yale": "yale.edu",
        "columbia": "columbia.edu",
        "johns hopkins": "jhu.edu",
        "nih": "nih.gov",
        "fda": "fda.hhs.gov",
        "emulate": "emulatebio.com",
        "organovo": "organovo.com",
        "insphero": "insphero.com"
    }
    
    UNIVERSITY_PATTERNS = [
        (r"university of (\w+)", "{}.edu"),
        (r"(\w+) university", "{}.edu"),
        (r"(\w+) college", "{}.edu"),
        (r"(\w+) institute", "{}.edu")
    ]
    
    def __init__(self):
        pass
    
    def _parse_name(self, name):
        if not name:
            return None, None
        
        name = name.lower()
        for title in ["dr.", "dr", "prof.", "prof", "mr.", "mrs.", "ms.", "phd", "md"]:
            name = name.replace(title, "")
        
        name = name.strip()
        parts = name.split()
        
        if len(parts) < 2:
            return None, None
        
        first = parts[0]
        last = parts[-1]
        
        first = re.sub(r'[^a-z]', '', first)
        last = re.sub(r'[^a-z]', '', last)
        
        return first, last
    
    def _get_domain(self, company):
        if not company:
            return None
        
        company_lower = company.lower()
        
        for key, domain in self.KNOWN_DOMAINS.items():
            if key in company_lower:
                return domain
        
        for pattern, domain_format in self.UNIVERSITY_PATTERNS:
            match = re.search(pattern, company_lower)
            if match:
                uni_name = match.group(1)
                return domain_format.format(uni_name)
        
        words = company_lower.split()
        if words:
            base = re.sub(r'[^a-z0-9]', '', words[0])
            if len(base) >= 3:
                return f"{base}.com"
        
        return None
    
    def generate_email(self, name, company, existing_email=""):
        if existing_email and "@" in existing_email:
            return existing_email
        
        first, last = self._parse_name(name)
        if not first or not last:
            return ""
        
        domain = self._get_domain(company)
        if not domain:
            return ""
        
        email = f"{first}.{last}@{domain}"
        
        return email
    
    def enrich_leads(self, leads):
        print("\n[Email] Generating email addresses...")
        
        generated = 0
        for lead in leads:
            if not lead.get("email"):
                email = self.generate_email(
                    lead.get("name", ""),
                    lead.get("company", "")
                )
                if email:
                    lead["email"] = email
                    generated += 1
        
        print(f"[Email] ✓ Generated {generated} email addresses")
        return leads