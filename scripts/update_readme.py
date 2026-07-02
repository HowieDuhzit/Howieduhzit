#!/usr/bin/env python3
"""
Dynamic README Updater for GitHub Profile
Automatically updates stats, badges, recent activity, and other dynamic content.
"""

import os
import re
import sys
import time
import argparse
import requests
from datetime import datetime, timedelta
from github import Github, GithubException
from bs4 import BeautifulSoup

DEFAULT_USERNAME = "HowieDuhzit"
DEFAULT_RSS_URL = "https://howieduhzit.best/rss.xml"
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, doubled each retry


def retry_request(func, *args, **kwargs):
    """Execute a function with retry logic and exponential backoff."""
    last_exception = None
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except (requests.RequestException, GithubException) as e:
            last_exception = e
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF * (2 ** attempt)
                print(f"  Retry {attempt + 1}/{MAX_RETRIES} after {wait}s: {e}")
                time.sleep(wait)
    raise last_exception


def get_github_stats(username, token):
    """Get GitHub statistics for the user with a single API call per repo."""
    g = Github(token)

    try:
        user = retry_request(g.get_user, username)
        total_stars = 0
        total_forks = 0
        recent_repos = []
        since = datetime.now() - timedelta(days=30)

        for repo in retry_request(user.get_repos):
            if repo.fork:
                continue
            total_stars += repo.stargazers_count
            total_forks += repo.forks_count
            if repo.updated_at and repo.updated_at > since:
                recent_repos.append(repo.name)

        return {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_repos": user.public_repos,
            "recent_repos": sorted(recent_repos)[:5],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        }
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return None


def get_twitter_info(username, bearer_token):
    """Get Twitter/X information and recent tweets."""
    if not bearer_token:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "README-Update/1.0",
        }

        user_url = f"https://api.twitter.com/2/users/by/username/{username}"
        user_response = retry_request(
            requests.get,
            user_url,
            headers=headers,
            params={"user.fields": "public_metrics,description,created_at"},
            timeout=15,
        )

        if user_response.status_code != 200:
            print(f"Twitter user lookup failed: {user_response.status_code}")
            return None

        user_data = user_response.json()["data"]

        tweets_url = f"https://api.twitter.com/2/users/{user_data['id']}/tweets"
        tweets_response = retry_request(
            requests.get,
            tweets_url,
            headers=headers,
            params={"max_results": 3, "tweet.fields": "created_at,public_metrics"},
            timeout=15,
        )

        recent_tweets = []
        if tweets_response.status_code == 200:
            for tweet in tweets_response.json().get("data", [])[:3]:
                text = tweet["text"]
                recent_tweets.append({
                    "text": text[:100] + ("..." if len(text) > 100 else ""),
                    "created_at": tweet["created_at"][:10],
                    "likes": tweet["public_metrics"].get("like_count", 0),
                })

        return {
            "followers": user_data["public_metrics"]["followers_count"],
            "following": user_data["public_metrics"]["following_count"],
            "tweets": user_data["public_metrics"]["tweet_count"],
            "bio": user_data.get("description", ""),
            "joined": user_data["created_at"][:10],
            "recent_tweets": recent_tweets,
        }
    except Exception as e:
        print(f"Error fetching Twitter info: {e}")
        return None


def get_recent_blog_posts(rss_url=DEFAULT_RSS_URL):
    """Get recent blog posts from RSS feed with fallback to empty list."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; README-Bot/1.0)"}
        response = retry_request(requests.get, rss_url, headers=headers, timeout=15)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            posts = []
            for item in soup.find_all("item")[:3]:
                title = item.find("title")
                link = item.find("link")
                pub_date = item.find("pubDate")

                title_text = title.text.strip() if title else "Untitled"
                link_text = link.text.strip() if link else "#"
                date_str = "Recent"

                if pub_date and pub_date.text:
                    try:
                        date_obj = datetime.strptime(
                            pub_date.text.strip(), "%a, %d %b %Y %H:%M:%S %Z"
                        )
                        date_str = date_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        pass

                posts.append({"title": title_text, "url": link_text, "date": date_str})

            if posts:
                return posts

    except Exception as e:
        print(f"Error fetching blog posts: {e}")

    return []


def update_badges(content, stats):
    """Update dynamic badge values in README content."""
    if not stats:
        return content

    stars = stats["total_stars"]
    repos = stats["total_repos"]
    forks = stats["total_forks"]

    # Update the badges section between the two markers
    badges_pattern = (
        r'(<div align="center">\s*<p>\s*<img src="https://img\.shields\.io/badge/Total_Stars-)'
        r'.*?'
        r'(Total_Forks-.*?\.svg)'
    )

    new_badges = (
        f'\\1{stars}-blue?style=flat&logo=github" alt="Total Stars" />\n'
        f'    <img src="https://img.shields.io/badge/Public_Repos-{repos}-green?style=flat&logo=github" alt="Public Repos" />\n'
        f'    <img src="https://img.shields.io/badge/\\2-{forks}-orange?style=flat&logo=github" alt="Total Forks" />'
    )

    updated = re.sub(badges_pattern, new_badges, content, flags=re.DOTALL)
    if updated == content:
        print("  Warning: Badge pattern not found in README; badges not updated")
    return updated


def update_github_stats(content, stats):
    """Update GitHub stats section in README."""
    if not stats:
        return content

    # Update activity highlights
    old_highlights = re.search(
        r"### \*\*.*?Recent Activity Highlights\*\*\n((?:- .*\n)*)",
        content,
        re.MULTILINE,
    )
    if old_highlights:
        new_highlights = "### **Recent Activity Highlights**\n"
        new_highlights += f"- Building AI agent ecosystem with Eliza framework\n"
        new_highlights += f"- Developing 3D modeling tools and Blender addons\n"
        new_highlights += f"- Creating full-stack web applications and MCP servers\n"
        new_highlights += f"- Contributing to open source projects with {stats['total_stars']}+ combined stars\n"
        new_highlights += f"- {stats['total_repos']} public repositories, {stats['total_forks']} total forks\n"
        content = content.replace(old_highlights.group(0), new_highlights)

    # Update last-updated timestamp
    content = re.sub(
        r"\*GitHub stats and detailed metrics will appear here.*?\*",
        f"*Last updated: {stats['last_updated']}*",
        content,
    )

    return content


def update_twitter_section(content, twitter_info):
    """Update Twitter/X section in README."""
    if not twitter_info:
        return content

    twitter_section = f"""
### Twitter/X Stats
- **{twitter_info['followers']:,}** followers
- **{twitter_info['tweets']:,}** tweets
- **{twitter_info['following']:,}** following
- Joined {twitter_info['joined']}

*{twitter_info['bio']}*

### Recent Tweets
"""
    for tweet in twitter_info.get("recent_tweets", []):
        twitter_section += f"- **{tweet['created_at']}**: {tweet['text']}\n"
    twitter_section += "\n---"

    social_pattern = r"(## .*Connect With Me.*?---)"
    replacement = r"\1\n" + twitter_section + "\n---"
    return re.sub(social_pattern, replacement, content, flags=re.DOTALL)


def update_blog_section(content, posts):
    """Update blog posts section in README."""
    if not posts:
        return content

    blog_section = '## Latest Blog Posts\n\n<div align="center">\n'
    for post in posts:
        blog_section += f"### [{post['title']}]({post['url']})\n"
        blog_section += f"*Published: {post['date']}*\n\n"
    blog_section += "</div>\n\n---"

    return re.sub(
        r"## .*Blog Posts.*?---",
        blog_section,
        content,
        flags=re.DOTALL,
    )


def update_readme(args):
    """Main entry point: update README with all dynamic content."""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    github_token = os.getenv("GITHUB_TOKEN")
    twitter_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not github_token:
        print("No GitHub token available; skipping GitHub stats")
        return

    print(f"Fetching stats for {args.username}...")
    github_stats = get_github_stats(args.username, github_token)
    twitter_info = (
        get_twitter_info(args.username, twitter_token) if twitter_token else None
    )
    recent_posts = get_recent_blog_posts(args.rss_url)

    content = update_badges(content, github_stats)
    content = update_github_stats(content, github_stats)
    content = update_twitter_section(content, twitter_info)
    content = update_blog_section(content, recent_posts)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated successfully!")


def parse_args():
    parser = argparse.ArgumentParser(description="Update GitHub profile README")
    parser.add_argument(
        "--username",
        default=os.getenv("GITHUB_USERNAME", DEFAULT_USERNAME),
        help=f"GitHub username (default: {DEFAULT_USERNAME})",
    )
    parser.add_argument(
        "--rss-url",
        default=os.getenv("RSS_URL", DEFAULT_RSS_URL),
        help=f"RSS feed URL (default: {DEFAULT_RSS_URL})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    update_readme(parse_args())
