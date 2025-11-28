# Project Brief: Personal AI Automations

## Project Name
Personal AI Automations Hub

## Purpose
A centralized repository for personal automation scripts powered by AI and intelligent algorithms to streamline daily tasks, job hunting, and future productivity enhancements.

## Goals
1. **Job Search Automation** - Automatically find and alert on relevant job opportunities
2. **Extensibility** - Easy to add new automations as needs arise
3. **Reliability** - Run autonomously via cronjobs with proper logging and error handling
4. **Privacy** - Keep personal data and API keys secure
5. **Maintainability** - Clear documentation and modular structure

## Scope

### In Scope
- Job search automation (LinkedIn, Indeed)
- Email notifications via SendGrid
- Automated scheduling via cron
- Future AI-powered automations (TBD)
- Logging and monitoring

### Out of Scope
- Web UI (command-line only for now)
- Paid APIs (free tier only)
- Real-time notifications (scheduled checks only)

## Success Criteria
- Job search runs reliably 2x daily
- Zero missed opportunities in target job categories
- Email digest arrives on schedule
- Easy to add new automation scripts
- Clean logs for troubleshooting

## Timeline
- **Phase 1** (Complete): Job search automation working
- **Phase 2** (Current): Documentation and Memory Bank setup
- **Phase 3** (Future): Additional automations as needed

## Constraints
- Budget: Free tier services only (SendGrid 100 emails/day)
- Environment: macOS with Python 3.12
- Privacy: API keys in code (should migrate to env vars)

