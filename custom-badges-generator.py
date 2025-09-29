#!/usr/bin/env python3
"""
Custom Badge Generator for GitHub Profile
Creates custom funding badges with specific icons and styling
"""

import urllib.parse
import json
from pathlib import Path

def create_shields_badge(label, message, color, logo=None, logo_color=None, style="flat"):
    """
    Generate a shields.io badge URL with custom parameters
    """
    base_url = "https://img.shields.io/badge"

    # Build query parameters
    params = []
    if label:
        params.append(f"label={urllib.parse.quote(label)}")
    if message:
        params.append(f"message={urllib.parse.quote(message)}")
    if color:
        params.append(f"color={color}")
    if logo:
        params.append(f"logo={logo}")
    if logo_color:
        params.append(f"logoColor={logo_color}")
    if style:
        params.append(f"style={style}")

    query_string = "&".join(params)
    return f"{base_url}?{query_string}"

def load_theme_config(theme_name="default"):
    """Load theme configuration"""
    try:
        theme_file = Path(f"themes/{theme_name}-theme.json")
        if theme_file.exists():
            with open(theme_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Could not load theme '{theme_name}': {e}")

    # Default theme
    return {
        "colors": {
            "primary": "#FF6B35",
            "secondary": "#9945FF",
            "accent": "#00FF41"
        },
        "badges": {
            "style": "for-the-badge",
            "color": "1a1a1a"
        }
    }

def create_funding_badges(theme="default"):
    """Generate all funding badges for the profile with theme support"""

    theme_config = load_theme_config(theme)
    colors = theme_config.get("colors", {})
    badge_style = theme_config.get("badges", {}).get("style", "for-the-badge")
    badge_color = theme_config.get("badges", {}).get("color", "1a1a1a")

    badges = {
        "buy_me_a_coffee": {
            "url": "https://www.buymeacoffee.com/howieduhzit",
            "label": "Enterprise Consultation",
            "color": badge_color,
            "logo": "buy-me-a-coffee",
            "logo_color": colors.get("primary", "FF6B35"),
            "style": badge_style
        },
        "github_sponsors": {
            "url": "https://github.com/sponsors/HowieDuhzit",
            "label": "GitHub Sponsors",
            "color": badge_color,
            "logo": "github",
            "logo_color": colors.get("primary", "FF6B35"),
            "style": badge_style
        },
        "solana_domain": {
            "url": "https://www.sns.id/domain/howieduhzit",
            "label": "howieduhzit.sol",
            "color": badge_color,
            "logo": "solana",
            "logo_color": colors.get("secondary", "9945FF"),
            "style": badge_style
        },
        "warp_terminal": {
            "url": "https://app.warp.dev/referral/3E9X3D",
            "label": "Warp Terminal Pro",
            "color": badge_color,
            "logo": "visual-studio-code",
            "logo_color": colors.get("primary", "FF6B35"),
            "style": badge_style
        },
        "ai_consultation": {
            "url": "mailto:Contact@HowieDuhzit.Best",
            "label": "AI Engineering Consultation",
            "color": badge_color,
            "logo": "robot",
            "logo_color": colors.get("primary", "FF6B35"),
            "style": badge_style
        }
    }

    # Terminal theme specific badges
    if theme == "terminal":
        badges.update({
            "mainframe": {
                "url": "https://howieduhzit.best",
                "label": "Mainframe",
                "color": "00FF41",
                "logo": "server",
                "logo_color": "000000",
                "style": badge_style
            },
            "network": {
                "url": "https://twitter.com/HowieDuhzit",
                "label": "Network",
                "color": "00FF41",
                "logo": "twitter",
                "logo_color": "000000",
                "style": badge_style
            }
        })

    return badges

def create_custom_badge_example():
    """Example of creating a completely custom badge"""

    # Custom engineering consultation badge
    custom_badge = create_shields_badge(
        label="AI Engineering",
        message="Consultation",
        color="FF6B35",
        logo="robot",
        logo_color="ffffff",
        style="for-the-badge"
    )

    print(f"\n🔧 Custom Badge Example:")
    print(f"Badge URL: {custom_badge}")
    print(f"Usage: <img src=\"{custom_badge}\" alt=\"AI Engineering Consultation\" />")

if __name__ == "__main__":
    import sys

    # Support theme-based badge generation
    theme = sys.argv[1] if len(sys.argv) > 1 else "default"
    print(f"🎨 Generating badges for '{theme}' theme...")
    badges = create_funding_badges(theme)

    for name, config in badges.items():
        badge_url = create_shields_badge(
            label=config["label"],
            message=None,
            color=config["color"],
            logo=config["logo"],
            logo_color=config["logo_color"],
            style=config["style"]
        )

        print(f"\n📌 {name.upper()}:")
        print(f"URL: {config['url']}")
        print(f"Badge: <img src=\"{badge_url}\" alt=\"{config['label']}\" />")
        print(f"Markdown: [![{config['label']}]({config['url']})]({config['url']})")

    create_custom_badge_example()
