# MyC-Lite Lexical Analyzer Simulator with Symbol Table Management

A web-based compiler construction simulator designed to demonstrate the step-by-step internal mechanics of the **Lexical Analysis Phase** of a compiler. This application parses a custom educational language specification named **MyC-Lite** character-by-character, displays live token generation metrics, maintains a simulated physical memory symbol table, and leverages complex static analysis constraints to report syntax anomalies with interactive error diagnostics.

---

## 🚀 Key Architectural Features

* **State Machine Character-by-Character Scanning:** Bypasses opaque high-level regex split matching functions to expose direct raw compiler operations.
* **Live Lexical Analysis Trace Mode:** Exposes structural timeline snapshots detailing exactly how individual text characters transition into validated lexemes.
* **Symbol Table Management:** Tracks and dynamically maps active variables, types, globally scoped properties, and simulated sequential physical hexadecimal memory tracking parameters ($0x3E8$).
* **Static Analysis Warnings:** Includes advanced architectural constraints checking for clean code rules (e.g., catching identifiers that are too short to preserve code readability).
* **Visual Pipeline Flow Animation:** Highlights the target compiler pipeline block active at each checkpoint of the lexical sweep.
* **Academic Dashboard Reference System:** Embeds language specifications directly within the UI to optimize developer reference constraints during evaluation.

---

## 🛠️ Language Specification Grid (MyC-Lite)

| Specification Boundary | Operational Constraints Ruleset | Valid Examples | Invalid / Fragment Fallbacks |
| :--- | :--- | :--- | :--- |
| **Identifier Prefix Flagging** | Must instantiate explicitly matching `v_` (Variables), `fn_` (Functions), or `c_` (Constants) properties. | `v_total`, `fn_calc`, `c_PI` | `total`, `marks` |
| **Identifier Maximum Capacity** | Strict execution barrier set at **20 characters maximum**. | `v_studentMarks` | `v_thisNameIsWayTooLong` |
| **Static Analysis Warning Layer** | Identifiers with raw inner payload sizes less than **3 characters** prompt readability warnings. | `v_a`, `fn_x` *(Generates Warning)* | N/A |
| **Prefix Integrity Interceptor** | Standalone prefixes without tail additions are intercepted immediately. | N/A | `v_`, `fn_`, `c_` *(Generates Error)* |
| **Educational Keywords** | Injects custom execution flow control primitives. | `begin`, `end`, `display`, `input`, `repeat`, `until` | N/A |

---

## 📁 Repository Directory Hierarchy

```text
myc_lite_lexer/
│
├── app.py                     # Primary Application Initialization Entry Point
├── routes.py                  # Orchestrates Central Flask Routing & AJAX Endpoints
├── lexer.py                   # State Machine Scanner Implementation Engine
├── symbol_table.py            # Simulated Memory & Symbol Structural Datastore
├── error_handler.py           # Custom Error & Structural Warning Classes
│
├── templates/
│   └── index.html             # Single-Page Academic Dashboard Frontend View
│
└── static/
    ├── css/
    │   └── style.css          # Production UI Grid System Layout
    └── js/
        └── script.js          # Client-Side AJAX Engine & Animation Pipeline
