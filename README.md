# BrainChart

*A Python wrapper around TradingView’s Advanced Charting Library with a Pythonic datafeed, widget generator, and runtime shape‑API.*

---

## ✨

**BrainChart** — Python × TradingView Advanced Charts

BrainChart connects your Python data (Pandas/NumPy) to TradingView’s Advanced Charting Library. It provides:

* A minimal **UDF-compatible FastAPI backend** (`/config`, `/search`, `/symbols`, `/history`, `/time`).
* A **Symbol** model to register local OHLCV CSV + metadata.
* A **ChartWidget** generator that writes a self-contained `runtime/widget/index.html` to open in a browser.
* A runtime **Shapes API** (REST wrappers) to create/list/delete drawings on a specific symbol.

You keep full control in Python; the library handles the ACL plumbing.

---

## 🤔 Why I created this

Using TradingView’s [Advanced Charting Library](https://www.tradingview.com/charting-library-docs/) from Python usually means writing a custom datafeed, serving files, and glueing JS <> Python. This project streamlines that:

* Register symbols from a Pandas DataFrame.
* Serve data via a ready-made UDF backend.
* Generate a working widget page.
* Inject drawings programmatically.

Objective: fast iteration for research and prototyping without switching stacks.

---

## ℹ️ Installation Instructions

### Option A — Conda (recommended)

```bash
# clone the repo
git clone https://github.com/MostafaRoohy/BrainChart.git
cd BrainChart

# create and activate the environment
conda env create -f env/environment.yml
conda activate brainchart
```

### Option B — pip

```bash
pip install -r env/requirements.txt
```

> Note: The project is not yet packaged. Import from the repo root (so `import brainchart` works) or add the repo to `PYTHONPATH`.

---

## 📝 Requirements

* **Python**: 3.12
* **Packages** (see `env/requirements.txt` or `env/environment.yml`):

  * `fastapi`, `uvicorn`, `pandas`, `numpy`, `pydantic`, `requests`, `SQLAlchemy`, `ipython`, `ipykernel`

**Proposed workflow:** use the provided **Conda** `env/environment.yml` to ensure deterministic environments across contributors.

---

## ✔️ Examples

Below are concise, working examples.

All exampled csv files exist in `playground/candle_data/`.

*You can see all the examples in `playground/example.ipynb`.*

### 1. Minimal end‑to‑end (symbol, widget)

```python
import time
import pandas as pd
from brainchart import Symbol, ChartWidget, BrainChart


# 1) Prepare OHLCV DataFrame (timestamp in ms)
df_1 = pd.read_csv("./candle_data/CardGlass.csv")


# 2) Define the symbol with the DataFrame
symbol_1 = Symbol(tohlcv_df   = df_1,
                  ticker      = "CGSS",
                  name        = "CardGlass",
                  description = "CardGlass is a symbol",
                  exchange    = "DEx")


# 3) Create the widget with the default symbol
widget = ChartWidget(symbol=symbol_1)


# 3) Create the BrainChart
brain_chart = BrainChart(symbols_list=[symbol_1], chart_widget=widget)
brain_chart.imagine()


# 4) Open browser and navigate to the generated server: http://localhost:8000
```

### 2. Two symbols + default widget

```python
import pandas as pd
from brainchart import Symbol, ChartWidget, BrainChart


# 1) Prepare OHLCV DataFrame (timestamp in ms)
df_1 = pd.read_csv("./candle_data/CardGlass.csv")
df_2 = pd.read_csv("./candle_data/RageGuy.csv")


# 2) Define the symbol with the DataFrame
symbol_1 = Symbol(tohlcv_df   = df_1,
                  ticker      = "CGSS",
                  name        = "CardGlass",
                  description = "CardGlass is a symbol",
                  exchange    = "DEx")

symbol_2 = Symbol(tohlcv_df   = df_2,
                  ticker      = "RGG",
                  name        = "Rage Guy",
                  description = "Rage Guy is another symbol",
                  exchange    = "DEx")


# 3) Create the BrainChart
brain_chart = BrainChart(symbols_list=[symbol_1, symbol_2])
brain_chart.imagine()


# 4) Open browser and navigate to the generated server: http://localhost:8000
```

Switch symbols from the widget’s native UI.

### 3. Attach custom series (overlay + pane)

```python
import pandas as pd
from brainchart import Symbol, ChartWidget, BrainChart


# 1) Prepare OHLCV DataFrame (timestamp in ms). The df has extra columns 'series_1', 'series_2', 'series_3'.
df_1 = pd.read_csv("./candle_data/CryBB.csv")


# 2) Define the symbol with the DataFrame, and pass the column names you want to see in the chart
symbol_1 = Symbol(tohlcv_df     = df_1,
                  ticker        = "CBB",
                  name          = "CryBB",
                  description   = "Babies Cry",
                  exchange      = "DEx",
                  series_column = ['series_1', 'series_3'],
                  series_panel  = ['overlay', 'pane'])


# 3) Create the BrainChart
brain_chart = BrainChart(symbols_list=[symbol_1])
brain_chart.imagine()


# 4) Open browser and navigate to the generated server: http://localhost:8000
```

The custom series become selectable in the UI (overlay vs. an auxiliary pane).

### 4. Create a trend line programmatically while runtime

```python
import pandas as pd
from brainchart import Symbol, ChartWidget, BrainChart


# 1) Prepare OHLCV DataFrame (timestamp in ms)
df_1 = pd.read_csv("./candle_data/CardGlass.csv")
df_2 = pd.read_csv("./candle_data/RageGuy.csv")


# 2) Define the symbol with the DataFrame
symbol_1 = Symbol(tohlcv_df   = df_1,
                  ticker      = "CGSS",
                  name        = "CardGlass",
                  description = "CardGlass is a symbol",
                  exchange    = "DEx")

symbol_2 = Symbol(tohlcv_df   = df_2,
                  ticker      = "RGG",
                  name        = "Rage Guy",
                  description = "Rage Guy is another symbol",
                  exchange    = "DEx")


# 3) Create the BrainChart
brain_chart = BrainChart(symbols_list=[symbol_1, symbol_2])
brain_chart.imagine()


# 4) Open browser and navigate to the generated server: http://localhost:8000


# 5) Make shapes
from brainchart.shape import Shapes, ShapeType, ShapePoint, TrendlineOverrides

shaper_1 = Shapes(symbol_1)
shape    = ShapeType.trend_line
points   = [ShapePoint.priced(1757332740000, 0.282), ShapePoint.priced(1757331660000, 0.294)]
ovr      = TrendlineOverrides(linecolor="#10b981", linewidth=5, show_angle=True)

shaper_1.create(shape, points, ovr)
```

### 5. Listing and Removing all shapes on a symbol

```python
import pandas as pd
from brainchart import Symbol, ChartWidget, BrainChart


# 1) Prepare OHLCV DataFrame (timestamp in ms)
df_1 = pd.read_csv("./candle_data/CardGlass.csv")
df_2 = pd.read_csv("./candle_data/RageGuy.csv")


# 2) Define the symbol with the DataFrame
symbol_1 = Symbol(tohlcv_df   = df_1,
                  ticker      = "CGSS",
                  name        = "CardGlass",
                  description = "CardGlass is a symbol",
                  exchange    = "DEx")

symbol_2 = Symbol(tohlcv_df   = df_2,
                  ticker      = "RGG",
                  name        = "Rage Guy",
                  description = "Rage Guy is another symbol",
                  exchange    = "DEx")


# 3) Create the BrainChart
brain_chart = BrainChart(symbols_list=[symbol_1, symbol_2])
brain_chart.imagine()


# 4) Open browser and navigate to the generated server: http://localhost:8000


# 5) Make shapes
from brainchart.shape import Shapes, ShapeType, ShapePoint, TrendlineOverrides

shaper_1 = Shapes(symbol_1)
shape    = ShapeType.trend_line
points   = [ShapePoint.priced(1757332740000, 0.282), ShapePoint.priced(1757331660000, 0.294)]
ovr      = TrendlineOverrides(linecolor="#10b981", linewidth=5, show_angle=True)

shaper_1.create(shape, points, ovr)


# 6) You can remove a specific shape, or just remove them all
shaper_1.all()                  # Lists all the shapes
# shaper_1.remove(shape_id=5)
# shaper_1.remove_all()
```

---

## 🤝 Contributing

I only onboard collaborators after a short discussion to align expectations.

Just ping me, and we will have a friendly chat and plan for the project.

---

## 📧 Contact Information

[![EMail](https://img.shields.io/badge/EMail-white)](mailto:MostafaRoohy@protonmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://linkedin.com/in/mostafaroohy)
[![Telegram](https://img.shields.io/badge/Telegram-skyblue)](https://telegram.me/MostafaRoohy)
[![Telegram Channel](https://img.shields.io/badge/BrainyAlgo-lightblue)](https://telegram.me/BrainyAlgo)  

---

## ❤️ Donations

If you rely on BrainChart in production or research, sponsoring helps prioritize maintenance and new features.

Or if you would like to support this project, you can donate using the following methods:

- **GitHub Sponsors**: [MostafaRoohy](https://github.com/sponsors/MostafaRoohy)
- **Monero (XMR)**: `85VxJ4mu4K8eRx7nsM6AdAh9RCELooXsFfy5NfSWKSvjaHF8w9heKDAaLHT2L2bWGZPayb2uiKG7cNZHt3vWHL1e5GC5gJs`
- **Bitcoin (BTC)**: `bc1qpzzdzds3mj93v3gp8y943yj4gcmasyhznf27ae`
- **USDT (BEP20)**: `0xb7A2695c5277d632660a8Bd93c6a0edCeBE283B7`
- **Solana (SOL)**: `B5anfZmQjBNUhR2kYJMQMfxEVQ7b5NAy1kGL9eoKeKw1`
- **Ton (TON)**: `UQD9wEyrAxrTcpFRi9xQwb1U0gDjnXjbW8xu9veBIWfR2njS`
- **Ethereum (ETH)**: `0xb7A2695c5277d632660a8Bd93c6a0edCeBE283B7`
- **Litecoin (LTC)**: `ltc1qx4dz04x3ptt6mxc0q9fg3vjqt2kyvkzrcwqq4d`

Thank you for your support!

---

## 💡 Features

* UDF‑compatible FastAPI backend: `/config`, `/search`, `/symbols`, `/history`, `/time`.
* Register local symbols from a Pandas DataFrame; auto‑writes `runtime/datafeed/<TICKER>.csv` and `registry.json`.
* Widget generator writes `runtime/widget/index.html` pointing to your local datafeed.
* Shapes runtime API with typed points and per‑tool overrides.
* Multi‑series support per symbol (overlay or separate pane) via `series_column`, `series_color`, `series_panel`.
* Self‑contained; TradingView’s library is vendored under `charting_library/`.

---

## 🎯 Future Version RoadMap

My roadmap for developing this project is as follows.


<details>
<summary>1️⃣ Version 1 RoadMap (Current)</summary>

1) **✅ Chart Widget**

    + ☑️ The Main Chart Widget
        + ✔️ [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/core_concepts/Widget-Constructor/)
        + ✔️ [Widget Options](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/)
        
        + ✔️ [Widget Methods](https://www.tradingview.com/charting-library-docs/latest/core_concepts/widget-methods)
        + ✔️ [Widget Resolution](https://www.tradingview.com/charting-library-docs/latest/core_concepts/Resolution/#default-resolution)
        + ✔️ [Widget Features](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets)

2) **✅ Symbol**

    + ☑️ Symbol Modeling
        + ✔️ [Symbol Model](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/)
        
        + ✔️ [Symbol DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Symbology)
        + ✔️ [SymbolExt](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.SymbolExt/)

3) **✅ Offline Static TOHLCV Data for Symbol**

    + ☑️ Symbol DataFeed
        + ✔️ [Symbol DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Symbology)
        + ✔️ [Symbol Model](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/)

        + ✔️ [DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/)
        + ✔️ [DataFeed API](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/)
        + ✔️ [DataFeed Required Methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/required-methods)
        + ✔️ [DataFeed Additional Methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/additional-methods)
        + ✔️ [Universal DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/UDF)
        + ✔️ [DataFeed Issues](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Datafeed-Issues)

4) **✅ Shaping Functionalities**

    + ☑️ Base
        + ✔️ [Drawing](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/)
        + ✔️ [Drawings List](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/Drawings-List)
        + ✔️ [Drawings API](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/drawings-api)

        + ✔️ [createshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createshape)
        + ✔️ [CreateShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateShapeOptions/)

        + ✔️ [getshapebyid()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#getshapebyid)
    
    + ☑️ Advanced
        + ✔️ [createmultipointshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createmultipointshape)
        + ✔️ [CreateMultipointShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateMultipointShapeOptions/)

        + ✖️ (postponed) [createexecutionshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createexecutionshape)
        + ✖️ (postponed) [IExecutionLineAdapter](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IExecutionLineAdapter/)

        + ✖️ (postponed) [createanchoredshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createanchoredshape)
        + ✖️ (postponed) [CreateAnchoredShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateAnchoredShapeOptions/)


3) **✅ Project ReDesign & BackEnd/FrontEnd Overview**
   
    + ✔️ COMPLETE ReView & ReWire


4) **✅ Custom TimeSeries Data**
   
    + ☑️ Foundamentals
        + ✖️ (postponed) [Built-In Indicators](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/)
        + ✖️ (postponed) [Custom Study](https://www.tradingview.com/charting-library-docs/latest/custom_studies/)
    
    + ☑️ MetaInfo
        + ✖️ (postponed) [MetaInfo](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/)
        + ✖️ (postponed) [Custom Study Inputs](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/Custom-Studies-Inputs)
        + ✖️ (postponed) [Custom Study Defaults](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/Custom-Studies-Defaults)
    
    + ☑️ Custom Indicator
        + ✖️ (postponed) [Custom Indicator Constructor](https://www.tradingview.com/charting-library-docs/latest/custom_studies/custom-indicator-constructor)
        + ✖️ (postponed) [PineJS](https://www.tradingview.com/charting-library-docs/latest/custom_studies/PineJS-Utility-Functions)
        + ✔️ [Custom Study Plots](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Custom-Studies-Plots)
        + ✔️ [Custom Study OHLC Plots](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Custom-Studies-OHLC-Plots)
    
    + ☑️ Other
        + ✖️ (postponed) [Examples](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Custom-Studies-Examples)
        + ✖️ (postponed) [Extending The Time Scale](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Studies-Extending-The-Time-Scale)

</details>

<details>
<summary>2️⃣ Version 2 RoadMap</summary>

1) **⬜️ Advanced Chart Widget**

    + ⚪️ Saving/Loading
        + [Widget Saving/Loading](https://www.tradingview.com/charting-library-docs/latest/saving_loading/)
        + [Save/Load REST API](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-rest-api/)
        
        + [Chart Layout Methods](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-rest-api/chart-layout-methods)
        + [Indicator Template Methods](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-rest-api/indicator-template-methods)
        + [Template](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-rest-api/drawing-methods)
        + [Template Methods](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-rest-api/drawing-template-methods)
        + [Save/Load Adapter](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-adapter)
        + [Low Level API](https://www.tradingview.com/charting-library-docs/latest/saving_loading/low-level-api)
        + [Saving Drawings Separately](https://www.tradingview.com/charting-library-docs/latest/saving_loading/saving_drawings_separately)
        + [User Settings](https://www.tradingview.com/charting-library-docs/latest/saving_loading/user-settings)

2) **⬜️ Datafeed Re-Architecture**

    + ⚪️ DataFeed
        + [DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/)
        + [DataFeed API](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/)
        + [DataFeed Required Methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/required-methods)
        + [DataFeed Additional Methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/additional-methods)
        + [Universal DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/UDF)
        + [DataFeed Issues](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Datafeed-Issues)

        + [Symbol DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Symbology)
        + [Trading Sessions](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Trading-Sessions)
        + [Extended Sessions](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Extended-Sessions)

3) **⬜️ Project ReDesign & BackEnd/FrontEnd Overview (again)**
   
   + ⚪️ COMPLETE ReView & ReWire

4) **⬜️ Online DataFeed Streaming**

    + ⚪️ DataFeed
        + [DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/)
        + [DataFeed API](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/)
        + [DataFeed Required Methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/required-methods)
        + [DataFeed Additional Methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/additional-methods)
        + [Universal DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/UDF)
        + [DataFeed Issues](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Datafeed-Issues)

        + [Symbol DataFeed](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Symbology)
        + [Symbol Model](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/)

        + [Trading Sessions](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Trading-Sessions)
        + [Extended Sessions](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Extended-Sessions)

</details>


<details>
<summary>3️⃣ Version 3 RoadMap</summary>

1) **⬜️ Custom Indicator/Study**
   
    + ⚪️ Foundamentals
        + [Built-In Indicators](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/)
        + [Custom Study](https://www.tradingview.com/charting-library-docs/latest/custom_studies/)
    
    + ⚪️ MetaInfo
        + [MetaInfo](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/)
        + [Custom Study Inputs](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/Custom-Studies-Inputs)
        + [Custom Study Defaults](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/Custom-Studies-Defaults)
    
    + ⚪️ Custom Indicator
        + [Custom Indicator Constructor](https://www.tradingview.com/charting-library-docs/latest/custom_studies/custom-indicator-constructor)
        + [PineJS](https://www.tradingview.com/charting-library-docs/latest/custom_studies/PineJS-Utility-Functions)
        + [Custom Study Plots](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Custom-Studies-Plots)
        + [Custom Study OHLC Plots](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Custom-Studies-OHLC-Plots)
    
    + ⚪️ Other
        + [Examples](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Custom-Studies-Examples)
        + [Extending The Time Scale](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Studies-Extending-The-Time-Scale)


2) **⬜️ Advanced Shaping Functionalities**

    + ⚪️ Execution Shape
        + [createexecutionshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createexecutionshape)
        + [IExecutionLineAdapter](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IExecutionLineAdapter/)

        + [createanchoredshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createanchoredshape)
        + [CreateAnchoredShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateAnchoredShapeOptions/)


</details>

---

## 🔑 License

**MIT** — see `LICENSE`.

---

## ❓ FAQ

* **How should my df be?**

  Your df must include `timestamp`, `open`, `high`, `low`, `close`, `volume` columns. And the `timestamp` column must be in milliseconds (I will flex it later).

* **Does shapes API accept ms or s?**

  Both. Timestamps are normalized; ms are auto‑converted to seconds for drawings.

* **Where are runtime artifacts?**

  Under `runtime/database/` and `runtime/datafeed/` and `runtime/widget/`.
