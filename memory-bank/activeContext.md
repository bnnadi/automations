# Active Context

## Current Focus
Refining job search automation with desktop notifications and local HTML reports.

## Recent Changes (November 28, 2025)
- ✅ **Migrated from email to desktop notifications**
  - Removed SendGrid dependency (simpler setup)
  - Implemented macOS native notifications
  - Generate beautiful HTML reports that auto-open in browser
  - Benefits: Instant notifications, no API keys, fully local & private
- Job search automation fully operational
- Running on cronjobs successfully
- Logs directory tracking execution history
- Memory Bank documentation updated
- All documentation updated to reflect notification system

## Next Steps
1. **Google Sheets Integration**: Consider adding job tracking spreadsheet
2. **Monitoring**: Create dashboard or summary script for job search stats
3. **Extensions**: Consider adding more job boards or filtering options
4. **Testing**: Add unit tests for core functions
5. **Refinement**: Improve match scoring algorithm

## Active Decisions
- **Monorepo Structure**: Each automation gets its own subdirectory
- **Python Standard**: Use Python for consistency across automations
- **Local First**: Prefer local solutions (notifications, files) over cloud services
- **Free & Simple**: No API keys or external dependencies unless necessary
- **Cron Scheduling**: Keep it simple with cron vs more complex schedulers
- **HTML Reports**: Beautiful, standalone HTML files for rich data presentation

## Open Questions
- Should we add Google Sheets for job application tracking?
- Should we add Glassdoor or other job boards?
- Should match scoring algorithm be more sophisticated?
- Time to add tests?

