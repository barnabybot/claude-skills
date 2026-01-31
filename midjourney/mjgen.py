#!/usr/bin/env python3
"""
Midjourney Alpha Portrait Generator for Obsidian People
Automates Midjourney web interface to generate watercolor portraits
"""

import asyncio
import os
import sys
import json
import re
import time
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Configuration
MIDJOURNEY_URL = "https://alpha.midjourney.com/imagine"
USER_DATA_DIR = Path.home() / ".midjourney-automation"
ATTACHMENTS_DIR = Path("/Users/barnabyrobson/Library/Mobile Documents/iCloud~md~obsidian/Documents/Core/Attachments")
PEOPLE_DIR = Path("/Users/barnabyrobson/Library/Mobile Documents/iCloud~md~obsidian/Documents/Core/References/People")

# People to generate portraits for
PEOPLE_TO_GENERATE = [
    "Anne Lamott",
    "Antoine de St. Exupery",
    "Aristotle",
    "Aristotle Onassis",
    "Benjamin Franklin",
    "Cathy Wood",
    "Chris Dixon",
    "Christopher Hitchens",
    "David Allen",
    "David Friedberg",
    "Euripides",
    "Franklin D. Roosevelt",
    "Heraclitus",
    "Homer",
    "Immanuel Kant",
    "Isaac Asimov",
    "Jerzy Gregorek",
    "Jim Carrey",
    "Jocko Willink",
    "John Davison Rockefeller",
    "John Locke",
    "John Maynard Keynes",
    "John Stuart Mill",
    "John Templeton",
    "Karl Marx",
    "Lao Tzu",
    "Leonardo da Vinci",
    "Mark Twain",
    "Martin Luther King",
    "Matthew Arnold",
    "Michael Dell",
    "Neil Gaiman",
    "Niccolò Machiavelli",
    "Patrick J. Deneen",
    "Paul Graham",
    "Paulo Coelho",
    "Plato",
    "Pythagoras",
    "Rene Descartes",
    "Robert Frost",
    "Roelof Botha",
    "Socrates",
    "Stephen Fry",
    "Terry Pratchett",
    "Theodore Roosevelt",
    "Thomas Aquinas",
    "Tiago Forte",
    "Tony Robbins",
    "Voltaire",
    "Walter Isaacson",
    "Warren Buffett",
    "William Butler Yeats",
    "William James",
    "William Shakespeare",
    "Winston Churchill",
    "Zeno of Citium",
]

# Simple Quentin Blake style prompt
def get_prompt(person_name: str) -> str:
    """Generate Midjourney prompt for a person"""
    return f"{person_name} painted by Quentin Blake --ar 1:1 --s 150"


def already_has_image(person_name: str) -> bool:
    """Check if person already has a feature image (in markdown OR as file)"""
    # First check if image file already exists in Attachments
    image_file = ATTACHMENTS_DIR / f"{person_name}.png"
    if image_file.exists():
        return True

    # Then check markdown file for feature property
    person_file = PEOPLE_DIR / f"{person_name}.md"
    if not person_file.exists():
        return False
    content = person_file.read_text()
    # Check for feature: with a value
    match = re.search(r'^feature:[^\S\n]*(\S.*)$', content, re.MULTILINE)
    return match is not None


async def setup_browser(headless: bool = False):
    """Launch browser with persistent context for auth"""
    USER_DATA_DIR.mkdir(exist_ok=True)

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        headless=headless,
        viewport={"width": 1400, "height": 900},
        args=["--disable-blink-features=AutomationControlled"]
    )
    return playwright, browser


async def login_to_midjourney():
    """Interactive login - opens browser for user to log in"""
    print("🔐 Opening Midjourney Alpha for login...")
    print("   Please log in with your Midjourney account.")

    playwright, browser = await setup_browser(headless=False)
    page = await browser.new_page()

    await page.goto(MIDJOURNEY_URL)

    signal_file = USER_DATA_DIR / "ready.signal"
    signal_file.unlink(missing_ok=True)

    print(f"\n✅ Complete the login process, then either:")
    print(f"   - Run in another terminal: touch '{signal_file}'")
    print(f"   - Or wait 120 seconds after reaching the imagine page")
    print(f"\n   (Browser will stay open for OAuth popups)")

    # Wait for signal file OR timeout after user is on imagine page
    start_time = time.time()
    logged_in_time = None

    while True:
        # Check for signal file
        if signal_file.exists():
            signal_file.unlink()
            print("📍 Signal received!")
            break

        # Check if we're on the imagine page (logged in)
        try:
            current_url = page.url
            if 'alpha.midjourney.com' in current_url and '/imagine' in current_url:
                if logged_in_time is None:
                    logged_in_time = time.time()
                    print("📍 Detected imagine page - waiting 30s for you to verify...")
                elif time.time() - logged_in_time > 30:
                    print("📍 Auto-completing after 30s on imagine page")
                    break
        except:
            pass  # Page might be navigating

        # Safety timeout after 5 minutes
        if time.time() - start_time > 300:
            print("⏰ Timeout after 5 minutes")
            break

        await asyncio.sleep(2)

    # Save config indicating login complete
    config = {"logged_in": True, "timestamp": time.time()}
    config_file = USER_DATA_DIR / "config.json"
    config_file.write_text(json.dumps(config))
    print(f"💾 Session saved to {USER_DATA_DIR}")

    try:
        await browser.close()
    except:
        pass
    await playwright.stop()

    print("✅ Login session saved! You can now run in automated mode.")


async def send_prompt(page, prompt: str) -> int:
    """Send a prompt to Midjourney Alpha. Returns current image count for tracking."""
    try:
        # Count existing images before submitting
        existing_images = page.locator('img[src*="cdn.midjourney.com"]')
        initial_count = await existing_images.count()
        print(f"   📊 {initial_count} existing images")

        # Find the prompt input
        prompt_input = page.locator('textarea, input[type="text"]').first
        await prompt_input.wait_for(state="visible", timeout=10000)

        # Clear and type prompt (fast fill, not slow typing)
        await prompt_input.click()
        await prompt_input.fill(prompt)
        await asyncio.sleep(0.3)

        # Dismiss any suggestion dropdown that might interfere
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.2)

        # Re-focus the input and submit with Enter (this is how MJ Alpha works)
        await prompt_input.click()
        await asyncio.sleep(0.2)
        await page.keyboard.press("Enter")
        print(f"   ⌨️ Submitted with Enter")

        await asyncio.sleep(2)

        # Quick verify: count should change or progress indicator should appear
        new_count = await existing_images.count()
        if new_count != initial_count:
            print(f"   ✅ Immediate response! ({initial_count} → {new_count})")

        return initial_count

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return -1


async def wait_for_generation(page, wait_seconds: int = 60):
    """Wait fixed time for MJ to generate, then return first image"""
    print(f"   ⏳ Waiting {wait_seconds}s for generation...")

    # Wait in chunks, showing progress
    for elapsed in range(0, wait_seconds, 10):
        await asyncio.sleep(10)
        print(f"   ⏳ {elapsed + 10}s...")

    # Scroll to top to ensure new images are loaded
    await page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(2)

    # Get first image (newest, at top)
    images = page.locator('img[src*="cdn.midjourney.com"]')
    count = await images.count()
    print(f"   ✅ Done waiting. {count} images visible.")

    if count > 0:
        return images.first
    return None


async def download_image(img_element, person_name: str, page) -> Path | None:
    """Click image to open large view, screenshot the largest image"""
    try:
        output_path = ATTACHMENTS_DIR / f"{person_name}.png"

        # Click thumbnail to open larger view
        print(f"   🖱️ Opening image...")
        await img_element.click()
        await asyncio.sleep(3)

        # Find the largest visible MJ image
        imgs = page.locator('img[src*="cdn.midjourney.com"]')
        count = await imgs.count()

        best_img = None
        max_size = 0

        for i in range(count):
            img = imgs.nth(i)
            try:
                if await img.is_visible(timeout=500):
                    box = await img.bounding_box()
                    if box:
                        size = box['width'] * box['height']
                        if size > max_size:
                            max_size = size
                            best_img = img
            except:
                continue

        if best_img:
            box = await best_img.bounding_box()
            print(f"   📐 Found {int(box['width'])}x{int(box['height'])} image")
            await best_img.screenshot(path=str(output_path))
            print(f"   💾 Saved: {output_path.name}")
        else:
            print(f"   ⚠️ No large image found, using thumbnail")
            await img_element.screenshot(path=str(output_path))

        # Close modal
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)

        return output_path

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def update_person_file(person_name: str, image_filename: str):
    """Update the person's markdown file with the feature image"""
    person_file = PEOPLE_DIR / f"{person_name}.md"
    if not person_file.exists():
        print(f"   ⚠️ Person file not found: {person_file}")
        return

    content = person_file.read_text()

    # Update or add feature property
    if re.search(r'^feature:\s*$', content, re.MULTILINE):
        content = re.sub(
            r'^feature:\s*$',
            f'feature: Attachments/{image_filename}',
            content,
            flags=re.MULTILINE
        )
    elif 'feature:' in content:
        content = re.sub(
            r'^feature:.*$',
            f'feature: Attachments/{image_filename}',
            content,
            flags=re.MULTILINE
        )
    else:
        content = re.sub(
            r'(categories:.*?\n(?:  - .*\n)*)',
            f'\\1feature: Attachments/{image_filename}\n',
            content
        )

    person_file.write_text(content)
    print(f"   📝 Updated {person_file.name}")


async def generate_portrait(page, person_name: str, debug: bool = False) -> bool:
    """Generate a single portrait"""
    prompt = get_prompt(person_name)
    print(f"   📝 {prompt}")

    # Navigate to imagine page
    await page.goto(MIDJOURNEY_URL)
    await asyncio.sleep(2)

    # Send prompt
    result = await send_prompt(page, prompt)
    if result < 0:
        return False

    # Debug: screenshot after submission
    if debug:
        await page.screenshot(path="/tmp/mj_debug_after_submit.png")
        print(f"   📸 Debug: /tmp/mj_debug_after_submit.png")

    # Wait fixed time for generation (60s)
    img_element = await wait_for_generation(page, wait_seconds=60)

    if img_element:
        saved_path = await download_image(img_element, person_name, page)
        if saved_path:
            update_person_file(person_name, saved_path.name)
            return True

    return False


async def generate_portraits(people: list[str], headless: bool = False):
    """Main function to generate portraits for a list of people"""

    config_file = USER_DATA_DIR / "config.json"
    if not config_file.exists():
        print("❌ No saved session found. Run with --login first.")
        return

    print(f"🚀 Starting portrait generation for {len(people)} people")
    print(f"📍 Using Midjourney Alpha: {MIDJOURNEY_URL}\n")

    # Filter out people who already have images
    people_to_do = [p for p in people if not already_has_image(p)]
    print(f"📋 {len(people_to_do)} people need portraits ({len(people) - len(people_to_do)} already have images)\n")

    if not people_to_do:
        print("✅ All people already have images!")
        return

    playwright, browser = await setup_browser(headless=headless)
    page = await browser.new_page()

    successful = 0
    failed = 0

    try:
        await page.goto(MIDJOURNEY_URL)
        await asyncio.sleep(5)

        for i, person in enumerate(people_to_do):
            print(f"\n[{i+1}/{len(people_to_do)}] {person}")

            if await generate_portrait(page, person):
                successful += 1
            else:
                failed += 1

            # Rate limiting
            if i < len(people_to_do) - 1:
                print(f"   ⏳ Waiting 10s before next...")
                await asyncio.sleep(10)

    finally:
        await browser.close()
        await playwright.stop()

    print(f"\n✅ Done! {successful} successful, {failed} failed")


async def test_single(person_name: str):
    """Test generation for a single person"""
    config_file = USER_DATA_DIR / "config.json"
    if not config_file.exists():
        print("❌ No saved session found. Run with --login first.")
        return

    playwright, browser = await setup_browser(headless=False)
    page = await browser.new_page()

    try:
        print(f"🧪 Testing with: {person_name}")
        await page.goto(MIDJOURNEY_URL)
        await asyncio.sleep(3)

        success = await generate_portrait(page, person_name, debug=True)

        if success:
            print(f"\n✅ Test successful!")
        else:
            print(f"\n❌ Test failed")

    finally:
        await browser.close()
        await playwright.stop()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Midjourney portraits for Obsidian People")
    parser.add_argument("--login", action="store_true", help="Interactive login to Midjourney")
    parser.add_argument("--test", type=str, help="Test with a single person name")
    parser.add_argument("--all", action="store_true", help="Generate all missing portraits")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (after testing)")
    parser.add_argument("--list", action="store_true", help="List people needing portraits")

    args = parser.parse_args()

    if args.login:
        asyncio.run(login_to_midjourney())
    elif args.test:
        asyncio.run(test_single(args.test))
    elif args.all:
        asyncio.run(generate_portraits(PEOPLE_TO_GENERATE, headless=args.headless))
    elif args.list:
        need_portraits = [p for p in PEOPLE_TO_GENERATE if not already_has_image(p)]
        print(f"People needing portraits ({len(need_portraits)}):")
        for p in need_portraits:
            print(f"  - {p}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
