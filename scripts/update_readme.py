#!/usr/bin/env python3
"""
Dynamic README Updater for GitHub Profile
Automatically updates stats, recent activity, and other dynamic content
"""

import os
import re
import requests
from datetime import datetime, timedelta
from github import Github
from bs4 import BeautifulSoup

def get_github_stats(username, token):
    """Get GitHub statistics for the user"""
    g = Github(token)

    try:
        user = g.get_user(username)

        # Get basic stats
        total_stars = sum(repo.stargazers_count for repo in user.get_repos() if not repo.fork)
        total_forks = sum(repo.forks_count for repo in user.get_repos() if not repo.fork)
        total_repos = user.public_repos

        # Get recent activity (last 30 days)
        since = datetime.now() - timedelta(days=30)
        recent_commits = 0
        recent_repos = []

        for repo in user.get_repos():
            if repo.updated_at and repo.updated_at > since:
                recent_repos.append(repo.name)

        return {
            'total_stars': total_stars,
            'total_forks': total_forks,
            'total_repos': total_repos,
            'recent_repos': recent_repos[:5],  # Last 5 updated repos
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M UTC')
        }
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return None

def get_twitter_info(username, bearer_token):
    """Get Twitter/X information and recent tweets"""
    if not bearer_token:
        return None

    try:
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'README-Update/1.0'
        }

        # Get user info
        user_url = f'https://api.twitter.com/2/users/by/username/{username}'
        user_response = requests.get(user_url, headers=headers, params={'user.fields': 'public_metrics,description,created_at'})

        if user_response.status_code != 200:
            return None

        user_data = user_response.json()['data']

        # Get recent tweets
        tweets_url = f'https://api.twitter.com/2/users/{user_data["id"]}/tweets'
        tweets_response = requests.get(tweets_url, headers=headers,
                                     params={'max_results': 3, 'tweet.fields': 'created_at,public_metrics'})

        recent_tweets = []
        if tweets_response.status_code == 200:
            tweets_data = tweets_response.json().get('data', [])
            for tweet in tweets_data[:3]:  # Last 3 tweets
                recent_tweets.append({
                    'text': tweet['text'][:100] + ('...' if len(tweet['text']) > 100 else ''),
                    'created_at': tweet['created_at'][:10],
                    'likes': tweet['public_metrics'].get('like_count', 0)
                })

        return {
            'followers': user_data['public_metrics']['followers_count'],
            'following': user_data['public_metrics']['following_count'],
            'tweets': user_data['public_metrics']['tweet_count'],
            'bio': user_data.get('description', ''),
            'joined': user_data['created_at'][:10],
            'recent_tweets': recent_tweets
        }
    except Exception as e:
        print(f"Error fetching Twitter info: {e}")

    return None

def get_recent_blog_posts():
    """Get recent blog posts from RSS feed or website"""
    try:
        # Try to fetch from actual blog RSS feed
        # Replace this URL with your actual blog RSS feed
        rss_url = "https://howieduhzit.best/rss.xml"  # Update with actual RSS URL

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(rss_url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            posts = []

            # Parse RSS feed
            for item in soup.find_all('item')[:3]:  # Get last 3 posts
                title = item.find('title').text if item.find('title') else 'Untitled'
                link = item.find('link').text if item.find('link') else '#'
                pub_date = item.find('pubDate').text if item.find('pubDate') else ''

                # Extract date
                try:
                    date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                    date_str = date_obj.strftime('%Y-%m-%d')
                except:
                    date_str = 'Recent'

                posts.append({
                    'title': title,
                    'url': link,
                    'date': date_str
                })

            if posts:
                return posts

    except Exception as e:
        print(f"Error fetching blog posts: {e}")

    # Fallback to static content if RSS fails
    return [
        {"title": "Building AI Agents with Eliza Framework", "url": "https://howieduhzit.best/blog/ai-agents-eliza", "date": "2024-12-15"},
        {"title": "3D Workflow Automation with Blender", "url": "https://howieduhzit.best/blog/blender-automation", "date": "2024-12-10"},
        {"title": "Open Source Contributions That Matter", "url": "https://howieduhzit.best/blog/open-source-impact", "date": "2024-12-05"}
    ]

def update_readme():
    """Update the README with dynamic content"""
    # Read current README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    github_token = os.getenv('GITHUB_TOKEN')
    twitter_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not github_token:
        print("No GitHub token available")
        return

    # Get dynamic data
    username = "HowieDuhzit"
    github_stats = get_github_stats(username, github_token)
    twitter_info = get_twitter_info(username, twitter_token) if twitter_token else None
    recent_posts = get_recent_blog_posts()

    # Update GitHub stats section
    if github_stats:
        # Update the activity highlights
        old_highlights = re.search(r'### \*\*🔥 Recent Activity Highlights\*\*\n((?:- .*\n)*)', content, re.MULTILINE)
        if old_highlights:
            new_highlights = "### **🔥 Recent Activity Highlights**\n"
            new_highlights += f"- 🤖 Building AI agent ecosystem with Eliza framework\n"
            new_highlights += f"- 🏗️ Developing 3D modeling tools and Blender addons\n"
            new_highlights += f"- 💻 Creating full-stack web applications and MCP servers\n"
            new_highlights += f"- 🌟 Contributing to open source projects with {github_stats['total_stars']}+ combined stars\n"
            new_highlights += f"- 📊 {github_stats['total_repos']} public repositories, {github_stats['total_forks']} total forks\n"

            content = content.replace(old_highlights.group(0), new_highlights)

        # Update last updated timestamp
        content = re.sub(
            r'\*GitHub stats and detailed metrics will appear here as projects are published! 📈\*',
            f'*GitHub stats and detailed metrics will appear here as projects are published! 📈*\n\n*Last updated: {github_stats["last_updated"]}*',
            content
        )

    # Update Twitter info if available
    if twitter_info:
        # Add Twitter stats to the social section
        twitter_section = f"""
### 🐦 Twitter/X Stats
- **{twitter_info['followers']:,}** followers
- **{twitter_info['tweets']:,}** tweets
- **{twitter_info['following']:,}** following
- Joined {twitter_info['joined']}

*{twitter_info['bio']}*

### 📱 Recent Tweets
"""

        for tweet in twitter_info.get('recent_tweets', []):
            twitter_section += f"- **{tweet['created_at']}**: {tweet['text']}\n"

        twitter_section += "\n---"

        # Insert after the social media links
        social_pattern = r'(## 📫 Connect With Me\n\n<div align="center">.*?</div>\n\n<div align="center">.*?</div>\n\n---)'
        replacement = r'\1\n' + twitter_section + '\n---'
        content = re.sub(social_pattern, replacement, content, flags=re.DOTALL)

    # Update recent blog posts
    blog_section = "## 📝 Latest Blog Posts\n\n<div align=\"center\">\n"
    for post in recent_posts:
        blog_section += f"### [{post['title']}]({post['url']})\n"
        blog_section += f"*Published: {post['date']}*\n\n"
    blog_section += "</div>\n\n*💡 Sharing insights on 3D modeling, game development, and tech innovations*\n\n---"

    # Replace the blog section
    content = re.sub(
        r'## 📝 Latest Blog Posts\n\n.*?\n\n---',
        blog_section,
        content,
        flags=re.DOTALL
    )

    # Write back the updated content
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

    print("README updated with dynamic content!")

if __name__ == "__main__":
    update_readme()
