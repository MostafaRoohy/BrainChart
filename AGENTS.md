# Project overview

First read the following files carefully to fully understand the project's architecture, purpose, conventions, design philosophy, and intended usage:

* `README.md`
* Existing files inside `doc/` IN ORDER

# Important notices

**Important:** Completely ignore the `.backups/` directory.

**Important:** Completely ignore the `todo/` file.

**Important:** If you made any changes, make sure you update affected other codes or other modules of the project.

**Important:** If you made any changes, make sure you update the related or affected documentations inside the `README.md` and the related markdown files inside `doc/` directory.

**Important:** If you made any changes, make sure you update the related or affected test modules that exist inside `test/` directory.

**Important:** If you made any changes, make sure at the end you write a comprehensive commit message that explains what and where and why each change was made. BUT DO NOT COMMIT INTO GIT.

**Important:** DO NOT COMMIT THE CHANGES INTO GIT.

# Code style and formatting guidelines

The codebase has a very distinctive visual style. It is intentionally more tabular, more parenthesized, and more vertically spaced than normal PEP 8 Python.

Do **not** silently normalize it into Black, Ruff-format, autopep8, or generic PEP 8 style. New or edited code must look as if it was written directly beside the existing code.

The rules below are derived from the existing project source and are the default formatting contract for all Python changes.

## 0. Style authority and precedence

When formatting code, use this order of authority:

1. **The exact style of the file being edited.**
2. **The dominant style of neighboring modules in the same package.**
3. **The rules in this `AGENTS.md`.**
4. **Normal Python / PEP 8 conventions only when the project has no established preference.**

Do not use an isolated legacy inconsistency as justification for introducing more inconsistent code.

For example, the overwhelming project convention is:

```python
return (value)
```

A rare existing `return value` is a local deviation. It is **not** precedent for new code.

The same principle applies to parenthesized conditions, visual `#` terminators, type-hint syntax, and alignment.

Also:

* Do not mass-format untouched files.
* Do not reflow unrelated code merely because it is not conventional PEP 8.
* Do not perform broad quote normalization.
* Do not remove visual separators or alignment as "cleanup".
* Keep the diff focused on the requested change and affected code.

---

## 1. Massive module section dividers

Major module-level categories use a three-line wall of hashes. The section name is appended to the **third** hash line.

Canonical pattern:

```python
#
###################################################################################################
###################################################################################################
################################################################################################### Standard Modules
#
```

Common section names in the project include:

* `Standard Modules`
* `My Modules`
* `Logger`
* `Constants`
* `Paths`
* `Internals`
* `Properties`
* `Serialization`
* `Rendering`
* domain-specific categories such as `Candle Data`, `TimeFrame`, `Scorers`, `Validator`, `Search Algorithm`, etc.

The section names must describe **responsibility**, not arbitrary chronology.

Good:

```python
#
###################################################################################################
###################################################################################################
################################################################################################### Constants
#
```

Bad:

```python
# constants
```

Bad:

```python
# ---------------- CONSTANTS ----------------
```

Bad:

```python
###############################################################################
# Constants
###############################################################################
```

For a substantial module, divide the file into meaningful architectural areas instead of leaving one uninterrupted body of code.

A normal module order is approximately:

```text
module explanation / future annotations
Standard Modules
My Modules
Logger
Constants / Paths / configuration
domain types / enums / records
main classes
public API / orchestration
```

This is a semantic order, not a rigid universal template. Match the module's responsibility.

---

## 2. Shorter class-internal subsection dividers

Large classes frequently use a shorter divider to separate groups of methods.

Canonical pattern:

```python
    #
    #################################################################  Properties
    #
```

The exact width varies slightly in existing files. **Match the local file's divider width** instead of inventing a third visual scale.

Typical class subsections include:

```text
Inits
Properties
Internals
HTTP Clients
DataFrames
Population
Dunders
Rendering
Serialization
Public API
```

Use internal dividers only when a class is large enough to benefit from categories. Do not put a giant labeled divider before every two methods like a bureaucrat stamping individual grains of rice.

Good:

```python
    #
    #################################################################  Properties
    #
    @property
    def name(self) -> str:

        return (self._name)
    #
```

---

## 3. Solitary `#` lines are visual end markers

A line containing only `#` is one of the strongest style conventions in the project.

It is **not merely decorative vertical spacing**. It often acts as a visual closing marker for a logical construct, almost like an informal `end` token.

Use a solitary `#` after:

* `if` / `elif` / `else` branches
* `for` loops
* `while` loops
* `try` / `except` / `finally` blocks
* `with` blocks
* function and method definitions
* groups of properties
* class bodies
* large collection declarations where the local file already uses this convention

The `#` normally appears at the indentation level of the construct it visually closes.

### Conditional example

```python
if (value is None):

    value = 0
#
```

### Nested block example

```python
for item in items:

    if (item is None):

        continue
    #

    output.append(item)
#
```

### Branch example

```python
if (is_valid):

    result = data
#
elif (is_empty):

    result = None
#
else:

    raise (ValueError('Bad data'))
#
```

### Method example

```python
    def get_name(self) -> str:

        return (self._name)
    #
```

### Class closure example

```python
class Example:

    def run(self) -> bool:

        return (True)
    #
#
```

Do not delete these markers because they are "empty comments". In this project, they carry visual structure.

---

## 4. Strong vertical whitespace

The code is intentionally airy.

A blank line is placed immediately after the header of nearly every executable block.

This applies to:

```python
def method():

    ...
```

```python
class Example:

    ...
```

```python
if (condition):

    ...
```

```python
for item in items:

    ...
```

```python
while (condition):

    ...
```

```python
try:

    ...
#
except ValueError:

    ...
#
```

```python
with console.capture() as cap:

    ...
#
```

Do not compress blocks into conventional dense Python formatting.

Bad for this project:

```python
def calculate():
    value = 10
    if value > 5:
        return value
```

Correct project style:

```python
def calculate():

    value = 10

    if (value > 5):

        return (value)
    #
#
```

Within a function, blank lines also separate logical phases:

```python
raw      = fetch_data()
filtered = clean_data(raw)

if (filtered.empty):

    return (None)
#

result = calculate(filtered)

return (result)
```

Related assignments remain together. Validation, transformation, execution, and return phases should visually breathe apart.

---

## 5. Vertical alignment is a first-class formatting rule

When multiple adjacent lines are structurally related, format them as a visual table.

### Assignment alignment

```python
self._name               = symbol.name
self._log_name           = symbol.log_name
self._api_chunk_size     = api_chunk_size
self._api_chunk_attempts = api_chunk_attempts
```

### Local variable alignment

```python
attempts     = self._api_chunk_attempts
all_attempts = attempts + 1
success      = False
```

### Annotated field alignment

```python
is_valid              : bool
missing_count         : int
irregular_count       : int
negative_volume_count : int
```

### Type and default alignment

```python
max_evals        : int   | None = 2000
n_initial_random : int   | None = None
n_candidates     : int   | None = 24
random_seed      : int   | None = None
```

### Enum member alignment

```python
AUTO       = 0
EXHAUSTIVE = 1
GENETIC    = 2
TPE        = 3
SMAC       = 4
```

### Dictionary key/value alignment

```python
catalog = {
    SearchAlgorithm.EXHAUSTIVE : (_OptimizerExhaustive, exhaustive_cfg),
    SearchAlgorithm.GENETIC    : (_OptimizerGenetic,    genetic_cfg),
    SearchAlgorithm.TPE        : (_OptimizerTPE,        tpe_cfg),
    SearchAlgorithm.SMAC       : (_OptimizerSMAC,       smac_cfg),
}
#
```

### Related function-call argument alignment

When a multiline call is naturally tabular, align its keyword arguments:

```python
report = Report(
    name        = name,
    total       = total,
    mismatches  = mismatches,
    samples     = samples,
)
```

However, do not pad a single isolated assignment for no reason:

```python
value = 10
```

The alignment rule applies to **adjacent, conceptually related rows**.

When editing an aligned block, re-align the whole affected block if a new identifier changes the alignment width.

---

## 6. Naming conventions

Use conventional Python naming, with the project's strong private-state preference.

### Classes and dataclasses

Use `PascalCase`:

```python
class CandleSet:
class OptimizationResult:
class SmartRateLimiter:
```

### Functions, methods, variables, and parameters

Use `snake_case`:

```python
def normalize_timestamp(...):

def _build_runtime_defaults(...):

retry_after = None
```

### Constants

Use `UPPER_SNAKE_CASE`:

```python
SCHEMA_VERSION       = 1
_DEFAULT_TOL         = 1
_MIN_EVENTS_CONFIDENT = 12
```

Module-private constants should generally begin with `_`:

```python
_DEFAULT_ATOL = 1e-10
```

Public module constants may remain unprefixed:

```python
SCHEMA_VERSION = 1
```

### Internal state and helpers

Use a single leading underscore:

```python
self._symbol
self._candles_df
self._validate_params()
self._build_plot_data()
```

Do not use double-leading-underscore name mangling unless there is a specific technical reason.

### Dunder methods

Use standard protocol names normally:

```python
__init__
__post_init__
__str__
__repr__
__len__
__iter__
__getitem__
```

Do not invent pseudo-dunder names.

---

## 7. Import organization and alignment

When the module has substantial imports, organize them under the normal major dividers.

Canonical structure:

```python
from __future__ import annotations
#
###################################################################################################
###################################################################################################
################################################################################################### Standard Modules
#
import json
import asyncio

import numpy  as np
import pandas as pd

from enum        import Enum
from pathlib     import Path
from dataclasses import dataclass
from typing      import Any, Callable
#
###################################################################################################
###################################################################################################
################################################################################################### My Modules
#
from ..util.logger import get_logger
from .timeframe    import TimeFrame
#
```

Rules:

* Put `from __future__ import annotations` first when the module uses the project's modern annotation style or forward references.
* Standard-library and third-party imports live in `Standard Modules` in the existing project vocabulary.
* Project-relative imports live in `My Modules`.
* Use blank lines to separate conceptual import groups.
* Adjacent `from ... import ...` statements may align the `import` keyword.
* Adjacent relative imports may align module paths and imported names.
* Preserve familiar aliases such as `np` and `pd`.
* Prefer semantic grouping over obsessive alphabetical sorting.
* Do not introduce wildcard imports.
* Do not create import churn unrelated to the task.

Good:

```python
from enum      import Enum, auto
from typing    import Any, overload
from dataclasses import dataclass
```

Also good when alignment is clearer in the local block:

```python
from enum            import Enum
from pathlib         import Path
from typing          import Any, Callable, Iterator, Mapping
from collections.abc import Mapping as MappingABC
```

Match the neighboring import block instead of forcing one global micro-layout.

---

## 8. Type hints are explicit and modern

Type hints are expected on public functions, substantial private helpers, dataclass fields, and important class state.

Prefer built-in generic syntax:

```python
list[str]
dict[str, Any]
tuple[float, float]
set[tuple]
```

Prefer `|` unions:

```python
int|None
int|float|None
np.ndarray|None
Callable[[Any], float]|None
```

Do not introduce `Optional[...]` or `Union[...]` in new code when `|` expresses the type clearly.

### Compact annotations

Inside ordinary inline signatures, there is normally **no space after the colon** and **no spaces around `|`**:

```python
def score(value:float|None, samples:list[int]) -> float:
```

### Aligned annotation tables

In dataclass/configuration tables, spaces may be added around type components to preserve vertical columns:

```python
num_generations      : int   | None = 2_500
mutation_probability : float | None = 0.15
crossover_type       : str   | None = 'uniform'
```

The table alignment is more important than mechanically removing those spaces.

### Return types

Provide explicit return annotations where the type is meaningful:

```python
def max_drawdown(result:BackTestResult) -> float:

def _resolve_closes(...) -> np.ndarray|None:

def as_dict(self) -> dict[str, Any]:
```

Use `-> None` for procedures when appropriate.

### `Any`

`Any` is acceptable at framework boundaries, dynamic registries, serializers, configuration adapters, and deliberately generic orchestration code. Do not replace a known concrete type with `Any` merely to silence the type checker.

---

## 9. Function and method signatures

### Compact signatures

Keep a short signature on one line:

```python
def breakeven_accuracy(binary_payout:float) -> float:

def _clamp01(x:float) -> float:

def get_limiter_for_url(url:str) -> SmartRateLimiter|None:
```

Spacing rules for compact signatures:

* no space before the annotation colon
* no space after the annotation colon
* no spaces around default `=`
* one space after commas
* use `|` for unions
* one space on each side of `->`

Good:

```python
def run(symbol:str, limit:int|None=None, verbose:bool=True) -> bool:
```

Bad:

```python
def run(symbol: str, limit: int | None = None, verbose: bool = True) -> bool:
```

The bad example is valid normal Python style. It is simply not this project's compact signature style.

### Multiline signatures

When a signature becomes long, convert it into a vertical table.

Example:

```python
def validate_strategies(
    vectorized : Any,
    iterative  : Any,
    candle     : Any        = None,
    params     : dict|None  = None,
    **kwargs   : Any,
) -> ValidationReport:
```

Inside classes, the project may use deeper continuation indentation:

```python
    def __init__(
            self,
            symbol             : Symbol,
            *,
            last_n             : int|None       = None,
            last_hours         : int|float|None = None,

            api_chunk_size     : int            = 60,
            api_chunk_attempts : int            = 4,
            async_mode         : bool           = False,
            timeframe          : TimeFrame      = TimeFrame.H01,
        ) -> None:
```

Rules for multiline signatures:

* one significant parameter per line
* align parameter names, `:`, type columns, `=`, and defaults where practical
* use a trailing comma
* place the closing `)` on its own line
* use blank lines to separate conceptual parameter groups
* preserve `*` when keyword-only arguments are part of the API design
* match the continuation indentation already used in that file

Do not create a half-wrapped signature with random parameters hanging at unrelated columns.

---

## 10. Heavy parenthesization is deliberate

The project wraps expressions in parentheses much more aggressively than standard Python.

### Return statements

Returned values are wrapped:

```python
return (df)
return (True)
return (None)
return (self._name)
return (a, b)
```

Do not write new code like:

```python
return df
```

### `if`, `elif`, and `while` conditions

Wrap the complete condition:

```python
if (missing_cols):

if (value is not None):

elif (isinstance(data, pd.DataFrame)):

while (attempt < max_attempts):
```

Do not write:

```python
if missing_cols:
```

### Ternary expressions

Parenthesize the true branch, condition, and false branch:

```python
result = (value) if (condition) else (fallback)
```

Nested ternaries retain explicit grouping:

```python
return (0.0) if (x < 0.0) else ((1.0) if (x > 1.0) else (float(x)))
```

### Raised exception objects

The dominant style also wraps newly raised exception objects:

```python
raise (ValueError('Input dataframe is empty'))
raise (TypeError(f'Unsupported type: {type(value).__name__}'))
raise (RuntimeError('Search produced no valid result'))
```

Exception chaining remains outside the wrapped exception object:

```python
raise (ValueError(f'Cannot restore enum {spec!r}: {e}')) from e
```

### Parenthesized branch values inside larger expressions

The project commonly writes:

```python
candles = (CandleSet(df)) if (return_candleset) else (Candles(df))
choice  = (SearchAlgorithm.EXHAUSTIVE) if (est_ex <= est_ga) else (SearchAlgorithm.GENETIC)
```

Do not "simplify" these parentheses away.

### Do not blindly parenthesize Python grammar

This rule does not mean every token must be entombed in brackets.

Normal loops remain normal:

```python
for item in items:
```

Use parentheses around the iterable only when the iterable expression itself benefits from grouping:

```python
for room, stats in (('train', self.train), ('val', self.val), ('test', self.test)):
```

---

## 11. Double spacing around `and` and `or`

In compound boolean expressions, place **two spaces on both sides** of `and` and `or`.

```python
if (token_0 is None  or  token_1 is None  or  price_0 is None):

if (self._mode == FetchMode.LAST_N  and  self._last_n is None):

if (a.size < 2  or  b.size < 2):

return (self._scores is not None  and  self._scores.diversification >= 60.0)
```

This also applies to compact fallback expressions when they are part of a boolean/fallback chain:

```python
name = getattr(obj, '__qualname__', None)  or  getattr(obj, '__name__', None)  or  type(obj).__name__
```

Bad:

```python
if (a is None or b is None):
```

Bad:

```python
if (a is None   or b is None):
```

Correct:

```python
if (a is None  or  b is None):
```

Existing isolated single-spaced boolean operators are legacy inconsistencies and should not be copied into new code.

---

## 12. General operator and punctuation spacing

Outside the special double-spacing rule for `and` / `or`, use normal readable operator spacing.

```python
total = left + right
ratio = value / count
mask  = values >= threshold
same  = a == b
```

Alignment may intentionally introduce extra spacing:

```python
M01 = (1  * 60.0)
M02 = (2  * 60.0)
M10 = (10 * 60.0)
```

That spacing is used to create columns, not randomly.

### Function calls

Keyword arguments normally use no spaces around `=`:

```python
get_logger(name='Candle', tag='candle')
pd.read_csv(path)
np.asarray(values, dtype=np.float64)
```

### Dictionary entries

Ordinary compact dictionary entries use normal Python punctuation:

```python
out = {'name': name, 'value': value}
```

When dictionary entries form a vertical table, align the colon:

```python
out = {
    'module'   : type(value).__module__,
    'qualname' : type(value).__qualname__,
    'name'     : value.name,
}
#
```

### Comparisons

Prefer readable spacing:

```python
if (start_timestamp >= end_timestamp):
```

Do not deliberately create compressed expressions such as `a==b` in new code merely because a few old lines contain them.

---

## 13. Multiline collections, calls, and expressions

Large structures should expose their shape visually.

### Lists and tuples

```python
_INT8_COLUMNS = [
    'month',
    'day',
    'day_of_week',
    'hour',
    'minute',
    'second',
]
#
```

```python
_optional_cols = (
    'timestamp_close',
    'quote_volume',
    'trade_count',
    'taker_buy_volume',
    'taker_buy_quote_volume',
)
#
```

### Sets

```python
_required_cols = {
    'timestamp',
    'open',
    'high',
    'low',
    'close',
    'volume',
}
#
```

### Large calls

```python
report = Comparison(
    name       = name,
    group      = group,
    passed     = passed,
    detail     = detail,
    total      = total,
    mismatches = mismatches,
    samples    = samples,
)
```

### Large constructor signatures

Use the tabular signature format described earlier instead of forcing a 250-character line.

### Trailing commas

Use trailing commas in multiline literals, calls, and signatures. They make later changes safer and preserve the vertical layout.

### Parentheses for long expressions

When a mathematical or boolean expression needs wrapping, preserve explicit grouping. Do not rely on visually ambiguous operator precedence.

```python
score = (
    (weight_a * value_a)
    + (weight_b * value_b)
    + (weight_c * value_c)
)
```

However, do not split a simple readable expression merely to satisfy an arbitrary 79- or 88-character limit.

---

## 14. Class state, encapsulation, and public data

The project strongly prefers explicit internal state for behavior-rich classes:

```python
self._name      = name
self._data      = data
self._is_update = False
```

Internal helpers also use `_`:

```python
def _validate_data(...):

def _build_group_table(...):

def _resolve_closes(...):
```

### Properties expose internal state

Read-only public access is commonly provided with `@property`:

```python
@property
def name(self) -> str:

    return (self._name)
#
```

For groups of trivial read-only properties, compact one-line forms are accepted when the local class already uses them:

```python
@property
def label_a(self) -> str: return (self._label_a)
#
@property
def label_b(self) -> str: return (self._label_b)
#
```

Do not use the one-line form for properties with validation, branching, mutation, expensive work, or non-obvious semantics.

### Properties are not universal for plain records

Do **not** interpret encapsulation as "every field must be private".

Dataclasses and result records frequently expose public typed fields directly:

```python
@dataclass(slots=True)
class CandleIntegrityReport:

    is_valid      : bool
    timeframe     : TimeFrame|None
    total_rows    : int
    warning_count : int
#
```

Use public dataclass fields for plain data containers. Use private state plus properties for behavior-rich objects whose invariants or implementation details should remain internal.

### Setters are rare

Prefer controlled methods such as `add()`, `update()`, `apply_to()`, or internal population methods over broad property setters. Introduce a property setter only when the existing API genuinely models assignable state.

---

## 15. Dataclasses, `slots`, and immutability

The project uses dataclasses heavily for configuration, reports, records, and immutable data containers.

Examples:

```python
@dataclass(slots=True)
class CandleIntegrityReport:
```

```python
@dataclass(frozen=True)
class GeneticOptimizerConfig:
```

```python
@dataclass(frozen=True, slots=True)
class Candles:
```

Use:

* `slots=True` for compact record/container objects when dynamic attributes are unnecessary.
* `frozen=True` for configuration or value objects that should not be rebound after construction.
* both when the object is explicitly designed as a compact immutable container.
* plain classes when the object has substantial behavior, mutable lifecycle state, caches, or controlled state transitions.

Do not turn every class into a dataclass merely to remove an `__init__`.

Manual `__slots__` is also acceptable for behavior-rich classes when the local implementation uses it:

```python
__slots__ = ('_ranges', '_names', '_doms', '_constraints', '_rng')
#
```

When immutability is part of the class contract, document it in the class docstring and preserve it in implementation details.

---

## 16. Class layout and method ordering

Methods are grouped by responsibility, not alphabetically.

A common class layout is:

```text
class docstring
class constants / __slots__
__init__ / __post_init__
validation or construction helpers
properties
controlled population / mutation methods
dunder protocol methods
private computational helpers
rendering / serialization helpers
public convenience methods
```

Large classes should use short internal section dividers to make these groups explicit.

Example:

```python
class Report:

    """
        Report contract and semantics.
    """

    def __init__(self, ...):

        ...
    #
    #################################################################  Properties
    #
    @property
    def score(self) -> float:

        return (self._score)
    #
    #################################################################  Dunders
    #
    def __str__(self) -> str:

        return (self.summary())
    #
    #################################################################  Rendering
    #
    def _render(self):

        ...
    #
    #################################################################  Serialization
    #
    def to_dict(self) -> dict[str, Any]:

        ...
    #
#
```

Keep closely related sync/async twins near each other when they implement the same operation.

Keep overload declarations immediately above the concrete implementation they describe.

---

## 17. Docstring format and depth

Substantial classes and public methods use descriptive docstrings.

The distinctive project format is:

```python
def calculate_score(result:BackTestResult) -> float:

    """
        Calculate the normalized strategy score.

        Explains the semantics, important assumptions, edge cases, and what the
        return value means to downstream code.
    """

    ...
#
```

Notice:

* a blank line after the `def` / `class` header
* triple double quotes for normal substantial docstrings
* docstring text indented inside the quotes
* a short summary first
* a blank line before deeper explanation
* a blank line after the closing docstring before executable code

### What to document

For important public APIs and non-obvious internal algorithms, explain:

* purpose
* input contract
* output semantics
* invariants
* mutation / immutability behavior
* alignment or timing assumptions
* caching behavior
* exceptional cases
* performance-sensitive behavior
* examples when the API is easy to misuse

Good documentation explains **why the code behaves this way** and **what contract downstream code may rely on**.

Do not write useless docstrings:

```python
"""Get score."""
```

when the score has nontrivial semantics.

### Tiny helpers

A very small internal helper may use a concise one-line docstring when the local file already does so:

```python
def trim_response_text(text:str|None, max_chars:int=300) -> str:

    '''Keep oversized HTTP response bodies bounded in log records.'''

    ...
#
```

For new substantial code, prefer the normal triple-double-quoted multiline format.

### Module-level explanation

Complex analytical modules may begin with a large full-line comment narrative instead of a traditional module docstring. Preserve the local choice.

Do not add a module docstring merely to satisfy a generic style checker if the file already uses a documented comment preamble.

---

## 18. Comments explain intent, hazards, and non-obvious decisions

Comments in this project are often detailed and technical.

Good comments explain:

* why an algorithm exists
* why a threshold or cap is present
* why a seemingly simpler implementation is unsafe
* look-ahead / alignment hazards
* performance costs
* external API quirks
* base-rate or statistical hazards
* lifecycle ownership
* compatibility constraints

Example style:

```python
# The endpoint rejects endTime older than 30 days; the hour of slack absorbs the
# window sliding forward while a long backfill is still running.
```

Another valid style for a dense algorithm:

```python
# The non-answer floor: an empty result must rank below every mild honest loser,
# never at a neutral score the optimizer could crown on an all-negative landscape.
```

Do not narrate obvious syntax:

Bad:

```python
# Increment i by one.
i += 1
```

Prefer full-line comments above the code they explain.

Trailing comments are acceptable in genuinely tabular constant/configuration blocks:

```python
num_generations : int   | None = 2_500   # 2.5k generations
sol_per_pop     : int   | None = 64      # population size
```

or where a short mathematical label makes a table clearer:

```python
same_sign = float(C[0, 0] + C[2, 2])   # red/red + green/green
opp_sign  = float(C[0, 2] + C[2, 0])   # red/green + green/red
```

Do not scatter end-of-line comments across ordinary procedural code.

---

## 19. String and quote style

Single-quoted string literals are dominant in the project:

```python
'name'
'optimizer'
'unknown'
```

Use single quotes by default for new ordinary literals.

Double quotes are acceptable when:

* the string contains apostrophes
* quoting an identifier inside the text is clearer
* the local logging block already uses double-quoted f-strings
* changing the quote style would require ugly escaping

Examples:

```python
raise (ValueError('Input dataframe is empty'))
logger.info(f"Loaded {len(df)} candles from {path}")
raise (ValueError(f'Timeframe "{timeframe.name}" not found'))
```

Do not rewrite unrelated strings solely to make every quote identical.

Use f-strings for interpolation:

```python
logger.debug(f'Built Candles: timeframe={tf.name} rows={len(df)}')
```

Use `!r` when debugging or validating values where representation matters:

```python
raise (ValueError(f'Unknown search algorithm {value!r}'))
```

---

## 20. Logging style

Modules with operational behavior commonly define a module logger in a dedicated `Logger` section:

```python
#
###################################################################################################
###################################################################################################
################################################################################################### Logger
#
logger = get_logger(name='OptResult', tag='optimizer')
#
```

Behavior-rich classes may store or derive a contextual logger when the class needs instance-specific tags.

Prefer structured context inside messages:

```python
logger.debug(f'Built Candles: timeframe={tf.name} rows={len(df)}')
```

```python
self._logger.warning(f'[{self._log_name}] Dataframe integrity check FAILED')
```

Use the correct level:

* `debug` for internal state, flow, requests, cache/build details
* `info` for meaningful successful operational events
* `warning` for recoverable degradation, suspicious data, retries, or partial problems
* `error` for failed operations or invalid states that matter operationally

Log useful context before raising when the failure is operationally important and the surrounding module already follows that pattern.

Do not add raw `print()` calls to library code for debugging. Explicit report/console APIs and CLI-style orchestration code are exceptions when console output is part of their purpose.

Remove temporary debugging output before finalizing a change.

---

## 21. Validation and error handling style

Validate inputs near the boundary where invalid state enters the object or operation.

Typical pattern:

```python
missing_cols = required_cols - set(df.columns)

if (missing_cols):

    logger.error(f'Cannot build Candles: missing required columns {sorted(missing_cols)}')

    raise (ValueError(f'Missing required columns: {sorted(missing_cols)}'))
#
```

Rules:

* fail early on invalid constructor/configuration inputs
* use specific exception classes (`ValueError`, `TypeError`, `KeyError`, `RuntimeError`, etc.)
* include the invalid value or expected contract when it helps debugging
* keep validation branches visually separated
* use `!r` when the exact supplied representation matters
* preserve exception chaining with `from e` when translating an exception
* do not silently swallow broad exceptions unless failure is intentionally converted into a documented fallback

When an exception is deliberately ignored, the reason should be obvious from context or documented:

```python
try:

    self._rate_limiter.report_server_usage(float(used_weight))
#
except (TypeError, ValueError):

    pass
#
```

Broad `except Exception` should generally log context or exist around a deliberately fault-tolerant boundary.

---

## 22. Sync and async twin APIs

Where a component intentionally exposes both synchronous and asynchronous behavior, keep the APIs visibly paired and semantically equivalent.

Typical naming pattern:

```python
def update(self) -> bool:

    ...
#

async def async_update(self) -> bool:

    ...
#
```

Or internal request twins:

```python
def _request(...):

    ...
#

async def _async_request(...):

    ...
#
```

Rules:

* keep argument meaning consistent
* keep return shapes consistent
* keep validation and retry semantics aligned
* use `time.sleep()` only in synchronous code
* use `await asyncio.sleep()` in asynchronous code
* do not call blocking network or sleep operations directly from an async path
* when one implementation mirrors the other, update both when behavior changes

Do not create a sync/async twin merely for symmetry if the project component is intentionally single-mode.

---

## 23. Decorators

Do not introduce custom decorators merely to hide straightforward control flow or reduce a few repeated lines.

Structural Python decorators already used by the project are normal:

```python
@property
@dataclass(...)
@staticmethod
@classmethod
@overload
@abstractmethod
```

Use them when they directly describe the API or object model.

Do not add decorator-heavy metaprogramming, registration magic, retry decorators, caching decorators, or validation decorators when explicit code matches the surrounding project better.

The project generally favors visible, inspectable behavior over clever indirection.

---

## 24. Dunder and protocol implementations

Protocol methods should remain small and direct when possible.

Examples:

```python
def __str__(self) -> str:

    return (self.summary())
#
```

```python
def __repr__(self) -> str:

    return (
        f'<OptimizationResult '
        f'fitness={self._fitness!r} '
        f'algorithm={self._algorithm_used!r}>'
    )
    #
#
```

Use dunder methods to implement real Python protocols, not as an alternative public API naming scheme.

If a class behaves as a mapping, iterator, sequence, or numeric type, keep the protocol semantics unsurprising.

---

## 25. Line length and wrapping

This project does **not** follow a strict 79- or 88-character line limit.

Many existing lines are intentionally long because:

* a signature remains easier to scan on one line
* a logging message contains useful operational context
* an aligned expression is clearer as one row
* a type signature would become harder to read when mechanically wrapped

Therefore:

* do not wrap code solely because a generic formatter would
* preserve a readable one-line expression when its structure is obvious
* wrap genuinely complex calls, signatures, expressions, and literals
* use vertical alignment when wrapping
* avoid absurdly long lines when a structured multiline form is clearer

Good reason to keep one line:

```python
def _estimate_evaluations(algorithm:SearchAlgorithm, space:ParamSpace, exhaustive_cfg:ExhaustiveOptimizerConfig, genetic_cfg:GeneticOptimizerConfig) -> int:
```

Good reason to wrap:

```python
def validate_strategies(
    vectorized : Any,
    iterative  : Any,
    candle     : Any        = None,
    params     : dict|None  = None,
    **kwargs   : Any,
) -> ValidationReport:
```

Choose the form that produces the clearest local visual structure.

---

## 26. Compact one-line bodies are a narrow exception

The dominant style uses full multiline function bodies.

A compact one-line body is accepted mainly for repetitive, trivial, read-only properties in an already compact property table:

```python
@property
def profile_a(self) -> CandleDirectionProfile: return (self._profile_a)
#
@property
def profile_b(self) -> CandleDirectionProfile: return (self._profile_b)
#
```

Do not generalize this into:

```python
def calculate(self): return (self._a + self._b)
```

Do not put branching, mutation, logging, exceptions, or multi-step calculations on the same line as a `def`.

When in doubt, use the normal multiline form.

---

## 27. Group related state and phases visually

Constructor state should be grouped by concept.

Good:

```python
self._name               = symbol.name
self._log_name           = symbol.log_name
self._symbol             = symbol.get_candler_name(self.__class__._candler_key)

self._last_n             = last_n
self._last_hours         = last_hours

self._start_timestamp    = self._normalize_timestamp(start_timestamp)
self._end_timestamp      = self._normalize_timestamp(end_timestamp)

self._api_chunk_size     = api_chunk_size
self._api_chunk_attempts = api_chunk_attempts
self._async_mode         = async_mode
self._timeframe          = timeframe
```

Bad:

```python
self._name = symbol.name
self._last_n = last_n
self._api_chunk_size = api_chunk_size
self._log_name = symbol.log_name
self._end_timestamp = self._normalize_timestamp(end_timestamp)
self._last_hours = last_hours
```

The first version exposes the object's conceptual layout. The second version merely proves that assignment is technically possible, a triumph Python did not need demonstrated again.

The same principle applies inside methods:

```text
normalize inputs
validate
prepare state
execute core logic
finalize result
log
return
```

Separate those phases with blank lines.

---

## 28. Preserve mathematical and domain semantics in formatting

Quantitative code frequently contains dense formulas. Formatting must make the formula's grouping visible and must never change semantics merely to make a line prettier.

Use explicit parentheses:

```python
ratio = ((N - 1.0) / float(N))
score = (int(min(round(N * (1.0 - (ratio ** k))), N)))
```

Align related metrics:

```python
same_sign = float(C[0, 0] + C[2, 2])
opp_sign  = float(C[0, 2] + C[2, 0])
```

For vectorized code:

* keep array shape assumptions visible
* do not hide shifts/alignment inside decorative helpers without reason
* preserve explicit `dtype` where numerical behavior depends on it
* preserve contiguity/read-only operations when they are part of a data contract
* document look-ahead, timestamp, expiry, and alignment semantics when relevant

Formatting must support auditing. This is especially important in trading and statistical code, where a beautiful one-line "cleanup" can quietly move time by one candle and then everyone gets to enjoy a very profitable backtest of the future.

---

## 29. Canonical module skeleton

Use this as a structural reference, not as a demand that every file contain every section:

```python
from __future__ import annotations
#
###################################################################################################
###################################################################################################
################################################################################################### Standard Modules
#
import asyncio

import numpy  as np
import pandas as pd

from dataclasses import dataclass
from typing      import Any
#
###################################################################################################
###################################################################################################
################################################################################################### My Modules
#
from ..util.logger import get_logger
from .model        import Model
#
###################################################################################################
###################################################################################################
################################################################################################### Logger
#
logger = get_logger(name='Example', tag='example')
#
###################################################################################################
###################################################################################################
################################################################################################### Constants
#
_DEFAULT_LIMIT = 100
#
###################################################################################################
###################################################################################################
################################################################################################### Example Record
#
@dataclass(frozen=True, slots=True)
class ExampleRecord:

    name  : str
    value : float
#
###################################################################################################
###################################################################################################
################################################################################################### Example
#
class Example:

    """
        Explain the class contract, important state, and usage semantics.
    """

    def __init__(self, name:str, limit:int=_DEFAULT_LIMIT) -> None:

        self._name  = name
        self._limit = limit

        self._validate()
    #
    #################################################################  Properties
    #
    @property
    def name(self) -> str:

        return (self._name)
    #

    @property
    def limit(self) -> int:

        return (self._limit)
    #
    #################################################################  Internals
    #
    def _validate(self) -> None:

        if (self._limit <= 0):

            raise (ValueError(f'limit must be > 0, got {self._limit}'))
        #
    #
    #################################################################  Public API
    #
    def run(self, values:list[float]) -> np.ndarray:

        """
            Convert `values` to a bounded NumPy array and return it.
        """

        arr = np.asarray(values, dtype=np.float64)

        if (arr.size > self._limit):

            arr = arr[-self._limit:]
        #

        logger.debug(f'Prepared values: name={self._name} rows={arr.size}')

        return (arr)
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#
```

---

## 30. Canonical logic-block example

A normal project-style method should visually resemble this:

```python
def resolve_value(value:float|None, fallback:float=0.0) -> float:

    """
        Resolve an optional numeric value and reject non-finite results.
    """

    result = (fallback) if (value is None) else (float(value))

    if (not np.isfinite(result)):

        raise (ValueError(f'Value must be finite, got {result!r}'))
    #

    if (result < 0.0  or  result > 1.0):

        logger.warning(f'Value outside expected [0, 1] range: value={result}')
    #

    return (result)
#
```

The important visual features are:

1. compact typed signature
2. blank line after `def`
3. project-style indented docstring
4. blank line after docstring
5. parenthesized ternary branches and condition
6. parenthesized `if` conditions
7. double spaces around `or`
8. blank line after each control-flow header
9. solitary `#` closing each logical block
10. parenthesized return value

---

## 31. Style drift to avoid

Do not introduce code formatted like this:

```python
class Processor:
    def __init__(self, data: list[float], use_cache: bool = True):
        self.data = data
        self.use_cache = use_cache

    def run(self) -> list[float]:
        if self.use_cache and len(self.data) > 0:
            return self.data
        else:
            return []
```

Even though this is conventional Python, it conflicts with the project.

Project-style equivalent:

```python
class Processor:

    def __init__(self, data:list[float], use_cache:bool=True) -> None:

        self._data      = data
        self._use_cache = use_cache
    #

    def run(self) -> list[float]:

        if (self._use_cache  and  len(self._data) > 0):

            return (self._data)
        #
        else:

            return ([])
        #
    #
#
```

Before finalizing Python changes, explicitly check that you did **not** accidentally introduce:

* PEP 8-style `if condition:` instead of `if (condition):`
* bare `return value` instead of `return (value)`
* single-spaced compound `and` / `or`
* `param: Type = default` compact signature formatting
* unaligned adjacent assignments or annotated fields
* dense block bodies with no blank line after the header
* missing solitary `#` visual terminators
* generic `# ----- section -----` headers
* public mutable state where the surrounding behavior-rich class uses private state
* `Optional` / `Union` in new code where `|` is appropriate
* wildcard imports
* custom decorator machinery for simple behavior
* raw debug `print()` calls in library code
* mass-formatting of unrelated code
* comments that merely restate syntax
* undocumented changes to timing, alignment, vectorization, or numerical semantics

---

## 32. Final formatting checklist

Before considering a code change complete, inspect the edited code manually and verify:

1. **Sections:** Major responsibilities use the project's large hash dividers where appropriate.
2. **Internal groups:** Large classes use shorter internal dividers when useful.
3. **Visual closure:** Solitary `#` lines close methods and logical blocks consistently with the surrounding file.
4. **Vertical air:** `def`, `class`, conditions, loops, `try`, `except`, and `with` blocks have the expected blank line after their headers.
5. **Alignment:** Related assignments, annotations, enum members, configuration fields, and table-like mappings are vertically aligned.
6. **Parentheses:** Returns, conditions, ternaries, and newly raised exception objects follow the project's heavy-parenthesization style.
7. **Boolean operators:** Compound `and` / `or` expressions use double spacing.
8. **Signatures:** Compact signatures use `name:type=default`; long signatures become aligned vertical tables.
9. **Typing:** Modern built-in generics and `|` unions are used.
10. **State:** Behavior-rich classes use `_private` internal state and properties/control methods where appropriate; plain records may expose public dataclass fields.
11. **Docstrings:** Non-obvious public APIs and algorithms document contracts, assumptions, and hazards rather than stating the method name again in sentence form.
12. **Comments:** Comments explain reasoning, constraints, hazards, or external quirks.
13. **Logging:** Operational code uses the project logger and useful contextual messages.
14. **Errors:** Invalid inputs fail early with specific, informative exceptions.
15. **Local consistency:** The edited block still visually matches the file around it.
16. **No formatter damage:** No automated style cleanup has destroyed the project's deliberate layout.

The final standard is simple: **new code must be visually indistinguishable from the dominant existing project style while remaining explicit, auditable, and easy to scan vertically.**
