# 🤖 Personal AI Automations

A centralized hub for personal automation scripts powered by AI and intelligent algorithms. Streamlines daily tasks, job hunting, and productivity enhancement.

## 📁 Project Structure

```
automations/
├── memory-bank/           # 📚 Project documentation & architecture
│   ├── projectbrief.md   # Project goals and scope
│   ├── productContext.md # Why this exists, problems it solves
│   ├── activeContext.md  # Current focus and recent changes
│   ├── systemPatterns.md # Architecture and design patterns
│   ├── techContext.md    # Technology stack and setup
│   └── progress.md       # What works, what's next
├── jobs/                  # 🎯 Job search automation
│   ├── jobs.py           # Main automation script
│   ├── run_job_search.sh # Cron wrapper
│   ├── requirements.txt  # Python dependencies
│   ├── .env.example      # Environment variable template
│   ├── logs/             # Execution logs
│   └── README.md         # Detailed setup instructions
├── .cursorrules          # Project intelligence & patterns
├── .gitignore            # Git ignore rules
└── LICENSE               # MIT License
```

## 🚀 Quick Start

### Prerequisites
- macOS with Python 3.12+
- No external accounts needed!

### Setup

1. **Clone the repository**
   ```bash
   cd /Users/bisikennadi/Projects/automations
   ```

2. **Set up a specific automation** (example: jobs)
   ```bash
   cd jobs
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Test the automation**
   ```bash
   python3 jobs.py
   ```

5. **Set up cron job** (optional)
   ```bash
   crontab -e
   # Add your schedule (see automation-specific README)
   ```

## 🎯 Current Automations

### Job Search Bot
Automatically searches LinkedIn and Indeed for engineering leadership positions, calculates match scores based on your skills, and sends **desktop notifications** with beautiful HTML reports.

**Features:**
- 🔍 Multi-platform search (LinkedIn, Indeed)
- 🎯 Smart match scoring
- 🔔 **Desktop notifications** (macOS)
- 📄 **Beautiful HTML reports** for easy browsing
- 🚫 Duplicate prevention
- ⏰ Automated scheduling
- 📊 Detailed logging
- 🆓 **Completely free** - no API keys needed!

**Status:** ✅ Operational  
**Details:** See [`jobs/README.md`](jobs/README.md)

## 📚 Documentation

All project documentation lives in the [`memory-bank/`](memory-bank/) directory:

- **[Project Brief](memory-bank/projectbrief.md)** - Goals, scope, and success criteria
- **[Product Context](memory-bank/productContext.md)** - Why this exists and problems it solves
- **[Active Context](memory-bank/activeContext.md)** - Current focus and next steps
- **[System Patterns](memory-bank/systemPatterns.md)** - Architecture and design decisions
- **[Tech Context](memory-bank/techContext.md)** - Technology stack and setup
- **[Progress](memory-bank/progress.md)** - What works and what's next

## 🛠 Adding New Automations

1. Create a new directory for your automation
2. Follow the standard structure:
   ```
   new-automation/
   ├── README.md           # Setup instructions
   ├── requirements.txt    # Python dependencies
   ├── .env.example        # Config template
   ├── main_script.py      # Your automation logic
   ├── run_*.sh            # Cron wrapper (if needed)
   └── logs/               # Auto-generated logs
   ```
3. Use environment variables for sensitive data
4. Update Memory Bank docs with new patterns
5. Add to this README

## 🔒 Security

- 🔐 All API keys and secrets in `.env` files (gitignored)
- 📝 `.env.example` templates provided for each automation
- ✅ Verified sender emails required for email services
- 🚫 No passwords or sensitive data in code

## 📊 Monitoring

Each automation logs to its own `logs/` directory with timestamped files:

```bash
# View latest logs
tail -50 jobs/logs/job_search_*.log

# Check for errors
grep -i error jobs/logs/*.log

# View cron jobs
crontab -l
```

## 🤝 Contributing

This is a personal project, but patterns and ideas are welcome! Each automation is self-contained and can be adapted for your own use.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔮 Future Automations

Ideas for future additions:
- 📰 Newsletter summarization bot
- 📅 Calendar optimization script
- 💰 Financial tracking automation
- 📚 Learning resource aggregator
- 📱 Social media content scheduler

---

**Last Updated:** November 28, 2025  
**Maintained By:** Bisike Nnadi

