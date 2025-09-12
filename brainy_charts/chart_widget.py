#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal, NewType
from enum import Enum
#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
from .symbol import Symbol
#
###################################################################################################
###################################################################################################
################################################################################################### index.html builder
#
index_html_raw = r'''
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
                return results === null ? ""        : decodeURIComponent(results[1].replace(/\+/g, " "));
            }}

            function initOnReady() 
            {{
                var datafeedUrl   = window.location.origin;
                var customDataUrl = getParameterByName('dataUrl');

                if (customDataUrl !== "") 
                {{
                    datafeedUrl = customDataUrl.startsWith('https://') ? customDataUrl        : `https://${{customDataUrl}}`;
                }}


                var widget = window.tvWidget = new TradingView.widget(
                {{
                    {debug}
                    {library_path}
                    {datafeed}
                    {container}
                    {theme}
                    {symbol}
                    {interval}

                    {timezone}
                    {locale}
                    {autosize}
                    {fullscreen}
                    {height}
                    {width}

                    {favorites}
                    {disabled_features}
                    {enabled_features}

                    {custom_indicators_getter}
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

later_doc_str  = """

    snapshot_url : str, optional
        This URL is used to send a POST request with binary chart snapshots
        when a user clicks the snapshot button.
        This POST request contains multipart/form-data with the field
        preparedImage that represents binary data of the snapshot image
        in image/png format.

    additional_symbol_info_fields        : list[AdditionalSymbolInfoField], optional
        Extra fields to display in the Security Info dialog. Each item:
        `{"title": str, "propertyName": str}` where `propertyName` is a symbol info key.
        Example:
            `[{"title": "Ticker", "propertyName": "ticker"}]`.

    auto_save_delay        : int, optional
        Throttle (seconds) for `onAutoSaveNeeded` callbacks to reduce save frequency.

    charts_storage_api_version        : Literal["1.0","1.1"], optional
        Version of your save/load backend. Study Templates require "1.1".

    charts_storage_url        : str, optional
        Base URL for the high-level save/load REST API. See “Save and load REST API”.

    client_id        : str, optional
        Client identifier used by the high-level save/load charts API.

    compare_symbols        : list[CompareSymbol], optional
        Default custom entries for the Compare window, e.g.
        `[{"symbol": "DAL", "title": "Delta Air Lines"}]`.

    context_menu        : ContextMenuOptions, optional
        Overrides for the right-click context menu. Can also be changed at runtime via
        `IChartingLibraryWidget.onContextMenu`.

    custom_chart_description_function        : ChartDescriptorFunction, optional
        Accessibility hook. Given a `context`, return a string description read by
        screen readers when a chart is focused via Tab, or return `null` to use the
        default. May be async (return a Promise).
        Example (summarized):
            `(ctx) => Promise.resolve(
                "Chart " + (ctx.chartIndex+1) + " of " + ctx.chartCount + ". " +
                ctx.chartTypeName + " chart of " + ctx.symbol + "."
            )`.

    custom_css_url        : str, optional
        Absolute or relative URL to a CSS file injected into the chart (use to style
        widgets outside the plot area—watchlist, etc.).

    custom_font_family        : str, optional
        CSS `font-family` applied to chart (time scale, price scale, panes).
        If using a non-system font, load it in your CSS (e.g. Google Fonts) and then
        reference it here. Format exactly as CSS `font-family`, e.g.
        `"'Inconsolata', monospace"`.

    custom_formatters        : CustomFormatters, optional
        Custom formatting hooks:
        • `timeFormatter.format(Date) -> str`
        • `dateFormatter.format(Date) -> str`
        • `tickMarkFormatter(Date, TickMarkType) -> str` (must format **UTC**)
        • `priceFormatterFactory(symbolInfo, minTick) -> {format(price, signPositive)->str} | null`
        • `studyFormatterFactory(format, symbolInfo) -> {format(value)->str} | null`
        Return `null` from a `*Factory` to fall back to default formatters.

    custom_themes        : CustomThemes, optional
        Color tokens to override built-in light/dark themes.

    custom_timezones        : list[CustomAliasedTimezone], optional
        Define additional timezones beyond the built-in list.

    custom_translate_function        : Callable[[str, str, str], str | None], optional
        i18n override for UI strings. Receives `(originalText, singularOriginalText,
        translatedText)` and should return a new translation string or `None` to use
        the default. Example: rename “Trend Line” to “Line Drawing”.

    drawings_access        : AccessList, optional
        Whitelist/blacklist and restrictions for drawing tools (same structure as
        `studies_access`). Special case: font-based drawings are grouped under
        `"Font Icons"` and cannot be toggled individually.

    header_widget_buttons_mode        : HeaderWidgetButtonsMode, optional
        Button layout mode for the top toolbar. Default is adaptive (full size on
        wide windows; iconified on narrow). Example: `"fullsize"`.

    image_storage_adapter        : IImageStorageAdapter, optional
        **Experimental.** Custom storage backend for images added via the image
        drawing tool. Useful if you don’t want images embedded in saved layouts.

    load_last_chart        : bool, optional
        If True, loads the user’s last saved chart (after you implement save/load).
        **Precedence:** If `symbol` is set, it overrides the saved symbol. To honor
        the saved symbol, omit `symbol` when enabling `load_last_chart`.

    loading_screen        : LoadingScreenOptions, optional
        Spinner customization: `{backgroundColor?: str, foregroundColor?: str}`.

    numeric_formatting        : NumericFormattingParams, optional
        Number formatting options. Currently supports `decimal_sign` (e.g. `{ "decimal_sign": "," }`).

    overrides        : dict[str, Any], optional
        Programmatic overrides for widget-editable properties (series style, scales,
        colors, etc.). Keys follow the “Widget Overrides” naming (e.g.
        `"mainSeriesProperties.style": 2` for Line). **Note:** `overrides` do **not**
        change values already persisted in user settings; use `settings_overrides` to
        override persisted values.

    save_load_adapter        : IExternalSaveLoadAdapter, optional
        Custom implementation of save/load operations (if you don’t use the built-in
        REST endpoints). See “API handlers”.

    saved_data        : dict, optional
        A pre-saved chart layout to load at widget creation. For deferred loading,
        call `IChartingLibraryWidget.load()` instead.

    saved_data_meta_info        : SavedStateMetaInfo, optional
        Meta information associated with `saved_data`.

    settings_adapter        : ISettingsAdapter, optional
        Custom storage for user settings (get/set/remove and optional
        `initialSettings`). Use to centralize persistence on your backend and bypass
        localStorage.

    settings_overrides        : dict[str, Any], optional
        Forced values for settings that override anything loaded from localStorage or
        a `settings_adapter`. Use this when you need to supersede persisted user
        choices. Similar structure to `overrides`, but **applies to persisted
        settings**.

    studies_access        : AccessList, optional
        Whitelist/blacklist and restrictions for indicators (studies). Example:
        ```
        {
        "type": "black" | "white",
        "tools": [{"name": "<study name>", "grayed": true}, ...]
        }
        ```

    studies_overrides        : dict[str, Any], optional
        Overrides for built-in indicators’ inputs/styles and for the Compare series.
        Keys follow “StudyOverrides” naming, e.g. `"volume.volume.color.0": "#00FFFF"`.

    study_count_limit        : int, optional
        Maximum concurrent studies allowed in the layout (min 2).

    symbol_search_complete        : Callable[[str, SearchSymbolResultItem|None], Awaitable[dict]],
        optional
        Async override for symbol selection from Symbol Search (not used for
        watchlist additions). Receives raw input and an optional selected item; must
        resolve to `{"symbol": str, "name": str}`. Useful to gather extra user input
        before deciding the final symbol.

    symbol_search_request_delay        : int, optional
        Debounce (milliseconds) for symbol search requests as the user types.

    time_frames        : list[TimeFrameItem], optional
        Items shown on the bottom time-frame toolbar. Each item:
        • `text`: label (e.g., `"3y"`, `"50y"`, `"3d"`)  
        • `resolution`: resolution to apply (e.g., `"1D"`, `"6M"`, `"5"`)  
        • `description`: human description  
        • `title`: optional alternate label

    time_scale        : TimeScaleOptions, optional
        Extra control over bar density/spacing, e.g. `{ "min_bar_spacing": 10 }`.

    timeframe        : str | dict, optional
        Default visible time range:
        • Relative: `'3D'`, `'6M'`, etc. (`D` = days, `M` = months)
        • Fixed range: `{"from": <unix>, "to": <unix>}`
        Note: Even with a fixed range, the chart still requests data up to “now” to
        allow forward scrolling.

    toolbar_bg        : str, optional
        Toolbar background color (CSS color).

    user_id        : str, optional
        User identifier for the high-level save/load charts API.

    Notes
    -----
    • **Precedence (favorites & settings):**
    `settings_adapter` (if present) > localStorage (if enabled) > `favorites`.
    Use `settings_overrides` to supersede persisted values; `overrides` only
    affects current in-memory properties.

    • **Accessibility:** Provide `custom_chart_description_function` for screen
    readers if your layout includes multiple charts or non-obvious visual states.

    • **Formatting:** `tickMarkFormatter` must format UTC time.

    • **Performance:** Use `auto_save_delay` and `symbol_search_request_delay` to
    control backend load. `autosize` avoids layout thrash from manual sizing.

    • **Persistence:** Choose one path—`charts_storage_url/client_id/user_id` or a
    `save_load_adapter`. Mixing is possible but clarify ownership of records.

    Examples
    --------
    Minimal UDF setup:
        widget = new TradingView.widget({
            container: "tv_chart_container",
            interval: "1D",
            symbol: "AAPL",
            locale: "en",
            datafeed: new Datafeeds.UDFCompatibleDatafeed("https://demo_feed.tradingview.com"),
            library_path: "charting_library/",
            autosize: True,
        })

    Custom formatters (UTC tick marks & scientific price for a study):
        custom_formatters = {
            "tickMarkFormatter": lambda date, t: f"T{date.getUTCHours()}:{date.getUTCMinutes()}",
            "studyFormatterFactory": lambda fmt, _si: (
                {"format": lambda v: Intl.NumberFormat("en-US", {"notation": "scientific"}).format(v)}
                if fmt["type"] == "price" else None
            )
        }

    Fixed range:
        timeframe = {"from": 1640995200, "to": 1643673600}  # 2022-01-01 .. 2022-02-01

    Symbol search override:
        async def symbol_search_complete(raw, item=None):
            sym  = getNewSymbol(raw, item)
            name = getHumanFriendlyName(sym, item)
            return {"symbol": sym, "name": name}
    """
#
###################################################################################################
###################################################################################################
################################################################################################### Objects
#
JavaScriptCode = NewType('JavaScriptCode', str)


class ThemeName(Enum):

    light = 'light'
    dark  = 'dark'

    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class ChartingLibraryFeatureset(Enum):

    use_localstorage_for_settings                                  = "use_localstorage_for_settings"
    items_favoriting                                               = "items_favoriting"
    save_chart_properties_to_local_storage                         = "save_chart_properties_to_local_storage"
    create_volume_indicator_by_default                             = "create_volume_indicator_by_default"
    create_volume_indicator_by_default_once                        = "create_volume_indicator_by_default_once"
    volume_force_overlay                                           = "volume_force_overlay"
    right_bar_stays_on_scroll                                      = "right_bar_stays_on_scroll"
    constraint_dialogs_movement                                    = "constraint_dialogs_movement"
    charting_library_debug_mode                                    = "charting_library_debug_mode"
    side_toolbar_in_fullscreen_mode                                = "side_toolbar_in_fullscreen_mode"
    header_in_fullscreen_mode                                      = "header_in_fullscreen_mode"
    disable_resolution_rebuild                                     = "disable_resolution_rebuild"
    chart_scroll                                                   = "chart_scroll"
    chart_zoom                                                     = "chart_zoom"
    horz_touch_drag_scroll                                         = "horz_touch_drag_scroll"
    vert_touch_drag_scroll                                         = "vert_touch_drag_scroll"
    mouse_wheel_scroll                                             = "mouse_wheel_scroll"
    pressed_mouse_move_scroll                                      = "pressed_mouse_move_scroll"
    mouse_wheel_scale                                              = "mouse_wheel_scale"
    pinch_scale                                                    = "pinch_scale"
    axis_pressed_mouse_move_scale                                  = "axis_pressed_mouse_move_scale"
    low_density_bars                                               = "low_density_bars"
    uppercase_instrument_names                                     = "uppercase_instrument_names"
    no_min_chart_width                                             = "no_min_chart_width"
    fix_left_edge                                                  = "fix_left_edge"
    lock_visible_time_range_on_resize                              = "lock_visible_time_range_on_resize"
    shift_visible_range_on_new_bar                                 = "shift_visible_range_on_new_bar"
    custom_resolutions                                             = "custom_resolutions"
    end_of_period_timescale_marks                                  = "end_of_period_timescale_marks"
    cropped_tick_marks                                             = "cropped_tick_marks"
    study_overlay_compare_legend_option                            = "study_overlay_compare_legend_option"
    study_symbol_ticker_description                                = "study_symbol_ticker_description"
    auto_enable_symbol_labels                                      = "auto_enable_symbol_labels"
    insert_indicator_dialog_shortcut                               = "insert_indicator_dialog_shortcut"
    two_character_bar_marks_labels                                 = "two_character_bar_marks_labels"
    confirm_overwrite_if_chart_layout_with_name_exists             = "confirm_overwrite_if_chart_layout_with_name_exists"
    determine_first_data_request_size_using_visible_range          = "determine_first_data_request_size_using_visible_range"
    move_logo_to_main_pane                                         = "move_logo_to_main_pane"
    study_templates                                                = "study_templates"
    datasource_copypaste                                           = "datasource_copypaste"
    seconds_resolution                                             = "seconds_resolution"
    tick_resolution                                                = "tick_resolution"
    secondary_series_extend_time_scale                             = "secondary_series_extend_time_scale"
    header_widget                                                  = "header_widget"
    header_symbol_search                                           = "header_symbol_search"
    symbol_search_hot_key                                          = "symbol_search_hot_key"
    allow_arbitrary_symbol_search_input                            = "allow_arbitrary_symbol_search_input"
    header_resolutions                                             = "header_resolutions"
    show_interval_dialog_on_key_press                              = "show_interval_dialog_on_key_press"
    header_chart_type                                              = "header_chart_type"
    header_settings                                                = "header_settings"
    header_indicators                                              = "header_indicators"
    header_compare                                                 = "header_compare"
    header_undo_redo                                               = "header_undo_redo"
    header_quick_search                                            = "header_quick_search"
    header_screenshot                                              = "header_screenshot"
    header_fullscreen_button                                       = "header_fullscreen_button"
    border_around_the_chart                                        = "border_around_the_chart"
    header_saveload                                                = "header_saveload"
    left_toolbar                                                   = "left_toolbar"
    control_bar                                                    = "control_bar"
    timeframes_toolbar                                             = "timeframes_toolbar"
    legend_widget                                                  = "legend_widget"
    display_legend_on_all_charts                                   = "display_legend_on_all_charts"
    object_tree_legend_mode                                        = "object_tree_legend_mode"
    edit_buttons_in_legend                                         = "edit_buttons_in_legend"
    show_hide_button_in_legend                                     = "show_hide_button_in_legend"
    format_button_in_legend                                        = "format_button_in_legend"
    delete_button_in_legend                                        = "delete_button_in_legend"
    context_menus                                                  = "context_menus"
    pane_context_menu                                              = "pane_context_menu"
    scales_context_menu                                            = "scales_context_menu"
    legend_context_menu                                            = "legend_context_menu"
    main_series_scale_menu                                         = "main_series_scale_menu"
    display_market_status                                          = "display_market_status"
    remove_library_container_border                                = "remove_library_container_border"
    property_pages                                                 = "property_pages"
    show_chart_property_page                                       = "show_chart_property_page"
    chart_property_page_scales                                     = "chart_property_page_scales"
    chart_property_page_trading                                    = "chart_property_page_trading"
    chart_property_page_right_margin_editor                        = "chart_property_page_right_margin_editor"
    countdown                                                      = "countdown"
    dont_show_boolean_study_arguments                              = "dont_show_boolean_study_arguments"
    hide_last_na_study_output                                      = "hide_last_na_study_output"
    symbol_info                                                    = "symbol_info"
    timezone_menu                                                  = "timezone_menu"
    snapshot_trading_drawings                                      = "snapshot_trading_drawings"
    source_selection_markers                                       = "source_selection_markers"
    go_to_date                                                     = "go_to_date"
    adaptive_logo                                                  = "adaptive_logo"
    show_dom_first_time                                            = "show_dom_first_time"
    hide_left_toolbar_by_default                                   = "hide_left_toolbar_by_default"
    chart_style_hilo                                               = "chart_style_hilo"
    chart_style_hilo_last_price                                    = "chart_style_hilo_last_price"
    pricescale_currency                                            = "pricescale_currency"
    pricescale_unit                                                = "pricescale_unit"
    scales_date_format                                             = "scales_date_format"
    popup_hints                                                    = "popup_hints"
    save_shortcut                                                  = "save_shortcut"
    show_right_widgets_panel_by_default                            = "show_right_widgets_panel_by_default"
    show_object_tree                                               = "show_object_tree"
    show_spread_operators                                          = "show_spread_operators"
    hide_exponentiation_spread_operator                            = "hide_exponentiation_spread_operator"
    hide_reciprocal_spread_operator                                = "hide_reciprocal_spread_operator"
    compare_symbol_search_spread_operators                         = "compare_symbol_search_spread_operators"
    studies_symbol_search_spread_operators                         = "studies_symbol_search_spread_operators"
    hide_resolution_in_legend                                      = "hide_resolution_in_legend"
    hide_unresolved_symbols_in_legend                              = "hide_unresolved_symbols_in_legend"
    show_zoom_and_move_buttons_on_touch                            = "show_zoom_and_move_buttons_on_touch"
    hide_main_series_symbol_from_indicator_legend                  = "hide_main_series_symbol_from_indicator_legend"
    hide_price_scale_global_last_bar_value                         = "hide_price_scale_global_last_bar_value"
    show_average_close_price_line_and_label                        = "show_average_close_price_line_and_label"
    hide_image_invalid_symbol                                      = "hide_image_invalid_symbol"
    hide_object_tree_and_price_scale_exchange_label                = "hide_object_tree_and_price_scale_exchange_label"
    scales_time_hours_format                                       = "scales_time_hours_format"
    use_na_string_for_not_available_values                         = "use_na_string_for_not_available_values"
    pre_post_market_sessions                                       = "pre_post_market_sessions"
    show_percent_option_for_right_margin                           = "show_percent_option_for_right_margin"
    lock_visible_time_range_when_adjusting_percentage_right_margin = "lock_visible_time_range_when_adjusting_percentage_right_margin"
    iframe_loading_compatibility_mode                              = "iframe_loading_compatibility_mode"
    use_last_visible_bar_value_in_legend                           = "use_last_visible_bar_value_in_legend"
    symbol_info_long_description                                   = "symbol_info_long_description"
    symbol_info_price_source                                       = "symbol_info_price_source"
    chart_template_storage                                         = "chart_template_storage"
    request_only_visible_range_on_reset                            = "request_only_visible_range_on_reset"
    clear_price_scale_on_error_or_empty_bars                       = "clear_price_scale_on_error_or_empty_bars"
    legend_inplace_edit                                            = "legend_inplace_edit"
    show_symbol_logos                                              = "show_symbol_logos"
    show_exchange_logos                                            = "show_exchange_logos"
    show_symbol_logo_in_legend                                     = "show_symbol_logo_in_legend"
    show_symbol_logo_for_compare_studies                           = "show_symbol_logo_for_compare_studies"
    always_show_legend_values_on_mobile                            = "always_show_legend_values_on_mobile"
    studies_extend_time_scale                                      = "studies_extend_time_scale"
    accessible_keyboard_shortcuts                                  = "accessible_keyboard_shortcuts"
    aria_detailed_chart_descriptions                               = "aria_detailed_chart_descriptions"
    aria_crosshair_price_description                               = "aria_crosshair_price_description"
    saveload_separate_drawings_storage                             = "saveload_separate_drawings_storage"
    disable_pulse_animation                                        = "disable_pulse_animation"
    iframe_loading_same_origin                                     = "iframe_loading_same_origin"
    library_custom_color_themes                                    = "library_custom_color_themes"
    use_symbol_name_for_header_toolbar                             = "use_symbol_name_for_header_toolbar"
    intraday_inactivity_gaps                                       = "intraday_inactivity_gaps"

    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class AvailableSaveloadVersions(Enum):

    v_1_0 = "1.0" 
    v_1_1 = "1.1" 

    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class LoadingScreenOptions:

    def __init__(self, background_color:str=None, foreground_color:str=None):

        if (background_color is None  and  foreground_color is None):

            raise
        #

        self.loading_screen_options = {}

        if (background_color is not None):

            self.loading_screen_options["backgroundColor"] = background_color
        #
        if (foreground_color is not None):

            self.loading_screen_options["foregroundColor"] = foreground_color
        #
    #


    def __str__(self):

        return '{' + ', '.join(f'{k}: "{v}"' for k, v in self.loading_screen_options.items()) + '}'
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class HeaderWidgetButtonsMode(Enum):

    fullsize = "fullsize"
    adaptive = "adaptive"
    compact  = "compact"

    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class ChartDescriptorFunction(Enum):

    pass
    #https://www.tradingview.com/charting-library-docs/latest/api/modules/Charting_Library/#chartdescriptorfunction

    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class TimeScaleOptions:

    def __init__(self, min_bar_spacing:float=None):

        if (min_bar_spacing is None):

            raise
        #

        self.time_scale_options = {"min_bar_spacing":min_bar_spacing}
    #


    def __str__(self):

        return '{' + ', '.join(f'{k}: {v}' for k, v in self.time_scale_options.items()) + '}'
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

class TimeFrameItem:

    def __init__(self, description:str=None, resolution:ResolutionString=None, text:str=None, title:str=None):

        if (resolution is None  or  text is None):

            raise
        #

        self.time_frame = {}

        if (description is not None):
         
            self.time_frame["description"] = description
        #
        if (resolution is not None):
         
            self.time_frame["resolution"] = resolution
        #
        if (text is not None):
         
            self.time_frame["text"] = text
        #
        if (title is not None):
         
            self.time_frame["title"] = title
        #
    #


    def __str__(self):

        return '{' + ', '.join(f'{k}: "{v}"' for k, v in self.time_frame.items()) + '}'
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class TimeframeOption:

    def __init__(self, relative_time:ResolutionString=None, from_timestamp_s:int=None, to_timestamp_s:int=None):

        if (relative_time is None  and  (from_timestamp_s is None  or  to_timestamp_s is None)):

            raise
        #

        if (relative_time is not None):

            self.timeframe = relative_time
        #
        else:

            self.timeframe =  {"from": from_timestamp_s, "to": to_timestamp_s}
        #
    #


    def __str__(self):
    
        if isinstance(self.timeframe, dict):

            return '{' + ', '.join(f'{k}: "{v}"' for k, v in self.timeframe.items()) + '}'
        #

        return f'"{self.timeframe}"'
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class LanguageCode(Enum):

    ar     = "ar"
    zh     = "zh"
    ca_ES  = "ca_ES"
    en     = "en"
    fr     = "fr"
    de     = "de"
    he_IL  = "he_IL"
    id_ID  = "id_ID"
    it     = "it"
    ja     = "ja"
    ko     = "ko"
    pl     = "pl"
    pt     = "pt"
    ru     = "ru"
    es     = "es"
    sv     = "sv"
    th     = "th"
    tr     = "tr"
    vi     = "vi"
    ms_MY  = "ms_MY"
    zh_TW  = "zh_TW"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class Timezone(Enum):

    exchange = "exchange" 
    Etc_UTC = "Etc/UTC"

    Africa_Cairo = "Africa/Cairo" 
    Africa_Casablanca = "Africa/Casablanca" 
    
    Africa_Johannesburg        = "Africa/Johannesburg"
    Africa_Lagos               = "Africa/Lagos"
    Africa_Nairobi             = "Africa/Nairobi"
    Africa_Tunis               = "Africa/Tunis"
    America_Anchorage          = "America/Anchorage"
    America_Argentina_Buenos_Aires = "America/Argentina/Buenos_Aires"
    America_Bogota             = "America/Bogota"
    America_Caracas            = "America/Caracas"
    America_Chicago            = "America/Chicago"
    America_El_Salvador        = "America/El_Salvador"
    America_Juneau             = "America/Juneau"
    America_Lima               = "America/Lima"
    America_Los_Angeles        = "America/Los_Angeles"
    America_Mexico_City        = "America/Mexico_City"
    America_New_York           = "America/New_York"
    America_Phoenix            = "America/Phoenix"
    America_Santiago           = "America/Santiago"
    America_Sao_Paulo          = "America/Sao_Paulo"
    America_Toronto            = "America/Toronto"
    America_Vancouver          = "America/Vancouver"
    Asia_Almaty                = "Asia/Almaty"
    Asia_Ashkhabad             = "Asia/Ashkhabad"
    Asia_Bahrain               = "Asia/Bahrain"
    Asia_Bangkok               = "Asia/Bangkok"
    Asia_Chongqing             = "Asia/Chongqing"
    Asia_Colombo               = "Asia/Colombo"
    Asia_Dhaka                 = "Asia/Dhaka"
    Asia_Dubai                 = "Asia/Dubai"
    Asia_Ho_Chi_Minh           = "Asia/Ho_Chi_Minh"
    Asia_Hong_Kong             = "Asia/Hong_Kong"
    Asia_Jakarta               = "Asia/Jakarta"
    Asia_Jerusalem             = "Asia/Jerusalem"
    Asia_Karachi               = "Asia/Karachi"
    Asia_Kathmandu             = "Asia/Kathmandu"
    Asia_Kolkata               = "Asia/Kolkata"
    Asia_Kuala_Lumpur          = "Asia/Kuala_Lumpur"
    Asia_Kuwait                = "Asia/Kuwait"
    Asia_Manila                = "Asia/Manila"
    Asia_Muscat                = "Asia/Muscat"
    Asia_Nicosia               = "Asia/Nicosia"
    Asia_Qatar                 = "Asia/Qatar"
    Asia_Riyadh                = "Asia/Riyadh"
    Asia_Seoul                 = "Asia/Seoul"
    Asia_Shanghai              = "Asia/Shanghai"
    Asia_Singapore             = "Asia/Singapore"
    Asia_Taipei                = "Asia/Taipei"
    Asia_Tehran                = "Asia/Tehran"
    Asia_Tokyo                 = "Asia/Tokyo"
    Asia_Yangon                = "Asia/Yangon"
    Atlantic_Azores            = "Atlantic/Azores"
    Atlantic_Reykjavik         = "Atlantic/Reykjavik"
    Australia_Adelaide         = "Australia/Adelaide"
    Australia_Brisbane         = "Australia/Brisbane"
    Australia_Perth            = "Australia/Perth"
    Australia_Sydney           = "Australia/Sydney"
    Europe_Amsterdam           = "Europe/Amsterdam"
    Europe_Athens              = "Europe/Athens"
    Europe_Belgrade            = "Europe/Belgrade"
    Europe_Berlin              = "Europe/Berlin"
    Europe_Bratislava          = "Europe/Bratislava"
    Europe_Brussels            = "Europe/Brussels"
    Europe_Bucharest           = "Europe/Bucharest"
    Europe_Budapest            = "Europe/Budapest"
    Europe_Copenhagen          = "Europe/Copenhagen"
    Europe_Dublin              = "Europe/Dublin"
    Europe_Helsinki            = "Europe/Helsinki"
    Europe_Istanbul            = "Europe/Istanbul"
    Europe_Lisbon              = "Europe/Lisbon"
    Europe_London              = "Europe/London"
    Europe_Luxembourg          = "Europe/Luxembourg"
    Europe_Madrid              = "Europe/Madrid"
    Europe_Malta               = "Europe/Malta"
    Europe_Moscow              = "Europe/Moscow"
    Europe_Oslo                = "Europe/Oslo"
    Europe_Paris               = "Europe/Paris"
    Europe_Prague              = "Europe/Prague"
    Europe_Riga                = "Europe/Riga"
    Europe_Rome                = "Europe/Rome"
    Europe_Stockholm           = "Europe/Stockholm"
    Europe_Tallinn             = "Europe/Tallinn"
    Europe_Vienna              = "Europe/Vienna"
    Europe_Vilnius             = "Europe/Vilnius"
    Europe_Warsaw              = "Europe/Warsaw"
    Europe_Zurich              = "Europe/Zurich"
    Pacific_Auckland           = "Pacific/Auckland"
    Pacific_Chatham            = "Pacific/Chatham"
    Pacific_Fakaofo            = "Pacific/Fakaofo"
    Pacific_Honolulu           = "Pacific/Honolulu"
    Pacific_Norfolk            = "Pacific/Norfolk"
    US_Mountain                = "US/Mountain"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class DrawingOverrides(Enum):

    FivepointspatternLineToolOverrides = "FivepointspatternLineToolOverrides" 

    AbcdLineToolOverrides                   = "AbcdLineToolOverrides"
    AnchoredvpLineToolOverrides             = "AnchoredvpLineToolOverrides"
    AnchoredvwapLineToolOverrides           = "AnchoredvwapLineToolOverrides"
    ArcLineToolOverrides                    = "ArcLineToolOverrides"
    ArrowLineToolOverrides                  = "ArrowLineToolOverrides"
    ArrowmarkdownLineToolOverrides          = "ArrowmarkdownLineToolOverrides"
    ArrowmarkerLineToolOverrides            = "ArrowmarkerLineToolOverrides"
    ArrowmarkleftLineToolOverrides          = "ArrowmarkleftLineToolOverrides"
    ArrowmarkrightLineToolOverrides         = "ArrowmarkrightLineToolOverrides"
    ArrowmarkupLineToolOverrides            = "ArrowmarkupLineToolOverrides"
    BalloonLineToolOverrides                = "BalloonLineToolOverrides"
    BarspatternLineToolOverrides            = "BarspatternLineToolOverrides"
    BeziercubicLineToolOverrides            = "BeziercubicLineToolOverrides"
    BezierquadroLineToolOverrides           = "BezierquadroLineToolOverrides"
    BrushLineToolOverrides                  = "BrushLineToolOverrides"
    CalloutLineToolOverrides                = "CalloutLineToolOverrides"
    CircleLineToolOverrides                 = "CircleLineToolOverrides"
    CommentLineToolOverrides                = "CommentLineToolOverrides"
    CrosslineLineToolOverrides              = "CrosslineLineToolOverrides"
    CypherpatternLineToolOverrides          = "CypherpatternLineToolOverrides"
    DisjointangleLineToolOverrides          = "DisjointangleLineToolOverrides"
    ElliottcorrectionLineToolOverrides      = "ElliottcorrectionLineToolOverrides"
    ElliottdoublecomboLineToolOverrides     = "ElliottdoublecomboLineToolOverrides"
    ElliottimpulseLineToolOverrides         = "ElliottimpulseLineToolOverrides"
    ElliotttriangleLineToolOverrides        = "ElliotttriangleLineToolOverrides"
    ElliotttriplecomboLineToolOverrides     = "ElliotttriplecomboLineToolOverrides"
    EllipseLineToolOverrides                = "EllipseLineToolOverrides"
    EmojiLineToolOverrides                  = "EmojiLineToolOverrides"
    ExecutionLineToolOverrides              = "ExecutionLineToolOverrides"
    ExtendedLineToolOverrides               = "ExtendedLineToolOverrides"
    FibchannelLineToolOverrides             = "FibchannelLineToolOverrides"
    FibcirclesLineToolOverrides             = "FibcirclesLineToolOverrides"
    FibretracementLineToolOverrides         = "FibretracementLineToolOverrides"
    FibspeedresistancearcsLineToolOverrides = "FibspeedresistancearcsLineToolOverrides"
    FibspeedresistancefanLineToolOverrides  = "FibspeedresistancefanLineToolOverrides"
    FibtimezoneLineToolOverrides            = "FibtimezoneLineToolOverrides"
    FibwedgeLineToolOverrides               = "FibwedgeLineToolOverrides"
    FlagmarkLineToolOverrides               = "FlagmarkLineToolOverrides"
    FlatbottomLineToolOverrides             = "FlatbottomLineToolOverrides"
    GanncomplexLineToolOverrides            = "GanncomplexLineToolOverrides"
    GannfanLineToolOverrides                = "GannfanLineToolOverrides"
    GannfixedLineToolOverrides              = "GannfixedLineToolOverrides"
    GannsquareLineToolOverrides             = "GannsquareLineToolOverrides"
    GhostfeedLineToolOverrides              = "GhostfeedLineToolOverrides"
    HeadandshouldersLineToolOverrides       = "HeadandshouldersLineToolOverrides"
    HighlighterLineToolOverrides            = "HighlighterLineToolOverrides"
    HorzlineLineToolOverrides               = "HorzlineLineToolOverrides"
    HorzrayLineToolOverrides                = "HorzrayLineToolOverrides"
    IconLineToolOverrides                   = "IconLineToolOverrides"
    ImageLineToolOverrides                  = "ImageLineToolOverrides"
    InfolineLineToolOverrides               = "InfolineLineToolOverrides"
    InsidepitchforkLineToolOverrides        = "InsidepitchforkLineToolOverrides"
    OrderLineToolOverrides                  = "OrderLineToolOverrides"
    ParallelchannelLineToolOverrides        = "ParallelchannelLineToolOverrides"
    PathLineToolOverrides                   = "PathLineToolOverrides"
    PitchfanLineToolOverrides               = "PitchfanLineToolOverrides"
    PitchforkLineToolOverrides              = "PitchforkLineToolOverrides"
    PolylineLineToolOverrides               = "PolylineLineToolOverrides"
    PositionLineToolOverrides               = "PositionLineToolOverrides"
    PredictionLineToolOverrides             = "PredictionLineToolOverrides"
    PricelabelLineToolOverrides             = "PricelabelLineToolOverrides"
    ProjectionLineToolOverrides             = "ProjectionLineToolOverrides"
    RayLineToolOverrides                    = "RayLineToolOverrides"
    RegressiontrendLineToolOverrides        = "RegressiontrendLineToolOverrides"
    RiskrewardlongLineToolOverrides         = "RiskrewardlongLineToolOverrides"
    RiskrewardshortLineToolOverrides        = "RiskrewardshortLineToolOverrides"
    RotatedrectangleLineToolOverrides       = "RotatedrectangleLineToolOverrides"
    SchiffpitchforkLineToolOverrides        = "SchiffpitchforkLineToolOverrides"
    Schiffpitchfork2LineToolOverrides       = "Schiffpitchfork2LineToolOverrides"
    SignpostLineToolOverrides               = "SignpostLineToolOverrides"
    SinelineLineToolOverrides               = "SinelineLineToolOverrides"
    StickerLineToolOverrides                = "StickerLineToolOverrides"
    TextLineToolOverrides                   = "TextLineToolOverrides"
    TextabsoluteLineToolOverrides           = "TextabsoluteLineToolOverrides"
    ThreedriversLineToolOverrides           = "ThreedriversLineToolOverrides"
    TimecyclesLineToolOverrides             = "TimecyclesLineToolOverrides"
    TrendangleLineToolOverrides             = "TrendangleLineToolOverrides"
    TrendbasedfibextensionLineToolOverrides = "TrendbasedfibextensionLineToolOverrides"
    TrendbasedfibtimeLineToolOverrides      = "TrendbasedfibtimeLineToolOverrides"
    TrendlineLineToolOverrides              = "TrendlineLineToolOverrides"
    TriangleLineToolOverrides               = "TriangleLineToolOverrides"
    TrianglepatternLineToolOverrides        = "TrianglepatternLineToolOverrides"
    VertlineLineToolOverrides               = "VertlineLineToolOverrides"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class NumericFormattingParams:

    def __init__(self, decimal_sign:str=None, grouping_separator:str=None):

        if (decimal_sign is None  and  grouping_separator is None):

            raise
        #


        self.numeric_formatting = {}

        if (decimal_sign is not None):

            self.numeric_formatting["decimal_sign"] = decimal_sign
        #
        if (grouping_separator is not None):

            self.numeric_formatting["grouping_separator"] = grouping_separator
        #
    #


    def __str__(self):

        return '{' + ', '.join(f'{k}: "{v}"' for k, v in self.numeric_formatting.items()) + '}'
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class CompareSymbol:

    def __init__(self, symbol:str=None, title:str=None):

        if (symbol is None  and  title is None):

            raise
        #


        self.compare_symbols = {}

        if (symbol is not None):

            self.compare_symbols["symbol"] = symbol
        #
        if (title is not None):

            self.compare_symbols["title"] = title
        #
    #


    def __str__(self):

        return '{' + ', '.join(f'{k}: "{v}"' for k, v in self.compare_symbols.items()) + '}'
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class SavedStateMetaInfo:

    def __init__(self, description:str=None, name:str=None, uid:int=None):

        if (description is None  and  name is None  and  uid is None):

            raise
        #


        self.saved_data_meta_info = {}

        if (description is not None):

            self.saved_data_meta_info["description"] = description
        #
        if (name is not None):

            self.saved_data_meta_info["name"] = name
        #
        if (uid is not None):

            self.saved_data_meta_info["uid"] = uid
        #
    #



    def __str__(self):

        return '{' + ', '.join(f'{k}: "{v}"' for k, v in self.saved_data_meta_info.items()) + '}'
    #

    def __repr__(self):

        return (self.__str__())
    #
#
#################################################
#
class ChartTypeFavorites(Enum):

    Area            = "Area"
    Bars            = "Bars"
    Candles         = "Candles"
    Heiken_Ashi     = "Heiken Ashi"
    Hollow_Candles  = "Hollow Candles"
    Line            = "Line"
    Line_Break      = "Line Break"
    Baseline        = "Baseline"
    LineWithMarkers = "LineWithMarkers"
    Stepline        = "Stepline"
    Columns         = "Columns"
    High_low        = "High-low"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class DrawingToolIdentifier(Enum):

    arrow                           = "arrow"
    cursor                          = "cursor"
    dot                             = "dot"
    eraser                          = "eraser"
    LineTool5PointsPattern          = "LineTool5PointsPattern"
    LineToolABCD                    = "LineToolABCD"
    LineToolArc                     = "LineToolArc"
    LineToolArrow                   = "LineToolArrow"
    LineToolArrowMarkDown           = "LineToolArrowMarkDown"
    LineToolArrowMarker             = "LineToolArrowMarker"
    LineToolArrowMarkLeft           = "LineToolArrowMarkLeft"
    LineToolArrowMarkRight          = "LineToolArrowMarkRight"
    LineToolArrowMarkUp             = "LineToolArrowMarkUp"
    LineToolBarsPattern             = "LineToolBarsPattern"
    LineToolBezierCubic             = "LineToolBezierCubic"
    LineToolBezierQuadro            = "LineToolBezierQuadro"
    LineToolBrush                   = "LineToolBrush"
    LineToolCallout                 = "LineToolCallout"
    LineToolCircle                  = "LineToolCircle"
    LineToolCircleLines             = "LineToolCircleLines"
    LineToolComment                 = "LineToolComment"
    LineToolCrossLine               = "LineToolCrossLine"
    LineToolCypherPattern           = "LineToolCypherPattern"
    LineToolDateAndPriceRange       = "LineToolDateAndPriceRange"
    LineToolDateRange               = "LineToolDateRange"
    LineToolDisjointAngle           = "LineToolDisjointAngle"
    LineToolElliottCorrection       = "LineToolElliottCorrection"
    LineToolElliottDoubleCombo      = "LineToolElliottDoubleCombo"
    LineToolElliottImpulse          = "LineToolElliottImpulse"
    LineToolElliottTriangle         = "LineToolElliottTriangle"
    LineToolElliottTripleCombo      = "LineToolElliottTripleCombo"
    LineToolEllipse                 = "LineToolEllipse"
    LineToolExtended                = "LineToolExtended"
    LineToolFibChannel              = "LineToolFibChannel"
    LineToolFibCircles              = "LineToolFibCircles"
    LineToolFibRetracement          = "LineToolFibRetracement"
    LineToolFibSpeedResistanceArcs  = "LineToolFibSpeedResistanceArcs"
    LineToolFibSpeedResistanceFan   = "LineToolFibSpeedResistanceFan"
    LineToolFibSpiral               = "LineToolFibSpiral"
    LineToolFibTimeZone             = "LineToolFibTimeZone"
    LineToolFibWedge                = "LineToolFibWedge"
    LineToolFixedRangeVolumeProfile = "LineToolFixedRangeVolumeProfile"
    LineToolFlagMark                = "LineToolFlagMark"
    LineToolFlatBottom              = "LineToolFlatBottom"
    LineToolGannComplex             = "LineToolGannComplex"
    LineToolGannFan                 = "LineToolGannFan"
    LineToolGannFixed               = "LineToolGannFixed"
    LineToolGannSquare              = "LineToolGannSquare"
    LineToolGhostFeed               = "LineToolGhostFeed"
    LineToolHeadAndShoulders        = "LineToolHeadAndShoulders"
    LineToolHighlighter             = "LineToolHighlighter"
    LineToolHorzLine                = "LineToolHorzLine"
    LineToolHorzRay                 = "LineToolHorzRay"
    LineToolInfoLine                = "LineToolInfoLine"
    LineToolInsidePitchfork         = "LineToolInsidePitchfork"
    LineToolNote                    = "LineToolNote"
    LineToolNoteAbsolute            = "LineToolNoteAbsolute"
    LineToolParallelChannel         = "LineToolParallelChannel"
    LineToolPath                    = "LineToolPath"
    LineToolPitchfan                = "LineToolPitchfan"
    LineToolPitchfork               = "LineToolPitchfork"
    LineToolPolyline                = "LineToolPolyline"
    LineToolPrediction              = "LineToolPrediction"
    LineToolPriceLabel              = "LineToolPriceLabel"
    LineToolTextNote                = "LineToolTextNote"
    LineToolPriceRange              = "LineToolPriceRange"
    LineToolProjection              = "LineToolProjection"
    LineToolRay                     = "LineToolRay"
    LineToolRectangle               = "LineToolRectangle"
    LineToolRegressionTrend         = "LineToolRegressionTrend"
    LineToolRiskRewardLong          = "LineToolRiskRewardLong"
    LineToolRiskRewardShort         = "LineToolRiskRewardShort"
    LineToolRotatedRectangle        = "LineToolRotatedRectangle"
    LineToolSchiffPitchfork         = "LineToolSchiffPitchfork"
    LineToolSchiffPitchfork2        = "LineToolSchiffPitchfork2"
    LineToolSignpost                = "LineToolSignpost"
    LineToolSineLine                = "LineToolSineLine"
    LineToolText                    = "LineToolText"
    LineToolTextAbsolute            = "LineToolTextAbsolute"
    LineToolThreeDrivers            = "LineToolThreeDrivers"
    LineToolTimeCycles              = "LineToolTimeCycles"
    LineToolTrendAngle              = "LineToolTrendAngle"
    LineToolTrendBasedFibExtension  = "LineToolTrendBasedFibExtension"
    LineToolTrendBasedFibTime       = "LineToolTrendBasedFibTime"
    LineToolTrendLine               = "LineToolTrendLine"
    LineToolTriangle                = "LineToolTriangle"
    LineToolTrianglePattern         = "LineToolTrianglePattern"
    LineToolVer                     = "LineToolVer"


    def __str__(self):

        return self.value
    #

    def __repr__(self):

        return (self.__str__())
    #
#

class Favorites:

    def __init__(self, chart_type_favortes:list[ChartTypeFavorites]=None, drawing_tools_favorites:list[DrawingToolIdentifier]=None, indicators:list[str]=None, intervals:list[ResolutionString]=None):
        
        if (chart_type_favortes is None  and  drawing_tools_favorites is None  and  indicators is None  and  intervals is None):

            raise
        #


        self.favorites = {}

        if (chart_type_favortes is not None):

            self.favorites['chartTypes'] = chart_type_favortes
        #
        if (drawing_tools_favorites is not None):

            self.favorites['drawingTools'] = drawing_tools_favorites
        #
        if (indicators is not None):

            self.favorites['indicators'] = indicators
        #
        if (intervals is not None):

            self.favorites['intervals'] = intervals
        #
    #


    def __str__(self):

        favorites_str = ', '.join(f"{key}: {[str(value)  for value in values]}" for key, values in self.favorites.items())
        return f"{{{favorites_str}}}"
    #

    def __repr__(self):

        return (self.__str__())
    #
#
###################################################################################################
###################################################################################################
################################################################################################### ChartWidget
#
class ChartWidget:

    """
    These parameters mirror the `ChartingLibraryWidgetOptions` interface and control
    data connectivity, UI/UX, persistence, localization, theming, accessibility, and
    performance. Unless otherwise stated, parameters are optional.
    
    For furthor information, please visit:
    https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/

    Parameters
    ----------

    debug : bool, optional
        If True, logs verbose Datafeed API traces to the browser console.
        `Default=False`

    library_path : str, required
        Static path to the charting library assets.
        `Default="/charting_library/charting_library/"`

    datafeed : JavaScriptCode, required
        Datafeed implementation supplying symbols, history, and (optionally) quotes/streaming.
        Example:
            `new Datafeeds.UDFCompatibleDatafeed("https://demo_feed.tradingview.com")`.
        `Default=new Datafeeds.UDFCompatibleDatafeed(datafeedUrl, undefined, {maxResponseLength: 1000, expectedOrder: 'latestFirst'})`

    container : str, required
        Container element id for the widget iframe
        `Default="tv_chart_container"`

    theme :ThemeName, optional
        Predefined theme.
        `Default=ThemeName.dark`

    symbol : Symbol, required
        Default instrument symbol.
        If provided, it overrides `load_last_chart`’s saved symbol.
        `Default=Symbol()`

    interval : ResolutionString, required
        Initial chart resolution (e.g., `"1D"`, `"60"`, `"5"`, `"1W"`).
        `Default=ResolutionString(1, Frame.m)`





    timezone : Timezone, optional
        Default timezone for the time scale. Use `"exchange"` for the exchange’s
        timezone, or supply a specific zone (e.g., `"America/New_York"`). Override
        via `overrides` if needed.
        `Default=Timezone.Etc_UTC`

    locale : LanguageCode, optional
        UI locale/language code (e.g., `"en"`, `"de"`, `"zh_TW"`).
        `Default=LanguageCode.en`

    autosize : bool, optional
        If True, the chart uses all available container space and resizes with it.
        Default in library: False. Prefer this over manually managing `width`/`height`.
        `Default=True`

    fullscreen : bool, optional
        If True, the widget occupies the entire window. Default in library: False.
        `Default=True`

    height : int, optional
        Widget height (pixels). Ensure the container has enough space. Prefer
        `fullscreen`/`autosize` when possible. (Avoid setting `"100%"` here.)

    width : int, optional
        Widget width (pixels). Ensure the container can accommodate it. Prefer
        `fullscreen`/`autosize` when possible. (Avoid setting `"100%"` here.)


        


    favorites : Favorites[ChartTypeFavorites], optional
        Default favorites for a new user/browser (intervals, indicators, drawings,
        chartTypes).
        To allow users to add/remove items from favorites, enable the `items_favoriting` featureset.
        Note that favorites saved in `localStorage` take precedence over the ones specified
        in the `favorites` property. Therefore, the library tries to load the favorites from
        `localStorage` first, and then use the elements in favorites if there is nothing
        saved in `localStorage`. If you want the elements specified within `favorites` to
        always apply, disable `localStorage` using the `use_localstorage_for_settings` featureset.

    disabled_features : list[ChartingLibraryFeatureset], optional
        Features to disable by default (names from “Featuresets”), e.g.
        `["header_widget", "left_toolbar"]`.
        `Default=["use_localstorage_for_settings"]`

    enabled_features : list[ChartingLibraryFeatureset], optional
        Features to enable by default (names from “Featuresets”), e.g.
        `["move_logo_to_main_pane"]`.





    custom_indicators_getter : JavaScriptCode, optional
        Async factory that returns your custom indicator descriptors. Receives `PineJS`
        to access helper functions.
    """

    def __init__(self,
                 #
                 # region params V1
                 #
                 ################################################################################################## Urgent
                 #
                 debug                                    : Optional[bool]                                 = False,
                 library_path                             : str                                            = "/charting_library/charting_library/",
                 datafeed                                 : JavaScriptCode                                 = r'''new Datafeeds.UDFCompatibleDatafeed(datafeedUrl, undefined, {maxResponseLength: 1000, expectedOrder: 'latestFirst'})''',
                 container                                : str                                            = "tv_chart_container",
                 theme                                    : Optional[ThemeName]                            = ThemeName.dark,
                 symbol                                   : Symbol                                         = Symbol(),
                 interval                                 : Optional[ResolutionString]                     = ResolutionString(1, Frame.m),
                 #
                 ################################################################################################## Essential
                 #
                 timezone                                 : Optional[Timezone]                             = Timezone.Etc_UTC,
                 locale                                   : Optional[LanguageCode]                         = LanguageCode.en,
                 autosize                                 : Optional[bool]                                 = True,
                 fullscreen                               : Optional[bool]                                 = True,
                 height                                   : Optional[int]                                  = None,
                 width                                    : Optional[int]                                  = None,
                 #
                 ################################################################################################## Good
                 #
                 favorites                                : Optional[Favorites]                            = None,
                 disabled_features                        : Optional[list[ChartingLibraryFeatureset]]      = ["use_localstorage_for_settings", "uppercase_instrument_names", ],
                 enabled_features                         : Optional[list[ChartingLibraryFeatureset]]      = ["seconds_resolution", "tick_resolution", ],
                 #
                 ################################################################################################## Custom Indicator and Study
                 #
                 custom_indicators_getter                 : Optional[JavaScriptCode]                       = None,
                 #
                 ################################################################################################## .
                 #
                 # endregion
                 #
                 # region params V2. These params will be implemented in V2
                 #
                 ################################################################################################## Saving and loading chart
                 #
                 snapshot_url                             : Optional[str]                                  = None,
                 charts_storage_url                       : Optional[str]                                  = None,
                 charts_storage_api_version               : Optional[AvailableSaveloadVersions]            = AvailableSaveloadVersions.v_1_1,
                 client_id                                : Optional[str]                                  = None,
                 user_id                                  : Optional[str]                                  = None,
                 load_last_chart                          : Optional[bool]                                 = None,
                 saved_data                               : Optional[Any]                                  = None,
                 auto_save_delay                          : Optional[int]                                  = None,
                 saved_data_meta_info                     : Optional[SavedStateMetaInfo]                   = None,
                 #
                 ################################################################################################## .
                 #
                 settings_adapter                         : Optional[Any]                                  = None,
                 settings_overrides                       : Optional[dict[str, str|int|bool]]              = None,
                 save_load_adapter                        : Optional[Any]                                  = None,
                 image_storage_adapter                    : Optional[Any]                                  = None,
                 #
                 ################################################################################################## .
                 #
                 drawings_access                          : Optional[Any]                                  = None,
                 studies_access                           : Optional[Any]                                  = None,
                 study_count_limit                        : Optional[int]                                  = None,
                 #
                 ################################################################################################## .
                 #
                 studies_overrides                        : Optional[Any]                                  = None,
                 overrides                                : Optional[dict[DrawingOverrides, str|int|bool]] = None,
                 #
                 ################################################################################################## .
                 #
                 numeric_formatting                       : Optional[NumericFormattingParams]              = None,
                 custom_formatters                        : Optional[Any]                                  = None,
                 custom_translate_function                : Optional[Any]                                  = None,
                 custom_timezones                         : Optional[Any]                                  = None,
                 #
                 ################################################################################################### .
                 #
                 custom_themes                            : Optional[Any]                                  = None,
                 custom_css_url                           : Optional[str]                                  = None,
                 custom_font_family                       : Optional[str]                                  = None,
                 #
                 ################################################################################################## .
                 #
                 compare_symbols                          : Optional[list[CompareSymbol]]                  = None,
                 additional_symbol_info_fields            : Optional[list[dict[str,str]]]                  = None,
                 symbol_search_complete                   : Optional[Any]                                  = None,
                 symbol_search_request_delay              : Optional[int]                                  = None,
                 #
                 ################################################################################################## .
                 #
                 timeframe                                : Optional[TimeframeOption]                      = None,
                 time_frames                              : Optional[list[TimeFrameItem]]                  = None,
                 time_scale                               : Optional[TimeScaleOptions]                     = None,
                 #
                 ################################################################################################## .
                 #
                 context_menu                             : Optional[Any]                                  = None,
                 toolbar_bg                               : Optional[str]                                  = None,
                 loading_screen                           : Optional[LoadingScreenOptions]                 = None,
                 header_widget_buttons_mode               : Optional[HeaderWidgetButtonsMode]              = None,
                 #
                 ################################################################################################## .
                 #
                 custom_chart_description_function        : Optional[ChartDescriptorFunction]              = None
                 #
                 ################################################################################################## .
                 #
                 #endregion
                 #
                ):
        

        self.debug                    = ("") if (debug                    is None) else (f"debug                    : {str(debug).lower()},")
        self.library_path             = ("") if (library_path             is None) else (f"library_path             : '{library_path}',")
        self.datafeed                 = ("") if (datafeed                 is None) else (f"datafeed                 : {datafeed},")
        self.container                = ("") if (container                is None) else (f"container                : '{container}',")
        self.theme                    = ("") if (theme                    is None) else (f"theme                    : '{theme}',")
        self.symbol                   = ("") if (symbol                   is None) else (f"symbol                   : '{symbol.ticker}',")
        self.interval                 = ("") if (interval                 is None) else (f"interval                 : '{interval}',")

        self.timezone                 = ("") if (timezone                 is None) else (f"timezone                 : '{timezone}',")
        self.locale                   = ("") if (locale                   is None) else (f"locale                   : '{locale}',")
        self.autosize                 = ("") if (autosize                 is None) else (f"autosize                 : {str(autosize).lower()},")
        self.fullscreen               = ("") if (fullscreen               is None) else (f"fullscreen               : {str(fullscreen).lower()},")
        self.height                   = ("") if (height                   is None) else (f"height                   : {height},")
        self.width                    = ("") if (width                    is None) else (f"width                    : {width},")

        self.favorites                = ("") if (favorites                is None) else (f"favorites                : {favorites},")
        self.disabled_features        = ("") if (disabled_features        is None) else (f"disabled_features        : {[f"{feat}" for feat in disabled_features]},")
        self.enabled_features         = ("") if (enabled_features         is None) else (f"enabled_features         : {[f"{feat}" for feat in enabled_features]},")

        self.custom_indicators_getter = ("") if (custom_indicators_getter is None) else (f"custom_indicators_getter : {custom_indicators_getter},")
    #

    def _generate_index_html(self):

        bc_dir           = Path(__file__).parent
        chart_widget_dir = bc_dir/"frontend"/"chart_widget"
        chart_widget_dir.mkdir(parents=True, exist_ok=True)
        frontend_file    = chart_widget_dir/"index.html"
        
        with open(frontend_file, "w") as file:

            file.write(index_html_raw.format(
                                             debug=self.debug, library_path=self.library_path, datafeed=self.datafeed, container=self.container, theme=self.theme, symbol=self.symbol, interval=self.interval,

                                             timezone=self.timezone, locale=self.locale, autosize=self.autosize, fullscreen=self.fullscreen, height=self.height, width=self.width,

                                             favorites=self.favorites, disabled_features=self.disabled_features, enabled_features=self.enabled_features,

                                             custom_indicators_getter=self.custom_indicators_getter
                                            ))
        #

        return (frontend_file)
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#
