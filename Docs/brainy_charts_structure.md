# BrainyCharts Project Structure

```bash
BrainyCharts/
│
├── brainy_charts/            # All wrapper functionalities and application logic
│   │
│   ├── __init__.py
│   │
│   ├── brainy_charts.py      # Wrapper of the charting library
│   │
│   ├── chart_data.py         # Data handler to be used via the brainy_chart
│   │
│   └── backend/
│       │
│       ├── __init__.py
│       │
│       ├── database.py
│       │
│       ├── main.py
│       │
│       ├── models.py
│       │
│       ├── routes.py
│       │
│       ├── schemas.py
│       │
│       ├── database/
│       │   ├── migrations/
│       │   ├── alembic.ini
│       │   └── tradingview.db.ini
│       │
│       │
│       │
│       └── datafeed/
│           ├── symbol_1.csv
│           ├── symbol_2.csv
│           ├── symbol_3.csv
│           ├── .
│           ├── .
│           ├── .
│           └── registry.json
│
│
├── charting_library/         # TradingView's charting library
│   └── ...
│
│
├── playground/               # A testing playground
│   ├── sample.csv
│   └── example.ipynb
│
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```
