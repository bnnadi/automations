# Product Context

## Why This Exists
Managing job searches manually is time-consuming and error-prone. This automation ensures no opportunities are missed while I focus on applications and interviews.

## Problems It Solves
1. **Manual Search Fatigue** - No need to check job boards multiple times daily
2. **Missing Opportunities** - Automated searches catch new postings within hours
3. **Relevance Filtering** - Match scores help prioritize best-fit roles
4. **Duplicate Noise** - Tracks sent jobs to prevent repeat notifications
5. **Time Efficiency** - Saves 30+ minutes per day

## How It Should Work

### Job Search Flow
1. Cron triggers script at 9 AM and 6 PM
2. Script searches LinkedIn and Indeed for configured job titles
3. Each job gets a match score based on skills/keywords
4. New jobs (not previously sent) are compiled into an email digest
5. Email sent via SendGrid with job details and apply links
6. Job IDs saved to prevent future duplicates

### User Experience
- Receive clean, formatted email digests twice daily
- Jobs sorted by match score (highest first)
- One-click apply links
- No duplicates or spam
- Clear indication of match quality (excellent/good/potential)

## Future Vision
This is the foundation for a broader personal automation suite:
- Newsletter summarization
- Calendar optimization
- Financial tracking
- Learning resource aggregation
- Social media content scheduling

