
---

# Jaksel Keyword Dictionary (`jaksel_dict1.py`)

## Overview

This file defines a **Jaksel slang keyword mapping** used in the Jaksel programming language project.
The dictionary maps **Jakarta slang (“Jaksel”) expressions** to **Python-like semantic meanings**, enabling a custom, slang-based syntax while preserving familiar programming behavior.

The dictionary is designed to be used by:

* the **lexer/parser** (as reserved words),
* the **compiler backend** (as semantic references),
* or as documentation for supported language constructs.

---

## Purpose

The purpose of this dictionary is to:

* Provide a **localized, culturally contextual syntax** inspired by Jakarta slang
* Maintain **clear correspondence with Python semantics**
* Make the language expressive yet intuitive for beginners
* Support compiler extensibility and readability

This mapping does **not directly execute code**, but acts as a **semantic reference layer** for the compiler.

---

## Keyword Categories

### 1️ Core Control & Structure

| Jaksel Keyword | Meaning    | Description                  |
| -------------- | ---------- | ---------------------------- |
| `yap`          | `print`    | Output to console            |
| `kalo`         | `while`    | Loop while condition is true |
| `burnout`      | `break`    | Exit loop                    |
| `imo`          | `def`      | Define function              |
| `cmiiw`        | `for`      | For-loop                     |
| `gas`          | `continue` | Skip to next iteration       |
| `stop`         | `return`   | Return value from function   |
| `done`         | `pass`     | No-op statement              |

---

### 2️ Conditions & Logic

| Jaksel Keyword | Meaning | Description           |
| -------------- | ------- | --------------------- |
| `whichis`      | `if`    | Conditional statement |
| `otherwise`    | `else`  | Alternative branch    |
| `elifan`       | `elif`  | Else-if condition     |
| `sure`         | `True`  | Boolean true          |
| `nah`          | `False` | Boolean false         |

---

### 3️ Data & Assignment

| Jaksel Keyword | Meaning | Description           |
| -------------- | ------- | --------------------- |
| `itu`          | `=`     | Assignment            |
| `equals`       | `==`    | Equality comparison   |
| `not`          | `!=`    | Inequality comparison |
| `lebih`        | `>`     | Greater-than          |
| `kurang`       | `<`     | Less-than             |
| `plus`         | `+`     | Addition              |
| `minus`        | `-`     | Subtraction           |
| `kali`         | `*`     | Multiplication        |
| `bagi`         | `/`     | Division              |

---

### 4️ Functions & Calls

| Jaksel Keyword | Meaning  | Description         |
| -------------- | -------- | ------------------- |
| `call`         | `call`   | Function invocation |
| `params`       | `args`   | Function parameters |
| `result`       | `return` | Function output     |
| `spill`        | `print`  | Alias for output    |

---

### 5️ Loop Helpers

| Jaksel Keyword | Meaning | Description                  |
| -------------- | ------- | ---------------------------- |
| `rangean`      | `range` | Loop range generator         |
| `step`         | `step`  | Step size (future extension) |

---

### 6️ Error & Flow Handling

| Jaksel Keyword | Meaning     | Description       |
| -------------- | ----------- | ----------------- |
| `confuse`      | `Exception` | Error object      |
| `tryin`        | `try`       | Try block         |
| `excepted`     | `except`    | Exception handler |
| `finallyy`     | `finally`   | Cleanup block     |

---

### 7️ Informal Jaksel Slang (Semantic Placeholders)

These keywords are included for **future extensibility** and stylistic completeness.

| Jaksel Keyword | Meaning   |
| -------------- | --------- |
| `literally`    | `literal` |
| `basically`    | `base`    |
| `honestly`     | `assert`  |
| `idk`          | `None`    |
| `fomo`         | `timeout` |
| `ghosting`     | `ignore`  |
| `bestie`       | `helper`  |
| `bro`          | `peer`    |
| `noted`        | `log`     |
| `otw`          | `pending` |

---

## Data Source

The slang terms were selected from:

> [https://www.english-academy.id/blog/istilah-istilah-gaul-bahasa-jaksel-untuk-menambah-kosakata-bahasa-inggris](https://www.english-academy.id/blog/istilah-istilah-gaul-bahasa-jaksel-untuk-menambah-kosakata-bahasa-inggris)

Only a **subset** of terms was chosen to:

* fit programming semantics,
* align with Python-like syntax,
* avoid ambiguity in parsing.

---

## Design Rationale

* Keywords are **short, expressive, and memorable**
* Slang terms are mapped to **deterministic behavior**
* Grammar-friendly (no symbols that conflict with parsing)
* Supports incremental language growth

---

## Usage Example

```jaksel
imo add(x, y):
    stop x plus y
END

yap add(2, 3)
```

Equivalent Python behavior:

```python
def add(x, y):
    return x + y

print(add(2, 3))
```

---

## Academic Note

This dictionary supports a **source-to-source compiler** design, where:

* Jaksel is the **source language**
* Python is the **target language**
* The mapping aids semantic understanding, not direct execution

---

## License & Usage

This file is intended for **educational use only** as part of a compiler or programming language coursework.

