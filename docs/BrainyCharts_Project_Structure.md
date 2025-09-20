# BrainyCharts Project Structure

-----------------------------------------------------------------------------------------------------------------------------------------------------

<details>
<summary>Main Structure</summary>

- **BrainyCharts/**
  - **`brainycharts/`**: The core package for the BrainyCharts application, containing all the logic for data handling, server management, and chart rendering.
  - **`charting_library/`**: Contains the TradingView's advanced charts Library, which is like a 'black box' for us.
  - **`Docs/`**: Project documentations.
  - **`env/`**: Environment-related files, such as conda environment configurations and pip requirements.
  - **`icons/`**: Icons used in the project.
  - **`playground/`**: A testing playground.
  - **`runtime/`**: Files and Folders generated while running the app.
  - **`.gitignore`**: Git Ignores.
  - **`LICENSE`**: License.
  - **`README.md`**: Read Me.

</details>

-----------------------------------------------------------------------------------------------------------------------------------------------------

<details>
<summary>brainycharts/</summary>

```bash
    brainycharts/                                 # The core package for the BrainyCharts application, containing all the logic for data handling, server management, and chart rendering.
    │
    ├── __init__.py                                # Marks the `brainycharts` directory as a Python package, allowing its modules to be imported.
    │
    ├── brainy.py                                  # The main user-facing module. It contains the `BrainyChart` class, which is the primary entry point for creating and managing charts. This class handles data processing, starts the backend server, and provides methods for interacting with the chart's features, such as drawing shapes.
    │
    ├── custom_indicators.py                       # Custom indicator/study functionalities.
    │
    ├── database.py                                # Configures the connection to the SQLite database using SQLAlchemy and manages database sessions.
    │
    ├── fast_api.py                                # The entry point for the FastAPI application. It initializes the app, configures middleware, and includes the API routes.
    │
    ├── shape.py                                   # Shaping functionalities.
    │
    ├── symbol.py                                  # Data model for the symbols displayed on the chart. It holds metadata like the ticker, name, and exchange, along with the bar data.
    │
    └── widget.py                                  # The main chart's widget constructor
```

</details>

-----------------------------------------------------------------------------------------------------------------------------------------------------

<details>
<summary>charting_library/</summary>

This package contains the TradingView Charting Library, which is the core component used to display the charts.

**This directory is like a 'black box'. Don't touch it's contents unless you know what you're doing.**

All internal JS and CSS codes of the library are inlined and minified to reduce the page load time. Files that are expected to be edited by you were not minified.

```bash
    charting_library/                              # contains all the library files.
    │
    ├── charting_library/                          # files contain an external library widget interface, they are not supposed to be edited.
    │   │
    │   ├── bundles/                               # stores library internal content and is not intended for other purposes, it should be like "black box" for you so it could be changed anytime without a notice.
    │   │
    │   ├── charting_library.js                    # is an UMD module (for backward compatibility). is an UMD module (for backward compatibility).
    │   │
    │   ├── charting_library.d.ts                  # contains TypeScript definitions for the widget interface.
    │   │
    │   ├── charting_library.cjs.js                # is an CommonJS module. is an UMD module (for backward compatibility).
    │   │
    │   ├── charting_library.esm.js                # is an native JavaScript module, see import. is an UMD module (for backward compatibility).
    │   │
    │   ├── charting_library.standalone.js         # is an iife module. is an UMD module (for backward compatibility).
    │   │
    │   ├── datafeed-api.d.ts                      # contains TypeScript definitions for the data feed interface.
    │   │
    │   └── package.json
    │
    │
    ├── datafeeds/
    │   │
    │   └── udf/                                   # contains UDF-compatible datafeed wrapper (implements Datafeed API to connect to library and UDF to connect to datafeed). Sample datafeed wrapper implements pulse real-time emulation. You are free to edit its code.
    │
    │
    └── changelog.md/
```

</details>

-----------------------------------------------------------------------------------------------------------------------------------------------------