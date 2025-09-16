#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
import pandas as pd
from typing import List, Dict, Optional, Any
from enum import Enum
from pathlib import Path
import json
import os
#
###################################################################################################
###################################################################################################
################################################################################################### Objects
#
class SymbolType(Enum):

    stock       = "stock"
    index       = "index"
    forex       = "forex"
    futures     = "futures"
    bitcoin     = "bitcoin"
    crypto      = "crypto"
    undefined   = "undefined"
    expression  = "expression"
    spread      = "spread"
    cfd         = "cfd"
    economic    = "economic"
    equity      = "equity"
    dr          = "dr"
    bond        = "bond"
    right       = "right"
    warrant     = "warrant"
    fund        = "fund"
    structured  = "structured"
    commodity   = "commodity"
    fundamental = "fundamental"
    spot        = "spot"
    swap        = "swap"
    option      = "option"


    def __str__(self):

        return (self.value)
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class Frame(Enum):

    T = "T"
    S = "S"
    m = ""
    D = "D"
    W = "W"
    M = "M"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class ResolutionString:

    def __init__(self, x:int=1, frame:Frame=Frame.m):

        self.resolution = f"{x}{frame.value}"
    #


    def __str__(self):
        
        return (self.resolution)
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class DataStatus(Enum):

    streaming         = 'streaming'
    endofday          = 'endofday'
    delayed_streaming = 'delayed_streaming'


    def __str__(self):

        return (f'{self.value}')
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class SeriesFormat(Enum):

    price  = 'price'
    volume = 'volume'


    def __str__(self):

        return (self.value)
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class VisiblePlotsSet(Enum):

    ohlcv = 'ohlcv'
    ohlc  = 'ohlc'
    c     = 'c'
    hlc   = 'hlc'


    def __str__(self):

        return (self.value)
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class SymbolPriceSource:

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/#price_source_id
    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/#price_sources

    def __init__(self, id:str=None, name:str=None):
        
        if (id is None  and  name is None):

            raise
        #
    #
#

class SubsessionInfo:

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySubsessionInfo/
    pass
#

class Timezone(Enum):

    exchange                       = "exchange" 
    Etc_UTC                        = "Etc/UTC"

    Africa_Cairo                   = "Africa/Cairo" 
    Africa_Casablanca              = "Africa/Casablanca" 
    Africa_Johannesburg            = "Africa/Johannesburg"
    Africa_Lagos                   = "Africa/Lagos"
    Africa_Nairobi                 = "Africa/Nairobi"
    Africa_Tunis                   = "Africa/Tunis"
    America_Anchorage              = "America/Anchorage"
    America_Argentina_Buenos_Aires = "America/Argentina/Buenos_Aires"
    America_Bogota                 = "America/Bogota"
    America_Caracas                = "America/Caracas"
    America_Chicago                = "America/Chicago"
    America_El_Salvador            = "America/El_Salvador"
    America_Juneau                 = "America/Juneau"
    America_Lima                   = "America/Lima"
    America_Los_Angeles            = "America/Los_Angeles"
    America_Mexico_City            = "America/Mexico_City"
    America_New_York               = "America/New_York"
    America_Phoenix                = "America/Phoenix"
    America_Santiago               = "America/Santiago"
    America_Sao_Paulo              = "America/Sao_Paulo"
    America_Toronto                = "America/Toronto"
    America_Vancouver              = "America/Vancouver"
    Asia_Almaty                    = "Asia/Almaty"
    Asia_Ashkhabad                 = "Asia/Ashkhabad"
    Asia_Bahrain                   = "Asia/Bahrain"
    Asia_Bangkok                   = "Asia/Bangkok"
    Asia_Chongqing                 = "Asia/Chongqing"
    Asia_Colombo                   = "Asia/Colombo"
    Asia_Dhaka                     = "Asia/Dhaka"
    Asia_Dubai                     = "Asia/Dubai"
    Asia_Ho_Chi_Minh               = "Asia/Ho_Chi_Minh"
    Asia_Hong_Kong                 = "Asia/Hong_Kong"
    Asia_Jakarta                   = "Asia/Jakarta"
    Asia_Jerusalem                 = "Asia/Jerusalem"
    Asia_Karachi                   = "Asia/Karachi"
    Asia_Kathmandu                 = "Asia/Kathmandu"
    Asia_Kolkata                   = "Asia/Kolkata"
    Asia_Kuala_Lumpur              = "Asia/Kuala_Lumpur"
    Asia_Kuwait                    = "Asia/Kuwait"
    Asia_Manila                    = "Asia/Manila"
    Asia_Muscat                    = "Asia/Muscat"
    Asia_Nicosia                   = "Asia/Nicosia"
    Asia_Qatar                     = "Asia/Qatar"
    Asia_Riyadh                    = "Asia/Riyadh"
    Asia_Seoul                     = "Asia/Seoul"
    Asia_Shanghai                  = "Asia/Shanghai"
    Asia_Singapore                 = "Asia/Singapore"
    Asia_Taipei                    = "Asia/Taipei"
    Asia_Tehran                    = "Asia/Tehran"
    Asia_Tokyo                     = "Asia/Tokyo"
    Asia_Yangon                    = "Asia/Yangon"
    Atlantic_Azores                = "Atlantic/Azores"
    Atlantic_Reykjavik             = "Atlantic/Reykjavik"
    Australia_Adelaide             = "Australia/Adelaide"
    Australia_Brisbane             = "Australia/Brisbane"
    Australia_Perth                = "Australia/Perth"
    Australia_Sydney               = "Australia/Sydney"
    Europe_Amsterdam               = "Europe/Amsterdam"
    Europe_Athens                  = "Europe/Athens"
    Europe_Belgrade                = "Europe/Belgrade"
    Europe_Berlin                  = "Europe/Berlin"
    Europe_Bratislava              = "Europe/Bratislava"
    Europe_Brussels                = "Europe/Brussels"
    Europe_Bucharest               = "Europe/Bucharest"
    Europe_Budapest                = "Europe/Budapest"
    Europe_Copenhagen              = "Europe/Copenhagen"
    Europe_Dublin                  = "Europe/Dublin"
    Europe_Helsinki                = "Europe/Helsinki"
    Europe_Istanbul                = "Europe/Istanbul"
    Europe_Lisbon                  = "Europe/Lisbon"
    Europe_London                  = "Europe/London"
    Europe_Luxembourg              = "Europe/Luxembourg"
    Europe_Madrid                  = "Europe/Madrid"
    Europe_Malta                   = "Europe/Malta"
    Europe_Moscow                  = "Europe/Moscow"
    Europe_Oslo                    = "Europe/Oslo"
    Europe_Paris                   = "Europe/Paris"
    Europe_Prague                  = "Europe/Prague"
    Europe_Riga                    = "Europe/Riga"
    Europe_Rome                    = "Europe/Rome"
    Europe_Stockholm               = "Europe/Stockholm"
    Europe_Tallinn                 = "Europe/Tallinn"
    Europe_Vienna                  = "Europe/Vienna"
    Europe_Vilnius                 = "Europe/Vilnius"
    Europe_Warsaw                  = "Europe/Warsaw"
    Europe_Zurich                  = "Europe/Zurich"
    Pacific_Auckland               = "Pacific/Auckland"
    Pacific_Chatham                = "Pacific/Chatham"
    Pacific_Fakaofo                = "Pacific/Fakaofo"
    Pacific_Honolulu               = "Pacific/Honolulu"
    Pacific_Norfolk                = "Pacific/Norfolk"
    US_Mountain                    = "US/Mountain"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

later_doc_str  = """









LibrarySymbolInfo
=================
Canonical description of a TradingView symbol as consumed by the Charting Library.
Populate this object from your symbology/metadata source and return it from the
datafeed's `resolveSymbol`/`searchSymbols` flows.

Parameters
----------

build_seconds_from_ticks : bool, optional, default=False
    Allow the library to synthesize **seconds** bars from **tick** data when the required
    seconds resolution is not directly available from the datafeed.
    Requirements:
      - `has_seconds == True`
      - `has_ticks == True`
      - `seconds_multipliers` is empty **or** only contains resolutions the datafeed
        itself provides.
    Notes:
      - If the datafeed provides 3S, the library may build 1S/2S from ticks;
        15S will be built from seconds bars, not ticks.

corrections : str, optional
    Per-day session overrides in `SESSION:YYYYMMDD` form. Multiple days are separated
    by `;`. Within `SESSION`, multiple sub-sessions are comma-separated.
    Example for two days:
      "1900F4-2350F4,1000-1845:20181113;1000-1400:20181114"
    Meaning:
      - 2018-11-13: two sessions; first 19:00 four days before to 23:50 four days before,
        then 10:00–18:45 same day.
      - 2018-11-14: single session 10:00–14:00.

currency_code : str, optional
    Display currency code (Security Info dialog and price axes). May reflect conversion
    if you enable currency conversion in your stack.


data_status : Literal["streaming","endofday","delayed_streaming"], optional
    Series data status. When `delayed_streaming` or `endofday`, the UI shows a
    delayed-data indicator (requires `display_data_mode` featureset).
    If `delayed_streaming`, set `delay` (seconds).

delay : int, optional
    Delay type/value for data:
      -  0  → realtime
      - -1  → end-of-day
      - >0  → delayed realtime in seconds


expiration_date : int, optional
    Unix timestamp of contract expiration. **Required** when `expired == True`.
    The library will request data starting at this time.

expired : bool, optional, default=False
    Whether this symbol is an expired futures contract.




original_currency_code : str, optional
    Trading currency (original, pre-conversion).

original_unit_id : str, optional
    Unique id of the trading unit (e.g., base unit for commodities).

price_source_id : str, optional
    Selected price source id for this symbol; must exist in `price_sources`.
    Requires `symbol_info_price_source` featureset to show in legend.

price_sources : list[dict], optional
    Enumerates supported price sources for the series (legend display).
    Example:
      [{"id": "1", "name": "Spot Price"}, {"id": "321", "name": "Bid"}]




session : str
    Trading hours in exchange timezone (Olson/IANA). See Trading Sessions.
    Example: "1700-0200".

session_display : str, optional
    Human-friendly session string shown in UI. Falls back to `session` if omitted.

session_holidays : str, optional
    Comma-separated YYYYMMDD non-trading dates (not shown on chart).
    Example: "20181105,20181107,20181112".
    Use `corrections` for nuanced holiday sessions.

subsession_id : str, optional
    Identifier of the currently displayed subsession (must exist in `subsessions`).

subsessions : list[dict], optional
    Metadata for subsessions within extended sessions. See Extended Sessions.




timezone : str
    Exchange timezone in Olson/IANA form (e.g., "America/New_York").



unit_conversion_types : list[str], optional
    Allowed unit conversion group names for this instrument.

unit_id : str, optional
    Unique unit identifier (or alt id when unit conversion is enabled). Shown on axes.





Cross-field rules & quick reference
----------------------------------
Resolution enablement:
  • Seconds  → `has_seconds=True` and `seconds_multipliers`.
  • Minutes  → `has_intraday=True` and `intraday_multipliers`.
  • Daily    → `has_daily=True` and `daily_multipliers`.
  • Weekly   → `has_weekly_and_monthly=True` and `weekly_multipliers`.
  • Monthly  → `has_weekly_and_monthly=True` and `monthly_multipliers`.

Building/synthesis:
  • Higher daily/weekly/monthly can be built from the respective *_multipliers lists.
  • Weekly/Monthly may be built from Daily when `has_weekly_and_monthly=False`
    (costly; may fail).
  • Seconds from ticks only when `build_seconds_from_ticks=True` and prerequisites met.

Pricing format interplay:
  • Decimal pricing  → set `format="price"`, `fractional=False`,
                       choose `minmov` and `pricescale=10**n`.
  • Fractional       → set `fractional=True`, `pricescale=2**n`,
                       `minmov` as numerator unit; optionally `minmove2>0` for xx'yy'zz.
  • Variable ticks   → omit `fractional`, specify `variable_tick_size`.

Examples
--------
Minimal stock:
  {
    "name": "AAPL",
    "ticker": "NASDAQ:AAPL",
    "description": "Apple Inc.",
    "exchange": "NASDAQ",
    "listed_exchange": "NASDAQ",
    "type": "stock",
    "timezone": "America/New_York",
    "session": "0930-1600",
    "format": "price",
    "minmov": 1,
    "pricescale": 100,
    "has_daily": True,
    "daily_multipliers": ["1"],
    "has_intraday": True,
    "intraday_multipliers": ["1","5","15","60"],
    "visible_plots_set": "ohlcv",
    "volume_precision": 0
  }

Fractional futures (1/4 of 1/32):
  {
    "name": "ZB",
    "type": "futures",
    "timezone": "America/Chicago",
    "session": "1700-1600",
    "format": "price",
    "fractional": True,
    "minmov": 1,
    "pricescale": 128,
    "minmove2": 4
  }

Seconds synthesized from ticks:
  {
    "name": "BTCUSD",
    "type": "crypto",
    "timezone": "Etc/UTC",
    "session": "0000-0000",
    "format": "price",
    "minmov": 1,
    "pricescale": 100,
    "has_ticks": True,
    "has_seconds": True,
    "seconds_multipliers": [],   # datafeed provides no explicit seconds
    "build_seconds_from_ticks": True
  }
"""
#
###################################################################################################
###################################################################################################
################################################################################################### Symbol
#
class Symbol:

    """
    LibrarySymbolInfo
    =================
    Canonical description of a TradingView symbol as consumed by the Charting Library.
    Populate this object from your symbology/metadata source and return it from the
    datafeed's `resolveSymbol`/`searchSymbols` flows.

    Parameters
    ----------

    tohlcv_df : pd.DataFrame, required
        The DF.
        `Default=pd.DataFrame()`

    ticker : str, optional
        Global unique identifier used for data requests (preferred over `name` if set).
        Avoid ":" unless following "EXCHANGE:SYMBOL" format (e.g., "NYSE:IBM").
        `Default=SYMBOL_TICKER`

    name : str, required
        Exchange-local symbol code (e.g., "AAPL", "9988"). Do not include exchange.
        Used to resolve symbols unless `ticker` is provided.
        `Default=symbol_name`

    base_name : list[str], optional
        Base symbols for synthetic or composite instruments.
        Example: for "AAPL*MSFT" → ["NASDAQ:AAPL", "NASDAQ:MSFT"].

    library_custom_fields : dict[str, Any], optional
        Arbitrary metadata preserved by the library and available via
        `IChartWidgetApi.symbolExt`. Does not override core fields like `name`/`ticker`.





    description : str, required
        Human-readable symbol description shown in the chart legend.
        `Default=Description`

    long_description : str, optional
        Optional longer description for the symbol.

    type : SymbolType, required
        Instrument type, e.g., "stock", "index", "forex", "futures", "crypto", etc.
        `Default=SymbolType.undefined`

    exchange : str, required
        Current (proxy) exchange label displayed in the legend.
        Example: "NYSE".
        `Default=ExChange`

    listed_exchange : str, required
        Real, listed exchange short name (legend). Example: "NYSE".
        `Default=ExChange`

    sector : str, optional
        Stock sector (Security Info dialog).

    industry : str, optional
        Stock industry (Security Info dialog).

    logo_urls : str | list[str], optional
        Symbol logo(s) (requires `show_symbol_logos` featureset).
        - One URL → single logo.
        - Two URLs → overlapped circles; first URL drawn on top (typical for FX flags).
        Accepts absolute/relative URLs and data-URLs.

    exchange_logo : str, optional
        URL or data-URL for exchange logo (requires `show_exchange_logos` featureset).
        Prefer square images; simple SVG recommended.
        Examples:
        "https://yourserver.com/exchangeLogo.svg"
        "/images/ex.svg"
        "data:image/svg+xml;base64,..."





    format : SeriesFormat, required
        Price axis label formatting:
        - "price"   → decimal/fractional based on `minmov`, `pricescale`, `minmove2`,
                        `fractional`, `variable_tick_size`.
        - "volume"  → decimal with K/M/B/T suffixes.
        `Default=SeriesFormat.price`

    pricescale : int, required
        Price scale factor:
        - Decimal pricing → `10**n` (e.g., 1, 10, 100, 10000000).
        - Fractional pricing → `2**n` (e.g., 8, 16, 256).
        Interacts with `minmov`, `minmove2`, `fractional`, `variable_tick_size`.
        `Default=1_00_000_000`

    minmov : int, required
        The minimal price **units** that comprise one tick.
        Example: U.S. equities tick by 0.01 → `minmov=1` with `pricescale=100`.
        `Default=1`

    minmove2 : int, optional
        Secondary fractional unit for fractional pricing (see `fractional`).
        Use 0 or omit for common decimal pricing.

    fractional : bool, optional
        Enable fractional price display:
        - Form 1: `xx'yy`       (e.g., 133'21)
        - Form 2: `xx'yy'zz`    (e.g., 133'21'5) when `minmove2 > 0`
        Conditions:
        - `minmov` / `pricescale` represent a fraction
        - `minmove2` used only in Form 2
        - `variable_tick_size` should be omitted
        Example config (1/4 of 1/32):
        minmov=1, pricescale=128, minmove2=4
        Values:
            119'16'0  → 119 + 16/32
            119'16'2  → 119 + 16.25/32
            119'16'5  → 119 + 16.5/32
            119'16'7  → 119 + 16.75/32
        More examples:
        ZBM2014 (1/32):            minmov=1,  pricescale=32,  minmove2=0
        ZCM2014 (2/8):             minmov=2,  pricescale=8,   minmove2=0
        ZFM2014 (1/4 of 1/32):     minmov=1,  pricescale=128, minmove2=4

    variable_tick_size : str, optional
        Piecewise tick size by price ranges. Format:
        "<tick1> <price1> <tick2> <price2> ... <tickN>"
        Example: "0.01 10 0.02 25 0.05"
        - tick=0.01 for price < 10
        - tick=0.02 for price < 25
        - tick=0.05 for price >= 25

    visible_plots_set : VisiblePlotsSet, optional, 
        Supported value set for the series:
        - "ohlcv" → OHLC + Volume
        - "ohlc"  → OHLC (no volume)
        - "c"     → Close-only (line-based styles)

    volume_precision : int, optional, 
        Typical decimal places for volume. 0 → integer volumes; 1 → one decimal, etc.
        Note: Although some docs show `'0'` as a string, the type is numeric.
        `Default=0`





    has_daily : bool, optional
        Datafeed contains daily bars. To actually enable daily resolutions, also set
        `daily_multipliers`. If false, selecting daily resolutions shows “No data here”.
        `Default=True`

    has_intraday : bool, optional
        Datafeed contains **minute** bars. Required to enable intraday resolutions.
        Also set `intraday_multipliers`.
        `Default=True`

    has_seconds : bool, optional
        Datafeed contains **seconds** bars. Required to enable seconds resolutions
        and for `build_seconds_from_ticks`.
        `Default=True`

    has_ticks : bool, optional
        Datafeed contains tick data. Required for tick-based resolutions and
        for `build_seconds_from_ticks`.
        `Default=False`

    has_weekly_and_monthly : bool, optional
        Datafeed contains weekly/monthly bars. To enable UI selection, also set
        `weekly_multipliers` and/or `monthly_multipliers`.
        If false, the library *may* attempt to build W/M from daily bars (expensive);
        failures show “No data here”.
        `Default=False`

    has_empty_bars : bool, optional
        Fill missing bars inside the trading session with empty bars (no trades).
        Incompatible with `disable_resolution_rebuild` featureset.
        `Default=False`

    supported_resolutions : list[ResolutionString], optional
        Resolutions enabled in the Resolution menu for this symbol.
        Behavior:
        - `[]`           → all menu resolutions disabled.
        - `undefined`    → enable `DatafeedConfiguration.supported_resolutions`
                            plus custom resolutions.
        Availability logic (pseudo):
            if resolution.isIntraday:
                require has_intraday and value in supported_resolutions
            else:
                require value in supported_resolutions
        Note: visible time frames also depend on available resolutions.
        `Default=["1S", "5S", "1", "5", "15", "30", "60", "D", "W"]`

    intraday_multipliers : list[str], optional
        Supported **minute** resolutions (ascending), e.g. ["1","5","15"].
        Required to enable intraday resolutions. Every value must be served by
        `getBars`. When omitted or empty list, the library treats it as “any minute
        resolution is supported” (be sure your backend can serve arbitrary minutes).
        Note: daily/weekly/monthly cannot be built from minute bars.

    seconds_multipliers : list[str], optional
        Supported **seconds** resolutions (ascending), e.g. ["1","2","5"].
        Required to enable seconds resolutions. If only ["1"] is provided, the library
        can build 5S from 1S; for unavailable smaller seconds it may synthesize from ticks
        if `build_seconds_from_ticks == True`.
        `Default=["1", "2", "3", "4", "5", "10", "15", "20", "30", "40"]`

    daily_multipliers : list[str], optional
        Supported **daily** resolutions (ascending). Strings must be numeric, e.g. ["1","2"].
        Required to enable daily resolutions. Also used to build higher daily multiples
        that aren’t explicitly provided by the datafeed.
        `Default=["1"]`

    weekly_multipliers : list[str], optional
        Supported **weekly** resolutions (ascending), e.g. ["1","3"].
        Required to enable weekly resolutions. Also used to build higher multiples.
        `Default=["1"]`

    monthly_multipliers : list[str], optional
        Supported **monthly** resolutions (ascending), e.g. ["1","3","6","12"].
        Required to enable monthly resolutions. Also used to build higher multiples.
        `Default=["1"]`
    """

    _tickers = []

    def __init__(self,
            #
            # region params V1
            #
            ################################################################################################## Urgent
            #
            tohlcv_df                : pd.DataFrame                      = pd.DataFrame(),
            ticker                   : str                               = "TICKER",
            name                     : str                               = "Name",
            base_name                : Optional[List[str]]               = None,
            library_custom_fields    : Optional[Dict[str, Any]]          = None,
            #
            ################################################################################################## Core Symbol Info
            #
            description              : str                               = "Description",
            long_description         : Optional[str]                     = None,
            type                     : SymbolType                        = SymbolType.undefined,
            exchange                 : str                               = "ExChange",
            listed_exchange          : str                               = "ExChange",
            sector                   : Optional[str]                     = None,
            industry                 : Optional[list[str]]               = None,
            logo_urls                : Optional[str|List[str]]           = None,
            exchange_logo            : Optional[str]                     = None,
            #
            ################################################################################################## Price & Volume Formatting
            #
            format                   : SeriesFormat                      = SeriesFormat.price,
            pricescale               : int                               = 1_00_000_000,
            minmov                   : int                               = 1,
            minmove2                 : Optional[int]                     = None,
            fractional               : Optional[bool]                    = None,
            variable_tick_size       : Optional[str]                     = None,
            visible_plots_set        : Optional[VisiblePlotsSet]         = None,
            volume_precision         : Optional[int]                     = 0,
            #
            ################################################################################################## Resolutions
            #
            has_daily                : Optional[bool]                    = True,
            has_intraday             : Optional[bool]                    = True,
            has_seconds              : Optional[bool]                    = True,
            has_ticks                : Optional[bool]                    = False,
            has_weekly_and_monthly   : Optional[bool]                    = False,
            has_empty_bars           : Optional[bool]                    = False,
            build_seconds_from_ticks : Optional[bool]                    = False,
            supported_resolutions    : Optional[list[ResolutionString]]  = ["1S", "5S", "1", "5", "15", "30", "60", "D", "W"],
            intraday_multipliers     : Optional[List[str]]               = None,
            seconds_multipliers      : Optional[List[str]]               = ["1", "2", "3", "4", "5", "10", "15", "20", "30", "40"],
            daily_multipliers        : Optional[List[str]]               = ["1"],
            weekly_multipliers       : Optional[List[str]]               = ["1"],
            monthly_multipliers      : Optional[List[str]]               = ["1"],
            #
            ################################################################################################## .
            #
            # endregion
            #
            # region params V2. These params will be implemented in V2
            #
            ################################################################################################## Data Capabilities & Status
            #
            data_status              : Optional[DataStatus]              = None,
            delay                    : Optional[int]                     = None,
            #
            ################################################################################################## Session and Time
            #
            session                  : str                               = "24x7",
            session_display          : Optional[str]                     = None,
            session_holidays         : Optional[str]                     = None,
            subsession_id            : Optional[str]                     = None,
            subsessions              : Optional[List[SubsessionInfo]]    = None,
            timezone                 : Timezone                          = Timezone.Etc_UTC,
            corrections              : Optional[str]                     = None,
            #
            ################################################################################################## Futures/Options
            #
            expired                  : Optional[bool]                    = False,
            expiration_date          : Optional[int]                     = None,
            #
            ################################################################################################## Units & Currency
            #
            currency_code            : Optional[str]                     = None,
            original_currency_code   : Optional[str]                     = None,
            unit_id                  : Optional[str]                     = None,
            original_unit_id         : Optional[str]                     = None,
            unit_conversion_types    : Optional[List[str]]               = None,
            #
            ################################################################################################## Price sources
            #
            price_source_id          : Optional[SymbolPriceSource]       = None, # ??
            price_sources            : Optional[List[SymbolPriceSource]] = None, # ??
            ################################################################################################## .
            #
            #endregion
            #
        ):

        if (ticker in Symbol._tickers):

            raise
        #


        self.tohlcv_df              = tohlcv_df
        self.ticker                 = (ticker)  if  (ticker!="TICKER")  else  (f"TICKER_{len(Symbol._tickers)}")
        self.name                   = name
        self.base_name              = base_name
        self.library_custom_fields  = library_custom_fields

        self.description            = description
        self.long_description       = long_description
        self.type                   = str(type)
        self.exchange               = exchange
        self.listed_exchange        = listed_exchange
        self.sector                 = sector
        self.industry               = industry
        self.logo_urls              = logo_urls
        self.exchange_logo          = exchange_logo

        self.format                 = str(format)
        self.pricescale             = pricescale
        self.minmov                 = minmov
        self.minmove2               = minmove2
        self.fractional             = fractional
        self.variable_tick_size     = variable_tick_size
        self.visible_plots_set      = visible_plots_set
        self.volume_precision       = volume_precision

        self.has_daily              = has_daily
        self.has_intraday           = has_intraday
        self.has_seconds            = has_seconds
        self.has_ticks              = has_ticks
        self.has_weekly_and_monthly = has_weekly_and_monthly
        self.has_empty_bars         = has_empty_bars
        self.has_empty_bars         = build_seconds_from_ticks
        self.supported_resolutions  = supported_resolutions
        self.intraday_multipliers   = intraday_multipliers
        self.seconds_multipliers    = seconds_multipliers
        self.daily_multipliers      = daily_multipliers
        self.weekly_multipliers     = weekly_multipliers
        self.monthly_multipliers    = monthly_multipliers


        self.session  = session
        self.timezone = str(timezone)

        Symbol._tickers.append(self.ticker)
    #

    def _as_dict(self):

        return {key: value for key, value in self.__dict__.items() if (value is not None  and  not isinstance(value, pd.DataFrame))}
    #

    def _register(self):

        root_dir      = Path(__file__).parent.parent
        datafeed_dir  = root_dir / "runtime" / "datafeed"
        datafeed_dir.mkdir(parents=True, exist_ok=True)
        csv_path      = datafeed_dir / f"{self.ticker}.csv"
        registry_path = datafeed_dir / "registry.json"

        registry = {}

        if registry_path.exists():

            with open(registry_path, 'r', encoding='utf-8') as f:

                try:

                    registry = json.load(f)
                #
                except Exception:

                    registry = {}
                #
            #
        #

        registry[self.ticker] = self._as_dict()
        with open(registry_path, 'w', encoding='utf-8') as f:

            json.dump(registry, f, indent=4)
        #

        self.tohlcv_df.to_csv(csv_path, index=False)
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#