# Job Search Automation

Automated job search script that searches LinkedIn and Indeed for engineering leadership positions and sends **desktop notifications** with a beautiful HTML report.

## Features

- 🔍 Searches LinkedIn and Indeed for relevant jobs
- 🎯 Calculates match scores based on your skills and experience
- 🔔 **Sends desktop notifications** when new jobs are found
- 📄 **Creates beautiful HTML reports** for easy browsing
- 🚫 Prevents duplicate job notifications
- ⏰ Runs automatically via cronjob (twice daily)
- 📊 Keeps logs of all runs
- 🆓 **No email service needed** - completely free!

## Quick Start

### 1. Install Dependencies
```bash
cd jobs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test It
```bash
./run_job_search.sh
```

When jobs are found, you'll see:
- ✅ A desktop notification with top job matches
- 📂 An HTML file that automatically opens in your browser
- 📝 A log file with detailed search results

### 3. Set Up Cronjob (Optional - Automated Runs)
```bash
crontab -e
```

Add these lines (replace `$HOME/Projects/automations` with your actual project path):
```bash
# 9:00 AM daily
0 9 * * * $HOME/Projects/automations/jobs/run_job_search.sh

# 6:00 PM daily
0 18 * * * $HOME/Projects/automations/jobs/run_job_search.sh
```

**Note**: You can also use an absolute path. To find your project path, run:
```bash
cd jobs && pwd
```
Then replace `$HOME/Projects/automations` in the cronjob with the output.

## Files

- `jobs.py` - Main Python script
- `run_job_search.sh` - Shell wrapper for cronjob
- `requirements.txt` - Python dependencies
- `CRONJOB_SETUP.md` - Detailed cronjob setup instructions
- `sent_jobs.json` - Tracks sent jobs (auto-generated)
- `latest_jobs.html` - Most recent job listings (auto-generated)
- `logs/` - Execution logs (auto-generated)

## Configuration

Edit `jobs.py` to customize your search:

- **Job titles** (lines 36-41): Engineering leadership roles
- **Location** (line 34): Winter Springs, FL
- **Search radius** (line 35): 50 miles
- **Required skills** (lines 43-48): React, TypeScript, AI/ML, etc.
- **Nice-to-have skills** (lines 50-53): EdTech, Python, Cloud, etc.
- **Job type** (line 55): Remote, full-time, or contract
- **Date range** (line 56): Last 7 days

## How It Works

1. **Searches** LinkedIn and Indeed for your specified job titles
2. **Calculates** match scores based on your skills (0-100%)
3. **Filters** out jobs you've already been notified about
4. **Notifies** you via desktop notification (macOS)
5. **Creates** a beautiful HTML file with all job details
6. **Opens** the HTML file in your browser automatically
7. **Logs** everything for debugging

## Match Score System

- **🔥 Excellent Match (70%+)**: High concentration of your required skills
- **✓ Good Match (40-69%)**: Several relevant skills or keywords
- **• Potential Match (0-39%)**: Some relevant keywords

Jobs are ranked by match score, with best matches at the top.

## Monitoring & Maintenance

### View Latest Jobs
```bash
# Open the most recent HTML report
open latest_jobs.html
```

### View Logs
```bash
# See latest run
tail -50 logs/job_search_*.log

# Check for errors
grep -i error logs/*.log

# See all runs today
ls -lh logs/job_search_$(date +%Y%m%d)*.log
```

### Check Cronjobs
```bash
# List all scheduled jobs
crontab -l

# Edit cronjobs
crontab -e
```

### Clear Old Data
```bash
# Remove old logs (older than 30 days)
find logs/ -name "*.log" -mtime +30 -delete

# Reset job tracking (start fresh)
rm sent_jobs.json
```

## Troubleshooting

### Desktop notifications not appearing
- **Check System Preferences**: Go to System Preferences → Notifications → Terminal (or Script Editor)
- **Enable notifications**: Make sure "Allow Notifications" is checked
- **Test manually**: Run `./run_job_search.sh` and watch for the notification

### No jobs found
- Jobs may have already been sent (check `sent_jobs.json`)
- Try adjusting search criteria (more job titles, wider radius, older date range)
- Check logs for scraping errors: `grep -i error logs/*.log`

### HTML file not opening
- **Manual open**: `open latest_jobs.html` or double-click the file
- **Browser default**: Set your preferred browser as default in System Preferences
- File is always saved even if it doesn't auto-open

### Cronjob not running
- See `CRONJOB_SETUP.md` for detailed troubleshooting
- Verify cron is enabled: `crontab -l`
- Check system logs: `grep CRON /var/log/system.log`
- Ensure full paths in crontab

## Why Desktop Notifications?

**Advantages over email:**
- ✅ Instant notifications on your Mac
- ✅ No email service needed (free!)
- ✅ No API keys or quotas
- ✅ Beautiful, local HTML reports
- ✅ No inbox clutter
- ✅ Privacy - your data stays local

**Best for:**
- Users who work primarily on one computer
- People who want instant awareness of new jobs
- Those who prefer local file storage
- Anyone wanting a simpler, free solution

## Future Enhancements

Possible additions:
- Google Sheets integration for job tracking
- Slack/Discord webhook notifications
- Mobile push notifications (via Pushover or similar)
- Email summaries (weekly digest)
- Application status tracking

---

**Note**: This script uses public job board searches and respects rate limits. Your computer must be running for notifications to appear (or set up cronjob to run when computer is on).

