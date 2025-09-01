# Package Content

Package content

    +/charting_library
        + /bundles
        - charting_library.js
        - charting_library.d.ts
        - charting_library.cjs.js
        - charting_library.esm.js
        - charting_library.standalone.js
        - datafeed-api.d.ts
        - package.json
    +/datafeeds
        + /udf
    - index.html
    - mobile_black.html
    - mobile_white.html
    - test.html

`/charting_library` contains all the library files.

`/charting_library/bundles` stores library internal content and is not intended for other purposes, it should be like "black box" for you so it could be changed anytime without a notice.

`/charting_library/charting_library*` files contain an external library widget interface, they are not supposed to be edited.

+ `.js` is an UMD module (for backward compatibility).
+ `.esm.js` is an native JavaScript module, see import.
+ `.cjs.js` is an CommonJS module.
+ `.standalone.js` is an iife module.
+ `.d.ts` contains TypeScript definitions for the widget interface.

`/charting_library/datafeed-api.d.ts` contains TypeScript definitions for the data feed interface.

`/charting_library/datafeeds/udf/` contains UDF-compatible datafeed wrapper (implements Datafeed API to connect to library and UDF to connect to datafeed). Sample datafeed wrapper implements pulse real-time emulation. You are free to edit its code.

`/index.html` is an example of using library widget on your web page.

`/mobile*.html` are also examples of Widget customization.

`/test.html` is an example of using different library customization features.

All internal JS and CSS codes of the library are inlined and minified to reduce the page load time. Files that are expected to be edited by you were not minified.
