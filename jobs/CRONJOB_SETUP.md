# Cronjob Setup Guide for Job Search Automation

## Quick Setup

### 1. Install Dependencies (One-Time Setup)
```bash
cd jobs
pip3 install -r requirements.txt
```

Or use a virtual environment (recommended):
```bash
cd jobs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 2. Configure Your Search Preferences
Edit `jobs.py` to customize:
- Job titles, location, search radius
- Required and nice-to-have skills
- Job type preferences
- Date range for searches

See the main README.md for detailed configuration options.

### 3. Test the Script Manually
```bash
cd jobs
./run_job_search.sh
```

Check the logs:
```bash
cat logs/job_search_*.log | tail -50
```

### 4. Set Up Cronjob

Open your crontab:
```bash
crontab -e
```

Add these lines to run the script **twice daily** (9 AM and 6 PM):
```bash
# Job Search Automation - Runs at 9:00 AM daily
0 9 * * * $HOME/Projects/automations/jobs/run_job_search.sh

# Job Search Automation - Runs at 6:00 PM daily
0 18 * * * $HOME/Projects/automations/jobs/run_job_search.sh
```

**Note**: Replace `$HOME/Projects/automations` with your actual project path. To find it, run:
```bash
cd jobs && pwd
```

Save and exit (`:wq` in vim, or Ctrl+X in nano).

## Alternative Cronjob Schedules

### Run every 6 hours:
```bash
0 */6 * * * $HOME/Projects/automations/jobs/run_job_search.sh
```

### Run Monday-Friday at 9 AM and 6 PM (weekdays only):
```bash
0 9 * * 1-5 $HOME/Projects/automations/jobs/run_job_search.sh
0 18 * * 1-5 $HOME/Projects/automations/jobs/run_job_search.sh
```

### Run every 3 hours during work hours (9 AM - 6 PM):
```bash
0 9-18/3 * * * $HOME/Projects/automations/jobs/run_job_search.sh
```

**Note**: Replace `$HOME/Projects/automations` with your actual project path.

## Cronjob Time Format Reference
```
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, Sunday=0 or 7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

## Verify Cronjob is Running

### List your cronjobs:
```bash
crontab -l
```

### Check the logs:
```bash
# View latest log (from jobs directory)
ls -lt logs/ | head -5

# View last run
tail -50 logs/job_search_*.log
```

### Check system cron logs (macOS):
```bash
log show --predicate 'process == "cron"' --last 1h
```

## Troubleshooting

### Cronjob not running?
1. **Grant Full Disk Access to cron on macOS:**
   - System Settings → Privacy & Security → Full Disk Access
   - Add `/usr/sbin/cron` (you may need to manually navigate to it)

2. **Check if cron daemon is running:**
   ```bash
   sudo launchctl list | grep cron
   ```

3. **Test the script manually:**
   ```bash
   cd jobs
   ./run_job_search.sh
   ```

### No emails being sent?
1. Check SendGrid API key is valid
2. Verify sender email is verified in SendGrid dashboard
3. Check the logs for error messages:
   ```bash
   grep -i error logs/*.log
   ```

### Permission denied errors?
```bash
cd jobs
chmod +x run_job_search.sh
chmod +x jobs.py
```

## Log Management

Logs are automatically cleaned up - only the last 30 runs are kept.

View all logs:
```bash
ls -lh logs/
```

Delete old logs manually:
```bash
rm logs/job_search_*.log
```

## Disable/Remove Cronjob

To temporarily disable:
```bash
crontab -e
# Comment out the line(s) with # at the beginning
```

To remove all cronjobs:
```bash
crontab -r
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Update SENDER_EMAIL in jobs.py
3. ✅ Test script manually
4. ✅ Set up cronjob
5. ✅ Monitor logs for first few runs
6. 🎉 Enjoy automated job alerts!

