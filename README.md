<p align="center">
  <img src="assets/logo.png" alt="Twilio CLI Manager Logo" width="200" />
</p>

<h1 align="center">Twilio CLI Manager</h1>

A Python-based wrapper around the Twilio SDK, built in just 3 days using AI helpers (OpenHands, Claude, ChatGPT). This functional CLI tool lets you search, purchase, release, and configure phone numbers; send and view messages; place and manage calls; and inspect your Twilio account—all from the terminal. Future plans include a GUI (web & desktop), a `pip`-installable package with full `argparse` support, and seamless command-line integration.

---

## 📋 Table of Contents

- [Features](#-features)  
- [Prerequisites](#-prerequisites)  
- [Installation](#-installation)  
- [Configuration](#-configuration)  
- [Usage](#-usage)  
- [Logging](#-logging)  
- [Testing](#-testing)  
- [Development](#-development)  
- [Roadmap](#-roadmap)  
- [Contributing](#-contributing)  
- [License](#-license)  

---

## 🔍 Features

**Phone Number Management**  
- 🔍 Search available numbers by region, area code, or custom pattern  
- 📊 View paginated search results  
- 🛒 Purchase a phone number  
- 🗑 Release a phone number  
- ⚙️ Configure number capabilities (SMS, MMS, voice, etc.)

**Messaging**  
- ✉️ Send SMS messages  
- 📄 View message logs  

**Voice**  
- 📞 Make voice calls  
- 🗂 View call logs & subaccounts  
- 🎤 Record calls & manage recordings  
- 🔗 Join or create conferences  
- 🔊 Manage SIP trunks & TwiML applications  

**Account Management**  
- 👤 View account info & balance  
- 👥 List subaccounts  
- 🔑 Manage API Keys  

---

## 🚀 Prerequisites

- **Python 3.10+**  
- A **Twilio account** with your **Account SID** and **Auth Token**  
- Terminal/CLI on macOS, Linux, or Windows  
- (Optional) [Poetry](https://python-poetry.org/) or `venv` for virtual environments  

---

## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/h1n054ur/twilio-cli-manager.git
   cd twilio-cli-manager
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .\.venv\Scripts\activate     # Windows PowerShell
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Configuration

1. Copy the example environment file and set your Twilio credentials:  
   ```bash
   cp .env.example .env
   ```
2. Edit `.env`:
   ```ini
   TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   TWILIO_AUTH_TOKEN=your_auth_token_here
   ```

> ⚠️ The app will raise an error if `TWILIO_ACCOUNT_SID` or `TWILIO_AUTH_TOKEN` are missing.

---

## 💻 Usage

Launch the CLI from the project root:

```bash
python -m twilio_manager.cli.main
```

Or, once packaged in the future:

```bash
twilio-cli-manager --help
```

Follow on-screen prompts to navigate menus. For direct commands, you can also run (after adding entry-points):

```bash
twilio-manager search           # Search available numbers
twilio-manager purchase         # Purchase a phone number
twilio-manager send-message     # Send an SMS
twilio-manager make-call        # Place a voice call
```

*(Exact command names will be finalized when the package is published.)*

---

## 📝 Logging

All runtime logs (info, warnings, errors) are written to `logs/app.log` by default. Use this file for troubleshooting:

```bash
tail -f logs/app.log
```

---

## ✅ Testing

Run the full test suite with [pytest](https://docs.pytest.org/):

```bash
pytest
```

- `tests/` covers core functionality, services, and CLI menus.  
- `tests/requirements-test.txt` lists any additional test-specific dependencies.

---

## 🛣 Roadmap

- **GUI Versions**  
  - Web App (React + Flask or FastAPI backend)  
  - Desktop App (PyInstaller → `.exe`)

- **Packaging**  
  - Publish on PyPI: `pip install twilio-cli-manager`  
  - Full `argparse` support for non-interactive workflows  

- **Enhancements**  
  - Advanced filtering & batch operations  
  - Webhooks & real-time notifications  
  - OAuth2-based credential management  

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  

1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/foo`)  
3. Commit your changes (`git commit -m "feat: add foo"`)  
4. Push (`git push origin feature/foo`)  
5. Open a Pull Request  

Please follow [PEP 8](https://peps.python.org/pep-0008/) and include tests for any new functionality.

---

## 📄 License

This project is released under the **MIT License**. See [LICENSE](./LICENSE) for details.
``` ````
