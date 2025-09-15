# BrainyCharts
*Python Wrapper For Tradingview's Advanced Charts*

-----------------------------------------------------------------------------------------------------------------------------------------------------

**Seamlessly integrate TradingView's world-class Advanced Charts into your Python workflows.**  
*A bridge between pythonic algo-trading and the most beautiful financial visualizations.*

## 🌟 Why This Project?

TradingView's charts are the gold standard in financial visualization, but using them programmatically in Python has been nearly impossible – until now. This library lets you:

✅ **Render TradingView's** directly in Jupyter notebooks or web apps *(Under Developement)*  
✅ **Sync Python data** (Pandas, NumPy) with TradingView's interactive widgets *(Under Developement)*   

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 🎯 RoadMap

My roadmap for developing this project is as follows.

I have developed the very zero version that "works". It can plot your dataframe.

Next, we will have two major versions:

<details>
<summary>1️⃣ Version 1 RoadMap</summary>

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

4) **▶️ Shaping Functionalities**

    + 🔄 Base
        + [Drawing](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/)
        + [Drawings List](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/Drawings-List)
        + [Drawings API](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/drawings-api)

        + [createshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createshape)
        + [CreateShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateShapeOptions/)

        + [getshapebyid()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#getshapebyid)
    
    + ⚪️ Advanced
        + [createmultipointshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createmultipointshape)
        + [CreateMultipointShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateMultipointShapeOptions/)

        + [createexecutionshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createexecutionshape)
        + [IExecutionLineAdapter](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IExecutionLineAdapter/)

        + [createanchoredshape()](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createanchoredshape)
        + [CreateAnchoredShapeOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateAnchoredShapeOptions/)


3) **⬜️ Project ReDesign & BackEnd/FrontEnd Overview**
   
   + ⚪️ COMPLETE ReView & ReWire

5) **⬜️ Custom Indicators & Timeseries**
   
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

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 🤝 Contributing

I welcome your ideas!  
ping me!  

[![EMail](https://img.shields.io/badge/EMail-white)](mailto:MostafaRoohy@protonmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://linkedin.com/in/mostafaroohy)
[![Telegram](https://img.shields.io/badge/Telegram-skyblue)](https://telegram.me/MostafaRoohy)
[![Telegram Channel](https://img.shields.io/badge/BrainyAlgo-lightblue)](https://telegram.me/BrainyAlgo)  

-----------------------------------------------------------------------------------------------------------------------------------------------------

##
Star ⭐ the repo if this saves you hours of work!