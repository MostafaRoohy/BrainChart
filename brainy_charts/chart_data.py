###################################################################################################
###################################################################################################
###################################################################################################
#
import pandas as pd
from typing import List, Dict, Optional
#
###################################################################################################
###################################################################################################
################################################################################################### Chart Model
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/
#
class ChartData:

    """
    Represents all the metadata for a single symbol, mirroring the TradingView
    Charting Library's LibrarySymbolInfo interface. This class is used to configure
    how a symbol is displayed and how its data is handled by the chart.

    Attributes
    ----------
    tohlcv_df : pd.DataFrame
        A DataFrame containing the Time, Open, High, Low, Close, and Volume data.
        The 'timestamp' column must be in UTC milliseconds and in ascending order.

    Parameters
    ----------
    ticker : str
        The unique identifier for the symbol. This is the name that you'll use to request
        data for this symbol from your datafeed.
    name : str, optional
        The name of the symbol. It is displayed in the chart legend and the symbol search.
        If not provided, it defaults to a combination of the ticker and exchange.
    description : str
        A brief description of the symbol. It's displayed in the chart legend.
    long_description : str, optional
        A longer, more detailed description for the symbol.
    type : str
        The type of the instrument (e.g., "stock", "crypto", "forex", "index").
    exchange : str
        The name of the exchange where the symbol is traded. It's displayed in the chart legend.
    listed_exchange : str, optional
        The name of the exchange where the symbol is listed.
    logo_urls : List[str], optional
        An array of URLs for the symbol's logo images. The library will select an appropriate
        logo based on the theme.
    exchange_logo : str, optional
        URL of an image to be displayed as the logo for the exchange.
    sector : str, optional
        The sector of the industry the symbol belongs to (e.g., "Technology").
    industry : str, optional
        The specific industry the symbol belongs to (e.g., "Software").
    session : str
        The trading session for the symbol. The format is "HHMM-HHMM". For 24x7 sessions,
        use "24x7". A session can be broken into parts using a comma, e.g., "0930-1600,1700-2000".
    session_display : str, optional
        A human-friendly representation of the session. If not provided, it's generated from `session`.
    timezone : str
        The timezone of the exchange where the symbol is traded (e.g., "America/New_York", "Etc/UTC").
    session_holidays : str, optional
        A comma-separated string of holidays for the symbol in "YYYYMMDD" format.
    corrections : str, optional
        A string defining session corrections for specific days.
    subsessions : List[Dict], optional
        An array of objects defining different trading phases within a session (e.g., pre-market, post-market).
    subsession_id : str, optional
        The ID of the current subsession.
    expired : bool
        A boolean showing whether this symbol is an expired futures contract.
    expiration_date : int, optional
        A Unix timestamp (in seconds) of the expiration date for futures contracts.
    pricescale : int
        The number of decimal places in the instrument's price. E.g., if a price is 1.01, `pricescale` is 100.
    minmov : int
        The smallest possible price movement. For example, for a tick size of 0.01, `minmov` is 1.
        For a tick size of 0.25, `minmov` is 25.
    minmov2 : int
        Used for fractional prices. For non-fractional prices, this should be 0.
    fractional : bool
        A boolean indicating if the price is fractional.
    variable_tick_size : List[Dict], optional
        Defines different tick sizes for different price ranges.
    has_intraday : bool
        Set to `True` if your datafeed can provide intraday (minutes) history.
    has_daily : bool
        Set to `True` if your datafeed can provide daily history.
    has_weekly_and_monthly : bool
        Set to `True` if your datafeed can provide weekly and monthly history.
    has_empty_bars : bool
        Set to `True` to have the library generate empty bars for periods with no trades.
    has_seconds : bool
        Set to `True` if your datafeed can provide history in seconds.
    has_ticks : bool
        Set to `True` if your datafeed can provide tick data.
    build_seconds_from_ticks : bool
        Set to `True` to allow the library to build second-based resolutions from tick data.
    supported_resolutions : List[str]
        An array of resolution strings that your datafeed supports.
    intraday_multipliers : List[str], optional
        An array of supported intraday (minute) resolutions.
    seconds_multipliers : List[str], optional
        An array of supported second-based resolutions.
    daily_multipliers : List[str], optional
        An array of supported daily resolutions.
    weekly_multipliers : List[str], optional
        An array of supported weekly resolutions.
    monthly_multipliers : List[str], optional
        An array of supported monthly resolutions.
    data_status : str
        The status of the data for this symbol: "streaming", "endofday", or "delayed_streaming".
    delay : int
        The delay in seconds for delayed real-time data. 0 for real-time.
    currency_code : str, optional
        The currency in which the instrument is traded (e.g., "USD", "EUR").
    original_currency_code : str, optional
        The original currency if a conversion has been applied.
    unit_id : str, optional
        The ID of the current unit of measurement for the symbol's price (e.g., "kg", "barrel").
    original_unit_id : str, optional
        The original unit if a conversion has been applied.
    unit_conversion_types : List[str], optional
        An array of unit conversion types that can be applied.
    base_name : List[str], optional
        For spread or expression symbols, this is an array of the base symbols.
    library_custom_fields : Dict, optional
        A dictionary for any custom data you want to associate with the symbol.
    pointvalue : int
        The value of a single point of price movement in the instrument's currency.
    volume_precision : int
        The number of decimal places for the volume values.
    price_source_id : str, optional
        The ID of the default price source for the symbol.
    price_sources : List[Dict], optional
        An array of available price sources for the symbol.
    format : str
        Specifies the formatting for the main series. Either 'price' or 'volume'.
    """

    def __init__(self,
                 tohlcv_df                : pd.DataFrame         = pd.DataFrame(),
                 #
                 ################################################################################### Core Symbol Info
                 #
                 ticker                   : str                  = "TICKER",
                 name                     : Optional[str]        = None,
                 description              : str                  = "Description",
                 long_description         : Optional[str]        = None,
                 type                     : str                  = "crypto",
                 exchange                 : str                  = "EXCHANGE",
                 listed_exchange          : Optional[str]        = None,
                 logo_urls                : Optional[List[str]]  = None,
                 exchange_logo            : Optional[str]        = None,
                 #
                 ################################################################################### Industry Info
                 #
                 sector                   : Optional[str]        = None,
                 industry                 : Optional[str]        = None,
                 #
                 ################################################################################### Session and Time
                 #
                 session                  : str                  = "24x7",
                 session_display          : Optional[str]        = None,
                 timezone                 : str                  = "Etc/UTC",
                 session_holidays         : Optional[str]        = None, # "YYYYMMDD,YYYYMMDD"
                 corrections              : Optional[str]        = None, # "YYYYMMDD,YYYYMMDD"
                 subsessions              : Optional[List[Dict]] = None,
                 subsession_id            : Optional[str]        = None,
                 #
                 ################################################################################### Futures/Options
                 #
                 expired                  : bool                 = False,
                 expiration_date          : Optional[int]        = None, # unix timestamp
                 #
                 ################################################################################### Price Formatting
                 #
                 pricescale               : int                  = 100,
                 minmov                   : int                  = 1,
                 minmov2                  : int                  = 0,
                 fractional               : bool                 = False,
                 variable_tick_size       : Optional[List[Dict]] = None,
                 #
                 ################################################################################### Data Capabilities & Status
                 #
                 has_intraday             : bool                 = True,
                 has_daily                : bool                 = True,
                 has_weekly_and_monthly   : bool                 = True,
                 has_empty_bars           : bool                 = False,
                 has_seconds              : bool                 = True,
                 has_ticks                : bool                 = False,
                 build_seconds_from_ticks : bool                 = False,
                 supported_resolutions    : List[str]            = ["1S", "5S", "1", "5", "15", "30", "60", "D", "W"],
                 intraday_multipliers     : Optional[List[str]]  = None,
                 seconds_multipliers      : Optional[List[str]]  = None,
                 daily_multipliers        : Optional[List[str]]  = None,
                 weekly_multipliers       : Optional[List[str]]  = None,
                 monthly_multipliers      : Optional[List[str]]  = None,
                 data_status              : str                  = "streaming", # "streaming" | "endofday" | "delayed_streaming"
                 delay                    : int                  = 0,
                 #
                 ################################################################################### Units & Currency
                 #
                 currency_code            : Optional[str]        = "USD",
                 original_currency_code   : Optional[str]        = None,
                 unit_id                  : Optional[str]        = None,
                 original_unit_id         : Optional[str]        = None,
                 unit_conversion_types    : Optional[List[str]]  = None,
                 #
                 ################################################################################### Other
                 #
                 base_name                : Optional[List[str]]  = None,
                 library_custom_fields    : Optional[Dict]       = None,
                 pointvalue               : int                  = 1,
                 volume_precision         : int                  = 2,
                 price_source_id          : Optional[str]        = None,
                 price_sources            : Optional[List[Dict]] = None,
                 format                   : str                  = 'price', # 'price' or 'volume'
                 ) :

        self.tohlcv_df                = tohlcv_df
        self.ticker                   = ticker
        self.name                     = name or f"{ticker}_{exchange}"
        self.description              = description
        self.long_description         = long_description
        self.type                     = type
        self.exchange                 = exchange
        self.listed_exchange          = listed_exchange or exchange
        self.logo_urls                = logo_urls
        self.exchange_logo            = exchange_logo
        self.sector                   = sector
        self.industry                 = industry
        self.session                  = session
        self.session_display          = session_display
        self.timezone                 = timezone
        self.session_holidays         = session_holidays
        self.corrections              = corrections
        self.subsessions              = subsessions
        self.subsession_id            = subsession_id
        self.expired                  = expired
        self.expiration_date          = expiration_date
        self.pricescale               = pricescale
        self.minmov                   = minmov
        self.minmov2                  = minmov2
        self.fractional               = fractional
        self.variable_tick_size       = variable_tick_size
        self.has_intraday             = has_intraday
        self.has_daily                = has_daily
        self.has_weekly_and_monthly   = has_weekly_and_monthly
        self.has_empty_bars           = has_empty_bars
        self.has_seconds              = has_seconds
        self.has_ticks                = has_ticks
        self.build_seconds_from_ticks = build_seconds_from_ticks
        self.supported_resolutions    = supported_resolutions
        self.intraday_multipliers     = intraday_multipliers or [res for res in supported_resolutions if 'D' not in res and 'W' not in res and 'M' not in res]
        self.seconds_multipliers      = seconds_multipliers
        self.daily_multipliers        = daily_multipliers or ["1"]
        self.weekly_multipliers       = weekly_multipliers
        self.monthly_multipliers      = monthly_multipliers
        self.data_status              = data_status
        self.delay                    = delay
        self.currency_code            = currency_code
        self.original_currency_code   = original_currency_code
        self.unit_id                  = unit_id
        self.original_unit_id         = original_unit_id
        self.unit_conversion_types    = unit_conversion_types
        self.base_name                = base_name
        self.library_custom_fields    = library_custom_fields
        self.pointvalue               = pointvalue
        self.volume_precision         = volume_precision
        self.price_source_id          = price_source_id
        self.price_sources            = price_sources
        self.format                   = format
        self.full_name                = self.name
        self.visible_plots_set        = "ohlcv"
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
