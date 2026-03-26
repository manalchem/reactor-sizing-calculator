# Ideal Reactor Sizing Calculator

A command-line Python tool for calculating the required volume of ideal chemical reactors (CSTR and PFR) for a first-order irreversible liquid-phase reaction. Built as a portfolio project demonstrating applied chemical reaction engineering concepts.

---

## Reactors Modeled

| Reactor | Description | Design Equation |
|---------|-------------|-----------------|
| CSTR | Continuous Stirred Tank Reactor — perfectly mixed | V = v₀·X / [k·(1−X)] |
| PFR | Plug Flow Reactor — no axial mixing | V = (v₀/k)·ln[1/(1−X)] |

---

## Reaction Model

```
A  →  Products     (irreversible, first-order, liquid-phase)
Rate law:  −rA = k · CA
```

The rate constant is calculated from the **Arrhenius equation**:
```
k(T) = A · exp(−Ea / R·T)       T in Kelvin
```

---

## How to Run

**Requirements:** Python 3.10+, no external libraries needed.

```bash
git clone https://github.com/manalchem/reactor-sizing-calculator.git
cd reactor-sizing-calculator
python3 reactor_sizing.py
```

---

## Sample Output

```
  Enter feed conditions:
    Volumetric flow rate v₀  (L/s): 2.0
    Inlet concentration CA0  (mol/L): 1.5
    Target conversion X (0–0.99): 0.80

  Enter Arrhenius parameters:
    Pre-exponential factor A (1/s): 2.0e6
    Activation energy Ea (J/mol): 50000
    Operating temperature (°C): 100

  ══════════════════════════════════════════════════════
    Results
  ══════════════════════════════════════════════════════
  Rate constant k (Arrhenius)               0.3012  1/s

  ── CSTR ───────────────────────────────────────────
  Required volume                          13.2800  L
  Residence time τ                          6.6400  s

  ── PFR ────────────────────────────────────────────
  Required volume                           3.2189  L
  Residence time τ                          1.6095  s

  ── Comparison ─────────────────────────────────────
  CSTR / PFR volume ratio                   4.1253  —

  → PFR requires 4.13× LESS volume than CSTR
    for 80.0% conversion of this first-order reaction.
```

---

## Engineering Concepts Applied

**CSTR Design Equation** — the entire reactor operates at the exit (lowest) concentration, making it least efficient for positive-order reactions:
```
V = FA0 · X / (−rA_exit) = v₀ · X / [k · (1−X)]
```

**PFR Design Equation** — concentration varies along reactor length, integrated analytically for first-order kinetics:
```
V = FA0 · ∫(dX / −rA) = (v₀/k) · ln[1/(1−X)]
```

**Arrhenius Equation** — describes the exponential dependence of reaction rate on temperature:
```
k(T) = A · exp(−Ea/RT)
```

**Key insight**: For any positive-order reaction, a PFR always achieves the same conversion as a CSTR in a smaller volume. The CSTR/PFR volume ratio increases with conversion — at 99% conversion, a CSTR can require 100× more volume than a PFR.

---

## Project Background

Built as part of a chemical engineering portfolio. Demonstrates practical application of chemical reaction engineering concepts including reactor design equations, kinetic rate laws, and the Arrhenius equation. Reactor design is a junior-level topic — building this project early demonstrates initiative and curiosity beyond current coursework.

---

## Planned Additions

- [ ] Second-order reaction kinetics
- [ ] Series/parallel reactor configurations (CSTR + PFR combinations)
- [ ] Levenspiel plot generator (matplotlib)
- [ ] Non-isothermal reactor with energy balance coupling
- [ ] Multiple reactions with selectivity calculations

---

## Author

**Manal**
| Chemical Engineering Student | github.com/manalchem
