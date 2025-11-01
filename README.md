<h1 align="center">🚀 Instagram Session Extractor (Ultra Fast)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat&logo=github" alt="Project Status">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Automation-Selenium-orange?logo=selenium" alt="Automation">
</p>

<p align="center">
  ⚡ A fast Python tool to detect and report active Instagram sessions from Brave browser profiles ⚡  
</p>

---

### ✨ Features
- 🧭 **Automatic Profile Detection:** Scans all Brave user profiles and finds valid ones.  
- 🔐 **Session Status Check:** Detects whether each profile is logged in to Instagram.  
- 📦 **Data Extraction:** Collects essential session and cookie data for logged-in profiles.  
- ⚡ **Fast Execution:** Optimized for speed with headless mode and lightweight browser settings.  
- 📧 **Automated Reporting:** Generates structured JSON reports and optionally emails them.  
- 🧹 **Cleanup Utilities:** Forcefully closes Brave and ChromeDriver processes to avoid conflicts.  

---

### 🛠️ Tech Stack
- 💻 **Language:** Python  
- 🧩 **Libraries:** Selenium, psutil, smtplib, json, shutil  
- 🌐 **Browser:** Brave (Chromium-based)  
- 📬 **Email Integration:** Gmail SMTP  

---

### 📋 Usage
1. 🧱 Install Brave Browser if not already installed.  
2. 🔑 Log in to Instagram using your desired Brave profile.  
3. 🚫 Close Brave completely before running the script.  
4. ▶️ Run the script from your terminal or IDE.  
5. 💾 View collected data in the `instagram_profiles_data` folder or check your email for the report.  

---

### ⚠️ Disclaimer
This project is for **educational and automation testing purposes only**.  
It does **not** collect, transmit, or misuse personal data.  
Use responsibly and only on systems and accounts you own.  

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/MehtabAli093">Mehtab Ali</a> • 
  📧 <a href="mailto:mehtabahmed093@gmail.com">prodark093@gmail.com</a>
</p>

---

### 🧠 How It Works

The script automates the process of checking whether Brave browser profiles contain active Instagram sessions.

#### 1. 🧹 Cleanup
It starts by forcefully killing all existing Brave and ChromeDriver processes to avoid conflicts and ensure a clean run.

#### 2. 🔍 Profile Detection
The script scans the Brave user data directory (`AppData\Local\BraveSoftware\Brave-Browser\User Data`) and lists all valid profiles such as **Default**, **Profile 1**, **Profile 2**, etc.

#### 3. ⚙️ WebDriver Setup
For each profile, it launches Brave in **headless mode** using Selenium with aggressive performance optimizations — JavaScript, plugins, and images are disabled for faster execution.

#### 4. 🌐 Instagram Session Check
It navigates to `https://www.instagram.com/` and performs a quick login status check by:
- Looking for session cookies like `sessionid`
- Checking the current URL (login page or not)
- Inspecting the DOM for navigation elements

#### 5. 📦 Data Extraction
If a valid session is found, the script extracts:
- Cookie names and values  
- Profile name  
- Timestamp  
- Active session count  

It saves this data as a JSON file inside the `instagram_profiles_data` directory.

#### 6. 📧 Email Reporting
Once all profiles are processed:
- It compiles all data into a single JSON report.  
- Sends the report to the configured Gmail address using **SMTP with TLS**.  

#### 7. 📊 Summary Output
Finally, it displays a summary showing:
- Number of profiles scanned  
- Number of active sessions found  
- Total execution time  

---

### 🧩 Example Output (Console)
