#
# https://www.tradingview.com/charting-library-docs/latest/connecting_data/Symbology
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.SymbolExt/
#
###################################################################################################
###################################################################################################
###################################################################################################
#
import pandas as pd
from typing import List, Dict, Optional, Any, Literal

Literal()
#
###################################################################################################
###################################################################################################
################################################################################################### Symbol Model
# 52 in site
class Symbol:

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