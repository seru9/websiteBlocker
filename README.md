# Python Website Blocker

A lightweight Python GUI application that helps you stay productive by blocking distracting websites during specific hours of the day. It works by modifying the system `hosts` file to redirect specified URLs to `127.0.0.1`.
=
## ✨ Features

* **Customizable Blocklist:** Add or remove websites (e.g., Facebook, YouTube, X) via the interface.
* **Time-Based Blocking:** Set your "Work Hours" using a 24-hour clock. The blocker automatically enables and disables based on your system time.
* **User-Friendly GUI:** Built with Tkinter for a simple, responsive experience.
* **Threaded Background Process:** The blocking logic runs on a background thread, ensuring the GUI never freezes.

## 📸 Preview

* **Start Hour:** When the blocking begins (e.g., `8` for 8:00 AM).
* **End Hour:** When the websites become accessible again (e.g., `17` for 5:00 PM).

## 🚀 Installation & Usage

### Prerequisites
* Python 3.x installed.
* **Windows OS** (The current path is configured for `C:\Windows\System32\drivers\etc\hosts`).

### Setup
1. Clone this repository:
   ```bash
   git clone [https://github.com/yourusername/website-blocker-gui.git](https://github.com/yourusername/website-blocker-gui.git)
   cd website-blocker-gui
2. For Windows open cmd in admin mode!
