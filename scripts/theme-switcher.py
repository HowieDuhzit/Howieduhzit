#!/usr/bin/env python3
"""
GitHub Profile Theme Switcher
Easily switch between different themed versions of your profile
"""

import os
import sys
import shutil
import json
from pathlib import Path

class ThemeSwitcher:
    def __init__(self):
        self.themes_dir = Path("themes")
        self.root_dir = Path(".")

    def list_themes(self):
        """List all available themes"""
        if not self.themes_dir.exists():
            print("❌ No themes directory found")
            return []

        themes = []
        for theme_file in self.themes_dir.glob("*-theme.json"):
            theme_name = theme_file.stem.replace("-theme", "")
            themes.append(theme_name)

        return themes

    def get_current_theme(self):
        """Get the currently active theme"""
        # Check if there's a .current_theme file
        current_theme_file = self.root_dir / ".current_theme"
        if current_theme_file.exists():
            return current_theme_file.read_text().strip()
        return "default"

    def set_current_theme(self, theme_name):
        """Set the current theme"""
        current_theme_file = self.root_dir / ".current_theme"
        current_theme_file.write_text(theme_name)

    def load_theme(self, theme_name):
        """Load a specific theme configuration"""
        theme_file = self.themes_dir / f"{theme_name}-theme.json"
        if not theme_file.exists():
            print(f"❌ Theme '{theme_name}' not found")
            return None

        try:
            with open(theme_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading theme '{theme_name}': {e}")
            return None

    def switch_to_theme(self, theme_name):
        """Switch to a specific theme"""
        print(f"🔄 Switching to '{theme_name}' theme...")

        # Load theme configuration
        theme_config = self.load_theme(theme_name)
        if not theme_config:
            return False

        # Copy the themed README
        themed_readme = self.themes_dir / f"{theme_name}-README.md"
        if themed_readme.exists():
            shutil.copy2(themed_readme, self.root_dir / "README.md")
            print(f"✅ Applied {theme_name} README.md")
        else:
            print(f"⚠️ No {theme_name}-README.md found, keeping current README.md")

        # Update current theme
        self.set_current_theme(theme_name)

        print(f"🎉 Successfully switched to '{theme_name}' theme!")
        return True

    def create_theme_from_current(self, theme_name):
        """Create a new theme based on current setup"""
        print(f"📝 Creating '{theme_name}' theme from current setup...")

        # Copy current README as template
        current_readme = self.root_dir / "README.md"
        if current_readme.exists():
            themed_readme = self.themes_dir / f"{theme_name}-README.md"
            shutil.copy2(current_readme, themed_readme)
            print(f"✅ Created {theme_name}-README.md")
        else:
            print("❌ No current README.md found")
            return False

        # Create theme configuration
        theme_config = {
            "name": theme_name.title() + " Theme",
            "description": f"Custom {theme_name} theme for GitHub profile",
            "colors": {
                "primary": "#00FF41",
                "secondary": "#39FF14",
                "accent": "#32CD32",
                "background": "#0a0a0a",
                "surface": "#1a1a1a",
                "text": "#00FF41",
                "textSecondary": "#39FF14",
                "border": "#00FF41"
            },
            "badges": {
                "style": "flat",
                "color": "00FF41",
                "logoColor": "000000"
            }
        }

        # Save theme configuration
        theme_file = self.themes_dir / f"{theme_name}-theme.json"
        with open(theme_file, 'w') as f:
            json.dump(theme_config, f, indent=2)

        print(f"✅ Created {theme_name}-theme.json")
        return True

    def show_status(self):
        """Show current theme status"""
        current_theme = self.get_current_theme()
        available_themes = self.list_themes()

        print("🎨 GitHub Profile Theme Status")
        print(f"📁 Current Theme: {current_theme}")
        print(f"🎯 Available Themes: {', '.join(available_themes)}")

        if current_theme != "default":
            theme_config = self.load_theme(current_theme)
            if theme_config:
                print(f"🎨 Theme Description: {theme_config.get('description', 'No description')}")

def main():
    switcher = ThemeSwitcher()

    if len(sys.argv) < 2:
        switcher.show_status()
        print("\n💡 Usage:")
        print("  python theme-switcher.py list          # List available themes")
        print("  python theme-switcher.py switch <name> # Switch to theme")
        print("  python theme-switcher.py create <name> # Create theme from current")
        print("  python theme-switcher.py status        # Show current status")
        return

    command = sys.argv[1]

    if command == "list":
        themes = switcher.list_themes()
        if themes:
            print("🎨 Available Themes:")
            for theme in themes:
                print(f"  • {theme}")
        else:
            print("❌ No themes found")

    elif command == "switch":
        if len(sys.argv) < 3:
            print("❌ Usage: python theme-switcher.py switch <theme_name>")
            return

        theme_name = sys.argv[2]
        switcher.switch_to_theme(theme_name)

    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ Usage: python theme-switcher.py create <theme_name>")
            return

        theme_name = sys.argv[2]
        switcher.create_theme_from_current(theme_name)

    elif command == "status":
        switcher.show_status()

    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'list', 'switch', 'create', or 'status'")

if __name__ == "__main__":
    main()
