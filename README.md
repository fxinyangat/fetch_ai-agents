### Below is the structure of the project:
Hacka3/
├── README.md
├── frontend/                # React.js frontend
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── TranslationPage.js # Core page for translation
│   │   ├── components/
│   │   │   └── LanguageSelect.js # Language dropdown component
│   │   └── styles/          # Styling files
├── agents/                  # Fetch.ai agents
│   ├── student_agent/       # Manages user preferences and requests
│   │   ├── student_agent.py
│   │   └── config.json
│   ├── broker_agent/        # Negotiates with service agents
│   │   ├── broker_agent.py
│   │   └── config.json
│   ├── service_agents/      # Mock service agents for translation
│   │   ├── translation_agent.py
│   │   └── config.json
└── .env                     # Environment variables