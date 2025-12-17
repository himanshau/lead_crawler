# 🔬 3D In-Vitro Lead Generator

A powerful Python-based web crawler that generates leads for 3D in-vitro models and drug-induced liver injury (DILI) research.

## 📋 Features

- **Multi-Source Crawling**: Scrapes data from 5 different scientific sources:
  - 📚 PubMed (Scientific Publications)
  - 💰 NIH RePORTER (Research Grants)
  - 🇪🇺 Europe PMC (European Publications)
  - 🏥 ClinicalTrials.gov (Clinical Trials)
  - 📖 Google Scholar (Academic Papers)

- **Email Generation**: Automatically generates probable email addresses for leads
- **Lead Scoring**: Uses a probability engine to score and rank leads based on relevance
- **Duplicate Removal**: Automatically removes duplicate entries
- **Multiple Output Formats**: Exports to both CSV and Excel formats

## 🏗️ Project Structure

```
lead_crawler/
├── main.py                 # Main entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── crawlers/              # Web crawlers for each source
│   ├── pubmed_crawler.py
│   ├── nih_crawler.py
│   ├── europe_pmc_crawler.py
│   ├── clinical_trials_crawler.py
│   ├── google_scholar_crawler.py
│   └── email_generator.py
├── scoring/               # Lead scoring system
│   └── probability_engine.py
└── output/                # Generated output files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or download the files):
   ```bash
   cd lead_crawler
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   
   - **Windows (Command Prompt)**:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Crawler

**Basic usage** (uses default settings):
```bash
python main.py
```

**With custom options**:
```bash
# Set maximum results per source (default: 50)
python main.py --max-results 100

# Skip Google Scholar (faster execution)
python main.py --skip-scholar

# Specify custom output filename
python main.py --output-name my_leads

# Combine multiple options
python main.py --max-results 75 --skip-scholar --output-name dili_leads
```

## ⚙️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-results` | Maximum results to fetch per source | 50 |
| `--skip-scholar` | Skip Google Scholar crawling (faster) | False |
| `--output-name` | Custom name for output files | Auto-generated with timestamp |

## 📊 Output

The crawler generates two output files in the `output/` directory:

- **CSV file**: `3d_invitro_leads_YYYYMMDD_HHMMSS.csv`
- **Excel file**: `3d_invitro_leads_YYYYMMDD_HHMMSS.xlsx`

### Output Columns

| Column | Description |
|--------|-------------|
| `name` | Researcher/Contact name |
| `title` | Job title or position |
| `company` | Organization/Institution |
| `person_location` | Location of the person |
| `company_hq` | Company headquarters location |
| `funding_stage` | Funding information |
| `publication_topic` | Research topic/publication title |
| `publication_year` | Year of publication |
| `uses_invitro` | Indicates if they use in-vitro methods |
| `email` | Generated email address |
| `work_mode` | Work mode/type |
| `company_in_hub` | Whether company is in a research hub |
| `probability_score` | Lead quality score (0-100) |
| `rank` | Ranking based on score |

## 🔧 Configuration

Edit `config.py` to customize:

- **YOUR_EMAIL**: Your email for API requests (required for PubMed)
- **RESEARCH_KEYWORDS**: Keywords to search for
- **TITLE_KEYWORDS**: Keywords to match in job titles
- **HUB_LOCATIONS**: Research hub locations to prioritize
- **SCORING_WEIGHTS**: Weights for lead scoring algorithm
- **REQUEST_DELAY**: Delay between requests (be respectful to APIs)

## 📝 Example

```bash
# Run with 30 results per source, skip Google Scholar
python main.py --max-results 30 --skip-scholar

# Expected output:
# ============================================================
# 🔬 3D IN-VITRO MODELS LEAD GENERATOR
#    Web Crawler - NO API KEYS REQUIRED
# ============================================================
# Start time: 2024-12-17 23:00:00
# Max results per source: 30
# ...
# ✅ COMPLETE!
# ============================================================
# Output files saved to: output/
#   - 3d_invitro_leads_20241217_230000.csv
#   - 3d_invitro_leads_20241217_230000.xlsx
```

## ⚠️ Notes

- **Rate Limiting**: The crawler includes delays between requests to respect API rate limits
- **Google Scholar**: May be slow or blocked; use `--skip-scholar` for faster execution
- **No API Keys**: All sources are accessed without requiring API keys
- **Internet Required**: Requires an active internet connection

## 📦 Dependencies

- `pandas` - Data manipulation and analysis
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML processing
- `openpyxl` - Excel file writing
- `xlsxwriter` - Excel file writing
- `tqdm` - Progress bars
- `fake-useragent` - User agent rotation
- `scholarly` - Google Scholar scraping

## 📄 License

This project is for educational and research purposes.

---

**Happy Lead Crawling! 🔬🧬**
