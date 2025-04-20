import requests
from bs4 import BeautifulSoup
import json
import time
import random
from requests.exceptions import RequestException

def scrape_cyber_news(topic):
    sites = [
        {
            "name": "The Hacker News",
            "url": "https://thehackernews.com/",
            "article_selector": "div.body-post.clear",
            "title_selector": "h2.home-title",
            "link_selector": "a.story-link",
            "summary_selector": "div.home-desc"
        },
        {
            "name": "Krebs on Security",
            "url": "https://krebsonsecurity.com/",
            "article_selector": "article.post",
            "title_selector": "h2.entry-title",
            "link_selector": "h2.entry-title a",
            "summary_selector": "div.entry-content p:first-child"
        },
        {
            "name": "Bleeping Computer",
            "url": "https://www.bleepingcomputer.com/news/",
            "article_selector": "div.article_front",
            "title_selector": "h4",
            "link_selector": "h4 a",
            "summary_selector": "div.article_content"
        }
    ]
    
    all_articles = []
    errors = []
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    for site in sites:
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(site["url"], headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            site_articles = []
            
            for item in soup.select(site["article_selector"]):
                title_elem = item.select_one(site["title_selector"])
                link_elem = item.select_one(site["link_selector"])
                summary_elem = item.select_one(site["summary_selector"])
                
                if title_elem and link_elem:
                    title_text = title_elem.text.strip()
                    link_url = link_elem.get("href")
                    
                    if link_url and not link_url.startswith(('http://', 'https://')):
                        link_url = site["url"].rstrip('/') + '/' + link_url.lstrip('/')
                    
                    summary_text = summary_elem.text.strip() if summary_elem else "No summary available"
                    
                    if topic.lower() in title_text.lower() or topic.lower() in summary_text.lower():
                        site_articles.append({
                            "site": site["name"],
                            "title": title_text,
                            "url": link_url,
                            "summary": summary_text
                        })
            
            all_articles.extend(site_articles)
            
        except RequestException as e:
            errors.append({
                "site": site["name"],
                "error": f"Request error: {str(e)}"
            })
        except Exception as e:
            errors.append({
                "site": site["name"],
                "error": f"Parsing error: {str(e)}"
            })
    
    result = {
        "status": "success" if not errors or all_articles else "partial_success" if errors and all_articles else "failure",
        "topic": topic,
        "count": len(all_articles),
        "articles": all_articles
    }
    
    if errors:
        result["errors"] = errors
        
    if not all_articles:
        result["message"] = f"No articles found related to '{topic}'"
        
    return result

def validate_topic(topic):
    return bool(topic and isinstance(topic, str) and topic.strip())
