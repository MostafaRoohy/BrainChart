import pandas as pd

class ChartData:

    '''
    The tohlcv_df must contain 'timestamp', 'open', 'high', 'low', 'close', 'volume' columns
    The 'timestamp' columns must be in milliseconds, and it must be in ascending order.
    '''

    def __init__(self,
                tohlcv_df              = pd.DataFrame(),
                name                   = "name",
                ticker                 = "ticker",
                full_name              = "full_name",
                description            = "description",
                type                   = "type",
                session                = "24x7",
                exchange               = "exchange",
                listed_exchange        = "listed_exchange",
                timezone               = "UTC",
                minmov                 = 1,
                minmov2                = 0,
                pricescale             = 100,
                pointvalue             = 1,
                has_intraday           = True,
                has_daily              = True,
                has_weekly_and_monthly = True,
                currency_code          = "USDT",
                visible_plots_set      = "ohlcv",
                supported_resolutions  = ["1", "5", "15", "30", "60", "240", "D", "W"]
    ):
        
        
        self.tohlcv_df              = tohlcv_df
        self.name                   = name
        self.ticker                 = ticker
        self.full_name              = full_name
        self.description            = description
        self.type                   = type
        self.session                = session
        self.exchange               = exchange
        self.listed_exchange        = listed_exchange
        self.timezone               = timezone
        self.minmov                 = minmov
        self.minmov2                = minmov2
        self.pricescale             = pricescale
        self.pointvalue             = pointvalue
        self.has_intraday           = has_intraday
        self.has_daily              = has_daily
        self.has_weekly_and_monthly = has_weekly_and_monthly
        self.currency_code          = currency_code
        self.visible_plots_set      = visible_plots_set
        self.supported_resolutions  = supported_resolutions
    #
#