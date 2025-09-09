# Repository: whatsapp_calendar_automation


Below is a production-ready, modular Python project that:
- Sends daily agendas (1:1) via WhatsApp.
- Lets the user add events to Google Calendar by sending a standard WhatsApp message.
- Exposes a webhook to receive WhatsApp updates and auto-create/edit Calendar events.
- Allows editing events by Calendar Event ID.
- Automatically sends the agenda each morning at the time configured by the user (via a scheduled HTTP trigger).
- Can be hosted on a free tier (Vercel Hobby) with zero infra cost; note that WhatsApp Cloud API may charge per message — the system is designed to minimize usage.
- Includes a per-user setup script that collects the phone number, performs Google OAuth, and deploys to Vercel.
- Uses only free/open libraries.
- Emphasizes security, scalability, and future extensibility.


> Tip: You can also run this on Railway/Render with a simple `Dockerfile`. Vercel is shown by default for easy free scheduling via **Vercel Cron**.


---


## Project Tree
```
whatsapp_calendar_automation/
├─ app/
│ ├─ __init__.py
│ ├─ main.py # FastAPI app & routes
│ ├─ config.py # Settings provider
│ ├─ domain/
│ │ ├─ models.py # Pydantic models / value objects
│ │ └─ parsers.py # Message → Event parser
│ ├─ services/
│ │ ├─ calendar_service.py # Google Calendar operations (POO)
│ │ ├─ whatsapp_service.py # WhatsApp Cloud API client (POO)
│ │ ├─ agenda_service.py # Builds agenda messages (POO)
│ │ └─ security.py # Webhook validation / signature checks
│ ├─ tasks/
│ │ └─ daily_agenda.py # Orchestrates the daily send (called by cron)
│ └─ utils/
│ └─ logging.py # Structured logging helper
├─ scripts/
│ ├─ setup.py # Interactive installer (per-user)
│ └─ deploy_vercel.sh # Zero-click-ish deploy to Vercel
├─ requirements.txt
├─ runtime.txt # For some hosts that require runtime pin
├─ vercel.json # Vercel routes + Cron
├─ .env.example
├─ Dockerfile # For Railway/Render alternative
└─ README.md
```