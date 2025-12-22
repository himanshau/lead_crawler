# Assignment: 3D In-Vitro Lead Generator

## 📌 Assignment Overview

This assignment involves building a **lead generation system** for researchers working on **3D in-vitro models** and **drug-induced liver injury (DILI)** research. The system crawls multiple scientific databases to find and score potential research leads based on their relevance to the field.

## 🎯 Assignment Objectives

### Primary Objective
Develop a Python-based web scraping and data analysis tool that automatically:
1. **Crawls** multiple scientific data sources
2. **Extracts** relevant researcher and publication information
3. **Scores** leads based on relevance criteria
4. **Generates** contact information (emails)
5. **Exports** results in usable formats (CSV and Excel)

### Learning Outcomes
Upon completing this assignment, you will have demonstrated ability to:
- Build multi-source web scrapers using Python
- Work with REST APIs and HTML parsing
- Implement data cleaning and deduplication
- Design scoring algorithms
- Generate structured data outputs
- Handle errors and rate limiting in web scraping

## 🏗️ Assignment Components

### 1. Web Crawlers (5 sources)

#### a) **PubMed Crawler** (`crawlers/pubmed_crawler.py`)
- **Purpose**: Search scientific publications from PubMed database
- **Technology**: Uses NCBI E-utilities API
- **Data Extracted**: Author names, affiliations, publication titles, years
- **Challenge**: Requires email for API access, XML parsing

#### b) **NIH RePORTER Crawler** (`crawlers/nih_crawler.py`)
- **Purpose**: Find research grant information from NIH
- **Technology**: REST API calls
- **Data Extracted**: Principal investigators, institutions, grant funding
- **Challenge**: Complex JSON structure, pagination handling

#### c) **Europe PMC Crawler** (`crawlers/europe_pmc_crawler.py`)
- **Purpose**: Search European scientific publications
- **Technology**: Europe PMC REST API
- **Data Extracted**: Authors, affiliations, publication metadata
- **Challenge**: Different data format than PubMed

#### d) **ClinicalTrials.gov Crawler** (`crawlers/clinical_trials_crawler.py`)
- **Purpose**: Find clinical trials related to liver research
- **Technology**: ClinicalTrials.gov API
- **Data Extracted**: Investigators, locations, study information
- **Challenge**: Nested JSON structures

#### e) **Google Scholar Crawler** (`crawlers/google_scholar_crawler.py`)
- **Purpose**: Search academic papers from Google Scholar
- **Technology**: scholarly library
- **Data Extracted**: Authors, citations, publication info
- **Challenge**: May be blocked/rate-limited (optional source)

### 2. Email Generator (`crawlers/email_generator.py`)
- **Purpose**: Generate probable email addresses for leads
- **Method**: Pattern-based email construction using:
  - Name + company domain
  - Common email formats (firstname.lastname@domain, etc.)
- **Challenge**: Domain extraction from company names

### 3. Probability Scoring Engine (`scoring/probability_engine.py`)
- **Purpose**: Score and rank leads based on relevance
- **Scoring Factors** (configurable weights in `config.py`):
  - **Title Match** (30%): Job title contains relevant keywords
  - **Funding Stage** (20%): Has active research funding
  - **Uses In-Vitro** (15%): Explicitly mentions in-vitro methods
  - **Location Hub** (10%): Based in major research hub
  - **Recent DILI Publication** (40%): Recent relevant publications
- **Output**: Probability score (0-100) and ranking

### 4. Data Processing Pipeline
The main workflow (`main.py`) orchestrates:
1. **Collection**: Gather data from all sources
2. **Deduplication**: Remove duplicate entries by name+company
3. **Enrichment**: Add email addresses
4. **Scoring**: Calculate probability scores
5. **Ranking**: Sort by score (highest to lowest)
6. **Export**: Save to CSV and Excel

## ⚙️ Configuration (`config.py`)

### Key Configuration Parameters:
```python
YOUR_EMAIL                 # Required for PubMed API
MAX_RESULTS_PER_SOURCE     # Default: 50
REQUEST_DELAY              # Delay between requests (2 seconds)
RESEARCH_KEYWORDS          # Keywords to search for
TITLE_KEYWORDS             # Keywords for job title matching
HUB_LOCATIONS              # Research hub locations
SCORING_WEIGHTS            # Weights for scoring algorithm
```

## 📊 Expected Output

### Output Files (in `output/` directory):
1. **CSV File**: `3d_invitro_leads_YYYYMMDD_HHMMSS.csv`
2. **Excel File**: `3d_invitro_leads_YYYYMMDD_HHMMSS.xlsx`

### Output Columns:
| Column | Description | Example |
|--------|-------------|---------|
| `name` | Researcher name | "Dr. Jane Smith" |
| `title` | Job title | "Principal Investigator" |
| `company` | Institution | "Harvard Medical School" |
| `person_location` | Location | "Boston, MA" |
| `company_hq` | HQ location | "Cambridge, MA" |
| `funding_stage` | Grant info | "NIH R01 Grant" |
| `publication_topic` | Research topic | "3D Hepatic Models for DILI" |
| `publication_year` | Year | "2024" |
| `uses_invitro` | Uses in-vitro | "Yes" |
| `email` | Generated email | "jane.smith@harvard.edu" |
| `work_mode` | Work type | "Academic" |
| `company_in_hub` | In research hub | "Yes" |
| `probability_score` | Score (0-100) | 85 |
| `rank` | Ranking | 1 |

## 🚀 How to Run the Assignment

### Setup:
```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Running:
```bash
# Basic run (50 results per source)
python main.py

# Custom run (100 results, skip Google Scholar)
python main.py --max-results 100 --skip-scholar

# Custom output name
python main.py --output-name my_custom_leads
```

### Command Line Arguments:
- `--max-results N`: Maximum results per source (default: 50)
- `--skip-scholar`: Skip Google Scholar (recommended for speed)
- `--output-name NAME`: Custom output filename

## 🔍 Assignment Requirements Checklist

### Functional Requirements:
- ✅ Crawl at least 4 scientific data sources
- ✅ Extract researcher and publication information
- ✅ Generate probable email addresses
- ✅ Implement lead scoring algorithm
- ✅ Remove duplicate entries
- ✅ Export to CSV and Excel formats
- ✅ Handle errors gracefully
- ✅ Respect API rate limits

### Technical Requirements:
- ✅ Python 3.8+
- ✅ Use `requests` for HTTP calls
- ✅ Use `BeautifulSoup` for HTML parsing
- ✅ Use `pandas` for data manipulation
- ✅ Implement proper error handling
- ✅ Add progress indicators
- ✅ No API keys required (except email for PubMed)

### Code Quality:
- ✅ Modular design (separate crawlers)
- ✅ Configuration file for easy customization
- ✅ Clear function and variable names
- ✅ Comments where necessary
- ✅ Consistent code style

## 📚 Dependencies

```
pandas          # Data manipulation
requests        # HTTP requests
beautifulsoup4  # HTML parsing
lxml           # XML/HTML processing
openpyxl       # Excel writing
xlsxwriter     # Excel formatting
tqdm           # Progress bars
fake-useragent # User agent rotation
scholarly      # Google Scholar API
```

## 🎓 Key Concepts Demonstrated

### 1. Web Scraping
- API integration (REST APIs)
- HTML parsing with BeautifulSoup
- XML processing
- Rate limiting and delays
- User agent rotation

### 2. Data Processing
- Data cleaning
- Deduplication algorithms
- Data normalization
- DataFrame operations with pandas

### 3. Algorithm Design
- Weighted scoring system
- Pattern matching
- Email generation logic
- Ranking algorithms

### 4. Software Engineering
- Modular design
- Error handling
- Configuration management
- Command-line interfaces
- File I/O operations

## ⚠️ Important Notes

### Ethical Considerations:
- **Rate Limiting**: Implements delays to avoid overwhelming servers
- **User Agents**: Rotates user agents for responsible scraping
- **Public Data Only**: Only accesses publicly available information
- **No Authentication Bypass**: Doesn't attempt to bypass any security

### Limitations:
- **Google Scholar**: May be blocked or rate-limited
- **Email Accuracy**: Generated emails are probabilistic, not verified
- **Data Freshness**: Results depend on source availability
- **Internet Required**: Needs active internet connection

## 📈 Evaluation Criteria

### Functionality (40%)
- Does it successfully crawl all sources?
- Are duplicates properly removed?
- Is the scoring algorithm working correctly?
- Are outputs properly formatted?

### Code Quality (30%)
- Is the code modular and well-organized?
- Are there proper error handlers?
- Is the code readable and maintainable?

### Documentation (15%)
- Is the README clear and complete?
- Are functions documented?
- Are configuration options explained?

### Innovation (15%)
- Scoring algorithm design
- Email generation strategy
- Additional features or improvements

## 🔧 Customization Ideas

### Possible Extensions:
1. **Add More Sources**: bioRxiv, medRxiv, ResearchGate
2. **Email Verification**: Check if generated emails exist
3. **Machine Learning**: Train ML model for better scoring
4. **Web Interface**: Add Flask/Django web UI
5. **Database Storage**: Store results in SQLite/PostgreSQL
6. **Real-time Updates**: Monitor sources for new publications
7. **Network Analysis**: Visualize researcher collaborations
8. **API Development**: Create REST API for the tool

## 💡 Troubleshooting

### Common Issues:

**Issue**: No results returned
- **Solution**: Check internet connection, verify keywords in `config.py`

**Issue**: Google Scholar blocking requests
- **Solution**: Use `--skip-scholar` flag

**Issue**: "No module named..." error
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Rate limiting errors
- **Solution**: Increase `REQUEST_DELAY` in `config.py`

## 📖 Additional Resources

### APIs Used:
- [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [NIH RePORTER API](https://api.reporter.nih.gov/)
- [Europe PMC REST API](https://europepmc.org/RestfulWebService)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/api/gui)

### Python Libraries:
- [Requests Documentation](https://docs.python-requests.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 📝 Summary

This assignment combines **web scraping**, **data processing**, **algorithm design**, and **software engineering** to create a practical tool for scientific lead generation. It demonstrates the ability to:
- Work with multiple APIs and data sources
- Process and clean real-world data
- Implement business logic (scoring)
- Create user-friendly outputs
- Write maintainable, modular code

The final product is a **production-ready tool** that could be used by pharmaceutical companies, research institutions, or biotech startups to identify potential research collaborators or business leads in the 3D in-vitro and DILI research space.

---

**Good luck with the assignment! 🔬🧬**
