#!/usr/bin/env python3
"""
Custom Badge Generator for GitHub Profile
Creates custom funding badges with specific icons and styling
"""

import urllib.parse
import json

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

def create_funding_badges():
    """Generate all funding badges for the profile"""

    badges = {
        "buy_me_a_coffee": {
            "url": "https://www.buymeacoffee.com/howieduhzit",
            "label": "Enterprise Consultation",
            "color": "1a1a1a",
            "logo": "buy-me-a-coffee",
            "logo_color": "FF6B35"
        },
        "github_sponsors": {
            "url": "https://github.com/sponsors/HowieDuhzit",
            "label": "GitHub Sponsors",
            "color": "1a1a1a",
            "logo": "github",
            "logo_color": "FF6B35"
        },
        "solana_domain": {
            "url": "https://www.sns.id/domain/howieduhzit",
            "label": "howieduhzit.sol",
            "color": "1a1a1a",
            "logo": "solana",
            "logo_color": "9945FF"
        },
        "warp_terminal": {
            "url": "https://app.warp.dev/referral/3E9X3D",
            "label": "Warp Terminal Pro",
            "color": "1a1a1a",
            "logo": "visual-studio-code",
            "logo_color": "FF6B35"
        },
        "crypto_donations": {
            "url": "https://solscan.io/account/HowieDuhzit.sol",
            "label": "SOL Donations",
            "color": "9945FF",
            "logo": "solana",
            "logo_color": "ffffff"
        }
    }

    print("🎨 Custom Funding Badges Generator")
    print("=" * 50)

    for name, config in badges.items():
        badge_url = create_shields_badge(
            label=config["label"],
            message=None,  # We're using label only for button style
            color=config["color"],
            logo=config["logo"],
            logo_color=config["logo_color"],
            style="for-the-badge"
        )

        print(f"\n📌 {name.upper()}:")
        print(f"URL: {config['url']}")
        print(f"Badge: <img src=\"{badge_url}\" alt=\"{config['label']}\" />")
        print(f"Markdown: [![{config['label']}]({config['url']})]({config['url']})")

    print("\n" + "=" * 50)
    print("💡 Usage Tips:")
    print("• Use 'for-the-badge' style for buttons")
    print("• Use 'flat' style for smaller badges")
    print("• Customize colors with hex codes")
    print("• Use any logo from simpleicons.org")

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
    create_funding_badges()
    create_custom_badge_example()
