# Clan Monitor - Ninja Kaizen

This is a Python-based bot developed to track and audit the real-time activity, attacks, and statistics of all my clan members in **Ninja Kaizen**. The system automates data scraping from the game's website, stores the history locally, and reports everything in an organized manner to our Discord server.

---

# Why did I create this project?

Managing a competitive clan manually is a headache. I needed to automate the tracking of battles and the daily status of each member without having to check the game's website all the time. 

This monitor does the heavy lifting for me every 6 seconds, ensuring no data is lost and keeping the entire team aligned through automated alerts.

---

# What this system does

- **Automated Scraping:** Connects to the official Ninja Kaizen website and extracts clean player data during each cycle.
- **Local Database (SQLite):** Stores the status of the members to maintain a reliable historical record. I use **DB Browser for SQLite** to verify the database structure and queries.
- **Discord Alerts:** Sends formatted reports directly to the clan channels using Webhooks.
- **Credential Security:** Secret Discord URLs and sensitive data are not exposed in the code; they are handled securely and hidden in a local `.env` file for cybersecurity.

---

# Technical Challenges and Solution (Network Stability)

During initial testing, the script opened and closed individual network connections on every loop. This saturated Windows network sockets and caused constant crashes due to remote server blocks (such as Error 10054).

**The Solution:** I refactored the connection to implement a **Persistent Network Tunnel (`requests.Session()`)**. By keeping the communication pipeline open (Keep-Alive), the bot no longer forces the network on every cycle. This completely eliminated disconnection errors, lowered CPU usage on my local computer, and stabilized mass reporting to Discord.

---

# Project Files

- `monitor_clan.py`: Main code containing the bot logic, network requests, and database storage.
- `clan_data.sqbpro`: DB Browser configuration file for managing SQLite tables.
- `.gitignore`: Essential filter to prevent Git from uploading my actual database (`.db`) or my private passwords (`.env`) to GitHub.

---
Developed by **nolandev**
