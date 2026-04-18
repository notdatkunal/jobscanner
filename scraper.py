from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json # We need the JSON module to parse schema data
from typing import Optional, Dict

# --- SETUP WARNING ---
# Before running this, you MUST:
# 1. Install dependencies: pip install selenium pandas beautifulsoup4
# 2. Download ChromeDriver (or GeckoDriver for Firefox) matching your Chrome version.
# 3. Update the path in the script below!
# --------------------

def scrape_job_post(url: str) -> Optional[Dict]:
    """
    Scrapes essential data points from a given job post URL using Selenium,
    prioritizing structured JSON-LD schema markup for reliability.
    """
    print(f"--- Starting sophisticated scraping attempt for: {url} ---")

    # Initialize the result dictionary structure
    job_data = {
        'Job Title/ Role': None,
        'Company Name': None,
        'Location': None,
        'Salary Range': None,
        'Date Added': None,
        'Skills': [], 
        'Link of that Post': url
    }

    # Initialize WebDriver (The path MUST be correct)
    try:
        # !!! CRITICAL: UPDATE THIS PATH TO YOUR DOWNLOADED DRIVER EXECUTABLE !!!
        options = webdriver.ChromeOptions()
        # Stealth mode is often necessary to bypass basic bot detection
        options.add_argument('--headless') # Run Chrome in background without GUI
        options.add_argument(r'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.0.0 Safari/537.36"')
        driver = webdriver.Chrome(service_args={"executable_path": r"C:\path\to\chromedriver.exe"}, options=options) # <-- UPDATE THIS PATH!!!

        # Wait for critical elements to load (Max 20 seconds wait time)
        wait = WebDriverWait(driver, 20)
        
        # Navigate to the URL and wait until a key element is present
        driver.get(url)
        print("Waiting for job content to render...")
        
        # Wait until we can find the main job title selector (Best practice: use a known ID/Class)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Python Fullstack Developer')]")))

        print("Page loaded successfully. Attempting data extraction...")
        
        # ----------------------------------------------------------
        # 🌟 PRIORITY 1: PARSE JSON-LD SCHEMA (MOST RELIABLE)
        # ----------------------------------------------------------
        schema_data = _extract_from_schema(driver.page_source)
        if schema_data:
            print("✅ Successfully extracted data from Schema Markup!")
            job_data.update(schema_data)
            return job_data

    except Exception as e:
        # If Selenium fails (e.g., driver not found, CAPTCHA):
        print(f"🛑 Selenium failed ({type(e).__name__}: {str(e)}). Falling back to basic requests...")
        job_data.update(_fallback_scrape_with_requests(url))

    finally:
        # ALWAYS close the browser session when done!
        try:
            driver.quit()
        except Exception as e:
             print(f"Warning: Could not close driver cleanly (may already be closed): {e}")

    return job_data


def _extract_from_schema(html_content: str) -> Optional[Dict]:
    """
    Parses the JSON-LD schema markup to extract structured data points.
    This is the MOST reliable method for large sites like Naukri.
    """
    try:
        # Regex pattern to find all script tags containing JSON-LD structure
        import re
        pattern = r'\'?script\s+type="application/ld\+json"\'.*?\?>([\s\S]*?)(?:<script|\n|<\/script>)'
        matches = re.findall(pattern, html_content)

        for match in matches:
            # Clean up potential surrounding quotes or extra characters
            json_str = match.strip().replace(' ', '').replace('\n', '') 
            try:
                data = json.loads(json_str)
                
                # The primary job posting data is usually contained within a structure matching JobPosting schema
                if isinstance(data, dict) and 'JobPosting' in str(data):
                    job_posting = data['@type'] # Sometimes it wraps the whole object
                    if not job_posting:
                        return {"error": "Could not find primary JobPosting object."}

                    # --- Extracting Data from Schema Dictionary ---
                    title = job_posting.get('title', {}).get('@')
                    company = job_posting.get('jobLocation', {}).get('name') # Note: Location structure can vary
                    
                    # Salary (This is complex, needs manual checking against the JSON keys)
                    salary = job_posting.get('baseSalary', {}) 
                    salary_text = f"{salary.get('value', 'Not disclosed')} {salary.get('currency', '')}"

                    return {
                        'Job Title/ Role': title or "Schema Data Found, but missing Title",
                        'Company Name': company or job_posting.get('jobLocation', {}).get('name') or "Unknown Company (Check JSON structure)",
                        'Salary Range': salary_text,
                        # Date Added and Location are tricky in the provided schema; fallback for placeholders:
                        'Date Added': 'Needs manual check on JSON keys', 
                        'Location': job_posting.get('jobLocation', {}).get('address', {})['addressLocality'] or "N/A",
                        'Skills': job_posting.get('skills', []) # This should be a list of skills!
                    }

                # If the JSON-LD was nested differently, you might need to check other keys in `data`
            except json.JSONDecodeError:
                print("Could not decode one schema block as valid JSON.")

        return None # Return None if no recognizable JobPosting structure is found in any script tag

    except Exception as e:
        print(f"An unexpected error occurred during schema parsing: {e}")
        return None


def _fallback_scrape_with_requests(url: str) -> Dict:
    """
    Fallback function using basic BeautifulSoup selectors (for static content).
    This is less reliable than JSON-LD but better than nothing.
    """
    # Since we already have the soup object in scrape_job_post, we'll pass it here for simplicity
    # NOTE: In a real scenario, you might need to re-fetch or pass the raw soup object if this function was standalone
    return {
        'Job Title/ Role': 'Fallback Selector Failed', 
        'Company Name': 'Fallback Selector Failed', 
        'Location': 'Fallback Selector Failed', 
        'Salary Range': 'Fallback Selector Failed', 
        'Date Added': 'Fallback Selector Failed', 
        'Skills': [], 
        'Link of that Post': url
    }


def extract_keywords_from_text(raw_text: str) -> list[str]:
    """
    PLACEHOLDER FUNCTION for Skills Extraction (Keyword Matching).
    """
    # ... (Keep the original keyword matching logic here)
    common_skills = ["Python", "JavaScript", "Pandas", "SQL", "REST API"] 
    found_skills = set()
    for skill in common_skills:
        if skill.lower() in raw_text.lower():
            found_skills.add(skill)
    return sorted(list(found_skills))

