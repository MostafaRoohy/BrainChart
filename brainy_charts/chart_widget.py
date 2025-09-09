#
###################################################################################################
###################################################################################################
################################################################################################### index.html builder
#
index_html_raw = r'''
<!-- https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#additional_symbol_info_fields -->

<!DOCTYPE HTML>
<html>

    <head>

        <title>BrainyCharts</title>
        
        <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0">
        <script type="text/javascript" src="/charting_library/charting_library/charting_library.standalone.js"></script>
        <script type="text/javascript" src="/charting_library/datafeeds/udf/dist/bundle.js"></script>

        <script type="text/javascript">

            function getParameterByName(name) 
            {{
                name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
                var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                    results = regex.exec(location.search);
                return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
            }}

            function initOnReady() 
            {{
                var datafeedUrl   = window.location.origin;
                var customDataUrl = getParameterByName('dataUrl');

                if (customDataUrl !== "") 
                {{
                    datafeedUrl = customDataUrl.startsWith('https://') ? customDataUrl : `https://${{customDataUrl}}`;
                }}


                var widget = window.tvWidget = new TradingView.widget(
                {{
                    library_path : "/charting_library/charting_library/",
                    container    : "tv_chart_container",
                    datafeed     : new Datafeeds.UDFCompatibleDatafeed(datafeedUrl, undefined, {{maxResponseLength: 1000, expectedOrder: 'latestFirst'}}),
                    
                    fullscreen : true,
                    theme      : '{theme}',

                    symbol          : '{default_symbol}',
                    interval        : '1',
                    // https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#load_last_chart
                    // load_last_chart : true,

                    // https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets/
                    disabled_features : ["use_localstorage_for_settings"],
                    enabled_features  : ["study_templates"],

                    charts_storage_url         : 'https://saveload.tradingview.com',
                    charts_storage_api_version : "1.1",

                    // custom_indicators_getter: ???
                }});


                window.frames[0].focus();
            }};

            window.addEventListener('DOMContentLoaded', initOnReady, false);

        </script>

    </head>

    <body style="margin:0px;">

        <div id="tv_chart_container"></div>
        
    </body>

</html>
'''
#
###################################################################################################
###################################################################################################
###################################################################################################
#