# System Patterns

## Architecture

### Current Structure
```
automations/
├── memory-bank/       # Project documentation
├── jobs/              # Job search automation
│   ├── jobs.py       # Main script
│   ├── run_job_search.sh  # Cron wrapper
│   ├── requirements.txt
│   ├── sent_jobs.json     # State tracking
│   └── logs/              # Execution logs
└── [future automations]/
```

### Design Patterns

**State Management**
- JSON files for simple state persistence
- `sent_jobs.json` tracks processed items
- No database needed for current scale

**Scraping Pattern**
- Platform-specific search functions (Indeed, LinkedIn)
- BeautifulSoup for HTML parsing
- Respectful delays between requests (2-3 seconds)
- Graceful error handling per job card

**Scoring Algorithm**
- Required skills: 10 points each
- Nice-to-have skills: 5 points each
- Leadership keywords: 3 points each
- Capped at 100 points
- Thresholds: 70+ excellent, 40-69 good, <40 potential

**Email Generation**
- HTML templates with inline CSS
- Color-coded match scores
- Sorted by relevance (highest match first)
- Only send if new jobs found

## Key Technical Decisions

1. **No API Keys for Job Boards**
   - LinkedIn and Indeed APIs are paid/restricted
   - Web scraping is legal for public job postings
   - Respectful rate limiting to avoid blocks

2. **SendGrid Over SMTP**
   - Better deliverability
   - Free tier sufficient (100 emails/day)
   - HTML email support out of the box

3. **Cron Over Task Scheduler**
   - Simple, built-in to macOS
   - Reliable for 2x daily schedule
   - Easy to debug with shell wrapper

4. **Monorepo for Automations**
   - Each automation is self-contained
   - Shared patterns emerge organically
   - Easy to add/remove automations

5. **Environment Variables for Secrets**
   - Sensitive data in .env file (gitignored)
   - Fallback values for development
   - Clear separation of config and code

## Component Relationships

```
Cron → run_job_search.sh → jobs.py
                             ├── search_indeed()
                             ├── search_linkedin()
                             ├── calculate_match_score()
                             └── send_email() → SendGrid API
```

## Error Handling Strategy
- Try/except around each job board scraper
- Continue on individual job card failures
- Log all errors to timestamped log files
- Email only sent if ≥1 job found successfully


