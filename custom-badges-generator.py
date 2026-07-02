#!/usr/bin/env python3
"""
Custom Badge Generator for GitHub Profile
Outputs shields.io badge URLs for funding section.
"""

import urllib.parse

BADGE_COLORS = {
    "dark": "1a1a1a",
    "solana_purple": "9945FF",
    "orange": "FF6B35",
}

FUNDING_BADGES = {
    "buy_me_a_coffee": {
        "url": "https://www.buymeacoffee.com/howieduhzit",
        "label": "Enterprise Consultation",
        "color": BADGE_COLORS["dark"],
        "logo": "buy-me-a-coffee",
        "logo_color": BADGE_COLORS["orange"],
    },
    "github_sponsors": {
        "url": "https://github.com/sponsors/HowieDuhzit",
        "label": "GitHub Sponsors",
        "color": BADGE_COLORS["dark"],
        "logo": "github",
        "logo_color": BADGE_COLORS["orange"],
    },
    "solana_domain": {
        "url": "https://www.sns.id/domain/howieduhzit",
        "label": "howieduhzit.sol",
        "color": BADGE_COLORS["dark"],
        "logo": "solana",
        "logo_color": BADGE_COLORS["solana_purple"],
    },
    "warp_terminal": {
        "url": "https://app.warp.dev/referral/3E9X3D",
        "label": "Warp Terminal Pro",
        "color": BADGE_COLORS["dark"],
        "logo": "visual-studio-code",
        "logo_color": BADGE_COLORS["orange"],
    },
    "crypto_donations": {
        "url": "https://solscan.io/account/HowieDuhzit.sol",
        "label": "SOL Donations",
        "color": BADGE_COLORS["solana_purple"],
        "logo": "solana",
        "logo_color": "ffffff",
    },
}


def create_shields_badge(label, color, logo=None, logo_color=None, style="flat"):
    """Generate a shields.io badge URL."""
    base_url = "https://img.shields.io/badge"
    params = []
    if label:
        params.append(f"label={urllib.parse.quote(label)}")
    if color:
        params.append(f"color={color}")
    if logo:
        params.append(f"logo={logo}")
    if logo_color:
        params.append(f"logoColor={logo_color}")
    if style:
        params.append(f"style={style}")
    return f"{base_url}?{'&'.join(params)}"


def generate_all():
    """Print all funding badges in markdown format."""
    for name, config in FUNDING_BADGES.items():
        badge_url = create_shields_badge(
            label=config["label"],
            color=config["color"],
            logo=config["logo"],
            logo_color=config["logo_color"],
            style="for-the-badge",
        )
        print(f"[![{config['label']}]({badge_url})]({config['url']})")
    print()


if __name__ == "__main__":
    generate_all()
