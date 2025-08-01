# BrainyCharts

``` text
BrainyCharts
│
├── brainy_charts/ # Anything we code, is here. All the wrapper functionalities.
│   |
│   ├── __init__.py
│   ├── brainy_charts.py
|   |
│   └── backend/
|       |
|       ├── __init__.py
|       ├── database.py
|       ├── main.py
|       ├── models.py
|       ├── routes.py
|       ├── schemas.py
|       |
|       ├── database/
|       |   |
|       |   ├── migrations/
|       |   |   |
|       |   |   └──*
|       |   ├──alembic.ini
|       |   └──tradingview.db
|       |
|       ├── datafeed/
|       |   |
|       |   ├──symbol1.scv
|       |   ├──sym65.csv
|       |   ├──examplesymbol.csv
|       |   └──registry.json
|       |
|       └────────────────────
│
│
├── charting_library/ # The whole tradingview's library comes here
│   └──*
│
│
├── playground/ # A testing playground.
│   ├── sample.csv
│   └── example.ipynb
|
|
└────────────────────────────
```
