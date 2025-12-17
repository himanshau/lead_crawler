from datetime import datetime

class ProbabilityEngine:
    def __init__(self):
        self.current_year = datetime.now().year
        
        self.weights = {
            "title_match": 30,
            "funding_stage": 20,
            "uses_invitro": 15,
            "location_hub": 10,
            "recent_dili_publication": 40
        }
        
        self.title_keywords = [
            "director", "vp", "vice president", "head", "chief",
            "senior", "principal", "lead", "manager"
        ]
        
        self.role_keywords = [
            "toxicology", "toxicologist", "safety", "hepatic",
            "preclinical", "liver", "dmpk", "adme"
        ]
        
        self.hub_locations = [
            "boston", "cambridge", "massachusetts",
            "san francisco", "bay area", "palo alto",
            "san diego", "la jolla",
            "basel", "zurich", "switzerland",
            "london", "oxford", "uk",
            "munich", "germany",
            "new jersey", "princeton",
            "maryland", "bethesda"
        ]
        
        self.dili_keywords = [
            "drug-induced liver injury", "drug induced liver injury",
            "dili", "hepatotoxicity", "liver toxicity", "hepatic toxicity",
            "liver injury"
        ]
    
    def _score_title(self, title):
        if not title:
            return 0
        
        title_lower = title.lower()
        score = 0
        
        has_senior_title = any(kw in title_lower for kw in self.title_keywords)
        has_relevant_role = any(kw in title_lower for kw in self.role_keywords)
        
        if has_senior_title and has_relevant_role:
            score = self.weights["title_match"]
        elif has_relevant_role:
            score = int(self.weights["title_match"] * 0.6)
        elif has_senior_title:
            score = int(self.weights["title_match"] * 0.3)
        
        return score
    
    def _score_funding(self, funding_stage):
        if not funding_stage:
            return 0
        
        funding_lower = funding_stage.lower()
        
        if any(f in funding_lower for f in ["series a", "series b", "series c"]):
            return self.weights["funding_stage"]
        
        if any(f in funding_lower for f in ["grant", "nih", "funded", "clinical trial"]):
            return int(self.weights["funding_stage"] * 0.8)
        
        if any(f in funding_lower for f in ["seed", "private"]):
            return int(self.weights["funding_stage"] * 0.4)
        
        return 0
    
    def _score_technology(self, uses_invitro, topic=""):
        score = 0
        
        if str(uses_invitro).lower() == "yes":
            score = self.weights["uses_invitro"]
        
        if topic:
            topic_lower = topic.lower()
            tech_keywords = ["3d", "in vitro", "organ-on-chip", "spheroid", "organoid"]
            if any(kw in topic_lower for kw in tech_keywords):
                score = max(score, self.weights["uses_invitro"])
        
        return score
    
    def _score_location(self, person_location, company_hq):
        locations = f"{person_location} {company_hq}".lower()
        
        if any(hub in locations for hub in self.hub_locations):
            return self.weights["location_hub"]
        
        return 0
    
    def _score_publication(self, topic, year):
        if not topic:
            return 0
        
        topic_lower = topic.lower()
        
        try:
            pub_year = int(year) if year else 0
        except:
            pub_year = 0
        
        is_recent = pub_year >= self.current_year - 2
        
        has_dili = any(kw in topic_lower for kw in self.dili_keywords)
        
        if is_recent and has_dili:
            return self.weights["recent_dili_publication"]
        
        has_liver = any(kw in topic_lower for kw in ["liver", "hepat", "toxicol"])
        
        if is_recent and has_liver:
            return int(self.weights["recent_dili_publication"] * 0.5)
        
        if has_dili or has_liver:
            return int(self.weights["recent_dili_publication"] * 0.25)
        
        return 0
    
    def calculate_score(self, lead):
        score = 0
        
        score += self._score_title(lead.get("title", ""))
        score += self._score_funding(lead.get("funding_stage", ""))
        score += self._score_technology(
            lead.get("uses_invitro", "No"),
            lead.get("publication_topic", "")
        )
        score += self._score_location(
            lead.get("person_location", ""),
            lead.get("company_hq", "")
        )
        score += self._score_publication(
            lead.get("publication_topic", ""),
            lead.get("publication_year", "")
        )
        
        return min(score, 100)
    
    def score_leads(self, leads):
        print("\n[Scoring] Calculating probability scores...")
        
        for lead in leads:
            lead["probability_score"] = self.calculate_score(lead)
        
        leads.sort(key=lambda x: x["probability_score"], reverse=True)
        
        for i, lead in enumerate(leads, 1):
            lead["rank"] = i
        
        for lead in leads:
            locations = f"{lead.get('person_location', '')} {lead.get('company_hq', '')}".lower()
            lead["company_in_hub"] = "TRUE" if any(hub in locations for hub in self.hub_locations) else "FALSE"
        
        scores = [l["probability_score"] for l in leads]
        if scores:
            avg = sum(scores) / len(scores)
            high_quality = sum(1 for s in scores if s >= 70)
            print(f"[Scoring] ✓ Scored {len(leads)} leads")
            print(f"[Scoring]   Average score: {avg:.1f}")
            print(f"[Scoring]   High-quality (≥70): {high_quality}")
        
        return leads