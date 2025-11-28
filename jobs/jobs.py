#!/usr/bin/env python3
"""
Automated Job Search Script
Searches LinkedIn and Indeed for jobs matching your resume
Sends desktop notifications and creates local HTML file for viewing
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time
import os
from urllib.parse import quote_plus
import re
import subprocess

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Output Configuration
JOBS_HTML_FILE = os.path.join(os.path.dirname(__file__), "latest_jobs.html")

# Job Search Configuration
LOCATION = "Winter Springs, FL"
SEARCH_RADIUS = "50"  # miles
JOB_TITLES = [
    "Director of Engineering",
    "Engineering Manager",
    "Senior Engineering Manager",
    "VP of Engineering"
]

REQUIRED_SKILLS = [
    "React", "TypeScript", "Node.js", "JavaScript",
    "AI", "ML", "OpenAI", "LangChain",
    "Team Leadership", "Engineering Management"
]

NICE_TO_HAVE = [
    "EdTech", "Education Technology", "React Native",
    "Python", "GCP", "AWS", "MongoDB"
]

JOB_TYPE = "remote"  # Can be: remote, full-time, contract
POSTED_WITHIN_DAYS = 7  # Only jobs posted within last 7 days

# File to track already-sent jobs (prevents duplicates)
SENT_JOBS_FILE = "sent_jobs.json"

# ============================================
# HELPER FUNCTIONS
# ============================================

def load_sent_jobs():
    """Load previously sent job IDs to avoid duplicates"""
    if os.path.exists(SENT_JOBS_FILE):
        with open(SENT_JOBS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_sent_jobs(job_ids):
    """Save sent job IDs"""
    with open(SENT_JOBS_FILE, 'w') as f:
        json.dump(job_ids, f)

def calculate_match_score(job_title, job_description):
    """Calculate how well a job matches the resume (0-100)"""
    score = 0
    text = f"{job_title} {job_description}".lower()
    
    # Required skills (10 points each)
    for skill in REQUIRED_SKILLS:
        if skill.lower() in text:
            score += 10
    
    # Nice to have (5 points each)
    for skill in NICE_TO_HAVE:
        if skill.lower() in text:
            score += 5
    
    # Leadership keywords
    leadership_keywords = ["lead", "manage", "director", "mentor", "team"]
    for keyword in leadership_keywords:
        if keyword in text:
            score += 3
    
    return min(score, 100)  # Cap at 100

# ============================================
# INDEED SCRAPER
# ============================================

def search_indeed(job_title):
    """Search Indeed for jobs"""
    jobs = []
    
    try:
        # Build Indeed search URL
        query = f"{job_title} {JOB_TYPE}"
        url = f"https://www.indeed.com/jobs?q={quote_plus(query)}&l={quote_plus(LOCATION)}&radius={SEARCH_RADIUS}&fromage={POSTED_WITHIN_DAYS}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards (Indeed's HTML structure)
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        for card in job_cards[:10]:  # Limit to top 10 per search
            try:
                # Extract job details
                title_elem = card.find('h2', class_='jobTitle')
                company_elem = card.find('span', {'data-testid': 'company-name'})
                location_elem = card.find('div', {'data-testid': 'text-location'})
                
                if title_elem and company_elem:
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True)
                    location = location_elem.get_text(strip=True) if location_elem else LOCATION
                    
                    # Get job link
                    link_elem = title_elem.find('a')
                    job_id = link_elem.get('data-jk', '') if link_elem else ''
                    job_url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else ""
                    
                    # Get description snippet
                    desc_elem = card.find('div', class_='job-snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Calculate match score
                    match_score = calculate_match_score(title, description)
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': job_url,
                        'description': description[:300],  # First 300 chars
                        'source': 'Indeed',
                        'match_score': match_score,
                        'job_id': f"indeed_{job_id}"
                    })
            except Exception as e:
                continue
        
        time.sleep(2)  # Be respectful, don't hammer the server
        
    except Exception as e:
        print(f"Error searching Indeed for {job_title}: {e}")
    
    return jobs

# ============================================
# LINKEDIN SCRAPER
# ============================================

def search_linkedin(job_title):
    """Search LinkedIn for jobs"""
    jobs = []
    
    try:
        # Build LinkedIn search URL (public job search)
        query = f"{job_title} {JOB_TYPE}"
        url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(query)}&location={quote_plus(LOCATION)}&distance={SEARCH_RADIUS}&f_TPR=r{POSTED_WITHIN_DAYS*86400}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('div', class_='base-card')
        
        for card in job_cards[:10]:  # Limit to top 10 per search
            try:
                title_elem = card.find('h3', class_='base-search-card__title')
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                location_elem = card.find('span', class_='job-search-card__location')
                link_elem = card.find('a', class_='base-card__full-link')
                
                if title_elem and company_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True)
                    location = location_elem.get_text(strip=True) if location_elem else LOCATION
                    job_url = link_elem.get('href', '')
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
                    job_id = job_id_match.group(1) if job_id_match else ''
                    
                    # Calculate match score (description not available in listing)
                    match_score = calculate_match_score(title, "")
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': job_url,
                        'description': 'Click to view full description on LinkedIn',
                        'source': 'LinkedIn',
                        'match_score': match_score,
                        'job_id': f"linkedin_{job_id}"
                    })
            except Exception as e:
                continue
        
        time.sleep(2)  # Be respectful
        
    except Exception as e:
        print(f"Error searching LinkedIn for {job_title}: {e}")
    
    return jobs

# ============================================
# DESKTOP NOTIFICATION & HTML GENERATION
# ============================================

def send_desktop_notification(jobs):
    """Send macOS desktop notification for new jobs"""
    if not jobs:
        print("No new jobs found. Skipping notification.")
        return
    
    # Sort jobs by match score
    jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Get top 3 jobs for notification preview
    top_jobs = jobs[:3]
    
    title = f"{len(jobs)} New Jobs Found!"
    
    # Build notification message (simplified for notification)
    if len(jobs) == 1:
        message = f"{top_jobs[0]['title']} at {top_jobs[0]['company']}"
    elif len(jobs) == 2:
        message = f"{top_jobs[0]['title']}, {top_jobs[1]['title']}"
    else:
        # For 3+ jobs, just show the top match and count
        message = f"{top_jobs[0]['title']} at {top_jobs[0]['company']} and {len(jobs)-1} more"
    
    # Use osascript (AppleScript) for notification
    try:
        # Escape quotes in the message
        safe_title = title.replace('"', '\\"').replace("'", "\\'")
        safe_message = message.replace('"', '\\"').replace("'", "\\'")
        
        script = f'''display notification "{safe_message}" with title "{safe_title}" sound name "Ping"'''
        subprocess.run(['osascript', '-e', script], check=True)
        print(f"✅ Desktop notification sent for {len(jobs)} jobs!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not send desktop notification: {e}")
    except Exception as e:
        print(f"⚠️  Error with notification: {e}")

def save_jobs_html(jobs):
    """Save jobs to a local HTML file for easy browsing"""
    if not jobs:
        print("No jobs to save to HTML.")
        return
    
    # Sort jobs by match score
    jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Build HTML content
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Search Results - {datetime.now().strftime('%B %d, %Y')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 18px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }}
        .stat {{
            background: #f8f9fa;
            padding: 10px 20px;
            border-radius: 8px;
        }}
        .stat strong {{
            color: #667eea;
            font-size: 24px;
        }}
        .job {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .job:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .job-title {{
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
        }}
        .company {{
            font-size: 18px;
            color: #555;
            margin-bottom: 8px;
        }}
        .company::before {{
            content: "🏢 ";
        }}
        .location {{
            color: #777;
            margin-bottom: 12px;
            font-size: 15px;
        }}
        .location::before {{
            content: "📍 ";
        }}
        .source {{
            display: inline-block;
            background: #e9ecef;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 13px;
            color: #495057;
            margin-left: 10px;
        }}
        .match-score {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            white-space: nowrap;
        }}
        .high-match {{
            background-color: #28a745;
            color: white;
        }}
        .medium-match {{
            background-color: #ffc107;
            color: black;
        }}
        .low-match {{
            background-color: #6c757d;
            color: white;
        }}
        .description {{
            color: #666;
            margin: 15px 0;
            line-height: 1.6;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 15px;
        }}
        .apply-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            margin-top: 15px;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        .apply-btn:hover {{
            transform: scale(1.05);
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            margin-top: 30px;
            font-size: 14px;
        }}
        .timestamp {{
            background: rgba(255,255,255,0.9);
            padding: 10px 20px;
            border-radius: 6px;
            margin-top: 10px;
            display: inline-block;
            color: #667eea;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Your Job Search Results</h1>
            <p>Found {len(jobs)} new opportunities matching your profile</p>
            <div class="stats">
                <div class="stat">
                    <strong>{len([j for j in jobs if j['match_score'] >= 70])}</strong>
                    <div>Excellent Matches</div>
                </div>
                <div class="stat">
                    <strong>{len([j for j in jobs if 40 <= j['match_score'] < 70])}</strong>
                    <div>Good Matches</div>
                </div>
                <div class="stat">
                    <strong>{len([j for j in jobs if j['match_score'] < 40])}</strong>
                    <div>Potential Matches</div>
                </div>
            </div>
        </div>
"""
    
    for job in jobs:
        # Determine match score class and text
        if job['match_score'] >= 70:
            score_class = "high-match"
            score_text = "🔥 Excellent Match"
        elif job['match_score'] >= 40:
            score_class = "medium-match"
            score_text = "✓ Good Match"
        else:
            score_class = "low-match"
            score_text = "• Potential Match"
        
        # Escape HTML characters in job data
        title = job['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        company = job['company'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        location = job['location'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        description = job['description'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        html_content += f"""
        <div class="job">
            <div class="job-header">
                <div>
                    <div class="job-title">{title}</div>
                    <div class="company">{company}</div>
                    <div class="location">{location}<span class="source">{job['source']}</span></div>
                </div>
                <span class="match-score {score_class}">{score_text} ({job['match_score']}%)</span>
            </div>
            <div class="description">{description}</div>
            <a href="{job['url']}" class="apply-btn" target="_blank">View & Apply →</a>
        </div>
"""
    
    html_content += f"""
        <div class="footer">
            <p>This is an automated job search digest. Jobs are ranked by match score based on your resume.</p>
            <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
    </div>
</body>
</html>
"""
    
    # Save to file
    try:
        with open(JOBS_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Saved {len(jobs)} jobs to HTML file: {JOBS_HTML_FILE}")
        
        # Automatically open in Google Chrome
        try:
            subprocess.run(['open', '-a', 'Google Chrome', JOBS_HTML_FILE], check=False)
            print(f"📂 Opening jobs in Google Chrome")
        except Exception:
            # Fallback to default open
            try:
                subprocess.run(['open', JOBS_HTML_FILE], check=False)
                print(f"📂 Opening jobs in default browser")
            except Exception:
                print(f"📂 HTML file saved (couldn't auto-open)")
            
    except Exception as e:
        print(f"❌ Error saving HTML file: {e}")

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to search jobs and send email"""
    print(f"\n{'='*60}")
    print(f"Job Search Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    all_jobs = []
    sent_jobs = load_sent_jobs()
    
    # Search each job title on both platforms
    for job_title in JOB_TITLES:
        print(f"Searching for: {job_title}")
        
        # Search Indeed
        indeed_jobs = search_indeed(job_title)
        print(f"  - Found {len(indeed_jobs)} jobs on Indeed")
        all_jobs.extend(indeed_jobs)
        
        # Search LinkedIn
        linkedin_jobs = search_linkedin(job_title)
        print(f"  - Found {len(linkedin_jobs)} jobs on LinkedIn")
        all_jobs.extend(linkedin_jobs)
        
        time.sleep(3)  # Pause between searches
    
    # Filter out already-sent jobs and duplicates
    new_jobs = []
    seen_ids = set()
    
    for job in all_jobs:
        job_id = job['job_id']
        if job_id and job_id not in sent_jobs and job_id not in seen_ids:
            new_jobs.append(job)
            seen_ids.add(job_id)
    
    print(f"\n{'='*60}")
    print(f"Total new jobs found: {len(new_jobs)}")
    print(f"{'='*60}\n")
    
    # Notify and save if there are new jobs
    if new_jobs:
        # Send desktop notification
        send_desktop_notification(new_jobs)
        
        # Save to HTML file for viewing
        save_jobs_html(new_jobs)
        
        # Update sent jobs list
        sent_jobs.extend(list(seen_ids))
        # Keep only last 1000 job IDs to prevent file from growing too large
        if len(sent_jobs) > 1000:
            sent_jobs = sent_jobs[-1000:]
        save_sent_jobs(sent_jobs)
    else:
        print("No new jobs to report.")
    
    print(f"\nJob search completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================
# RUN SCRIPT
# ============================================

if __name__ == "__main__":
    main()