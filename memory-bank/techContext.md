# Tech Context

## Technology Stack

### Language & Runtime
- **Python 3.12** - Primary language
- **Virtual Environment** - Isolated dependencies in `venv/`

### Core Dependencies
```python
beautifulsoup4==4.14.2  # HTML parsing
requests==2.32.5         # HTTP requests
sendgrid==6.12.5         # Email service
```

### Supporting Libraries
- `soupsieve` - CSS selector support for BeautifulSoup
- `urllib3` - URL handling
- `cryptography` - SSL/TLS for HTTPS

## Development Setup

### Prerequisites
- macOS (Darwin 25.0.0)
- Python 3.12+
- SendGrid account (free tier)
- Verified sender email in SendGrid

### Installation
```bash
cd /Users/bisikennadi/Projects/automations/jobs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration
1. Get SendGrid API key from https://sendgrid.com
2. Verify sender email in SendGrid dashboard
3. Copy `.env.example` to `.env`
4. Update `.env` with your API key and email addresses
5. Customize job search parameters in `jobs.py` (lines 29-51)

### Running Locally
```bash
cd /Users/bisikennadi/Projects/automations/jobs
source venv/bin/activate
python3 jobs.py
# Or use the shell wrapper:
./run_job_search.sh
```

### Setting Up Cron
```bash
crontab -e
# Add:
0 9 * * * /Users/bisikennadi/Projects/automations/jobs/run_job_search.sh
0 18 * * * /Users/bisikennadi/Projects/automations/jobs/run_job_search.sh
```

## Technical Constraints

### Rate Limiting
- 2-3 second delays between requests
- Max 10 jobs per search per platform
- Respectful scraping practices

### Service Limits
- **SendGrid**: 100 emails/day (free tier)
- **Job Boards**: No official rate limits (web scraping)
- **Current Usage**: ~2 emails/day (well within limits)

### Security Considerations
- ✅ API key in environment variable (.env)
- ✅ .env file in .gitignore
- Verified sender email required
- No password/auth for job boards (public data)

## Monitoring & Logs
- Logs: `jobs/logs/job_search_YYYYMMDD_HHMMSS.log`
- State: `jobs/sent_jobs.json` (last 1000 job IDs)
- Retention: Manual cleanup needed

## Known Issues
1. Web scraping is fragile - HTML structure changes break scrapers
2. LinkedIn may require login for some listings
3. Match scoring is basic keyword matching (no AI/NLP yet)
4. No alerting if script fails (check logs manually)


