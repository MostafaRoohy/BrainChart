#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
import pandas as pd
from typing import List, Dict, Optional, Any, Literal
#
###################################################################################################
###################################################################################################
################################################################################################### Symbol Model
#
class Symbol:

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


# 52 in site
class CompleteSymbol:

    def __init__(self,

                 tohlcv_df                : pd.DataFrame                                                    = pd.DataFrame(),
                 #
                 ################################################################################### Core Symbol Info
                 # 9
                 ticker                   : Optional[str]       = "TICKER",
                 name                     : str                 = None,
                 description              : str                 = "Description",
                 long_description         : Optional[str]       = None,
                 type                     : str                 = "crypto",
                 exchange                 : str                 = "EXCHANGE",
                 listed_exchange          : Optional[str]       = None,
                 logo_urls                : Optional[List[str]] = None,
                 exchange_logo            : Optional[str]       = None,
                 #
                 ################################################################################### Industry Info
                 # 2
                 sector                   : Optional[str] = None,
                 industry                 : Optional[str] = None,
                 #
                 ################################################################################### Session and Time
                 # 7
                 session                  : str                 = "24x7",
                 session_display          : str                 = None,
                 timezone                 : str                 = "Etc/UTC",
                 session_holidays         : str                 = None,
                 corrections              : Optional[str]       = None,
                 subsessions              : Optional[List[str]] = None,
                 subsession_id            : Optional[str]       = None,
                 #
                 ################################################################################### Futures/Options
                 # 2
                 expired                  : bool          = False,
                 expiration_date          : Optional[int] = None,
                 #
                 ################################################################################### Price Formatting
                 # 6
                 format                   : Literal["price", "volume"] = "price",
                 pricescale               : int            = 100,
                 minmov                   : int            = 1,
                 minmove2                 : Optional[int]  = 0,
                 fractional               : Optional[bool] = False,
                 variable_tick_size       : Optional[str]  = None,
                 #
                 ################################################################################### Data Capabilities & Status
                 # 15
                 has_daily                : Optional[bool] = True,
                 has_intraday             : Optional[bool] = False,
                 has_seconds              : Optional[bool] = False,
                 has_ticks                : Optional[bool] = False,
                 has_weekly_and_monthly   : Optional[bool] = False,
                 has_empty_bars           : Optional[bool] = False,
                 build_seconds_from_ticks : Optional[bool] = False,
 
                 data_status              : Optional[Literal["streaming", "endofday", "delayed_streaming"]] = None,
                 delay                    : Optional[int]  = None,

                 # Resolutions
                 supported_resolutions    : Optional[List[str]] = None,
                 intraday_multipliers     : Optional[List[str]] = [],
                 seconds_multipliers      : Optional[List[str]] = None,
                 daily_multipliers        : Optional[List[str]] = ["1"],
                 weekly_multipliers       : Optional[List[str]] = ["1"],
                 monthly_multipliers      : Optional[List[str]] = ["1"],
                 #
                 ################################################################################### Units & Currency
                 # 11
                 currency_code            : Optional[str]                  = "USD",
                 original_currency_code   : Optional[str]                  = None,
                 unit_id                  : Optional[str]                  = None,
                 original_unit_id         : Optional[str]                  = None,
                 unit_conversion_types    : Optional[List[str]]            = None,

                 # Price sources
                 price_source_id          : Optional[str]                  = None,
                 price_sources            : Optional[List[Dict[str, str]]] = None,

                 # Composition/custom
                 base_name                : Optional[List[str]]            = None,
                 library_custom_fields    : Optional[Dict[str, Any]]       = None, # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/#library_custom_fields

                 # Visible plots & volume precision
                 visible_plots_set        : Optional[str]                  = "ohlcv",
                 volume_precision         : Optional[str]                  = "0",
                ):

        pass
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#