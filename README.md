Run this in terminal: watchmedo auto-restart --patterns="*.py" --recursive -- python src/main.py

Or: python -m watchdog.watchmedo auto-restart --patterns="*.py" --recursive -- python main.py       

Needed to add:
- cloud database
- email verification
- Dynamic GSheet link import (new gsheet link -> import data to settings config)
 
 <h1>MedRX Inventory System</h1>
 Developed and Architectured by: YesuDesu21 (Feil Jasper Doria)

<h2>2. About the Project</h2>
Description: This project was primarily built to make invnetory inspection much easier in my family business. It was also to allow me to integrate my learnings from college and personal research.

Tech Stack:
- Program: Python and Custom Tkinter
- Data Analysis: Pandas, Matplotlib
- Database: Sqlite
- Cloud: Google Sheets API, Supabase

<h2>3. Getting Started</h2>

Prerequisites: everything is under @requirements.txt. 
Run: pip install -r requirements.txt
or
python -m pip install -r requirements.txt

Bash
git clone https://github.com/YesuDesu21/MedRX-Inventory-System/tree/main

<h2>4. Usage</h2>
Local Development: How to run the dev server (e.g., npm run dev).

Examples: Code snippets showing the basic API or UI interaction.

Configuration: List of Environment Variables (.env file requirements).

<h2>5. Roadmap & Features</h2>
Features: 
1. Visual Dashboard that works in real time
2. Ability to [CRUD] inventory items
3. Ability to [CRUD] transactions
4. Ability to see logs


<h2>6. Architecture</h2>
Guidelines: How can others help? (Link to CONTRIBUTING.md if it’s long).

File Structure:

```
MedRX-Inventory-System/
├── assets/          # Icons, images, and UI resources
├── cloud/           # Cloud integration logic (Supabase)
├── data/            # Local SQLite database files
├── docs/            # Project documentation
├── logs/            # Application runtime logs
├── notebooks/       # Jupyter notebooks for testing/data analysis
├── src/             # Source code (modules and logic)
├── .env             # Environment variables (API keys, secrets)
├── .gitignore       # Files to be ignored by Git
├── credentials.json  # Google Cloud/API credentials
├── main.py          # Application entry point
├── README.md        # Project overview and documentation
└── requirements.txt # Python dependencies
```

![Flow Diagram](/docs/flow_diagram.png)

<h2>7. Testing</h2>
How to run the test suite (e.g., pytest or jest).

Mention the types of tests included (Unit, Integration, E2E).

<h2>8. License & Contact</h2>
License: State the license (MIT, Apache 2.0, etc.).

Linkedin: https://www.linkedin.com/in/feil-jasper-doria-b4a3a8318/

<h2>9. Docs</h2>
https://docs.google.com/document/d/130f9qzljseilO18wmqOkCBMm38OBdINmIgFiVlDN94Y/edit?tab=t.0
