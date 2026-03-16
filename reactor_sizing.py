"""
=============================================================
 Ideal Reactor Sizing Calculator
 CSTR and PFR Volume for First-Order Liquid-Phase Reactions
=============================================================
 Author: Manal
 Description:
   Calculates the required reactor volume to achieve a target
   fractional conversion for an irreversible, first-order,
   liquid-phase reaction:

       A  →  Products       -rA = k·CA

   Two ideal reactor models are supported:
     1. CSTR (Continuous Stirred Tank Reactor)
        — perfectly mixed, uniform concentration throughout
     2. PFR  (Plug Flow Reactor)
        — no mixing in flow direction, concentration varies
          along reactor length

   The Arrhenius equation is used to calculate the rate
   constant k at the operating temperature:

       k(T) = A · exp(−Ea / RT)

 Key equations:
   CSTR:  V = FA0 · X / (−rA_exit)     design equation
   PFR:   V = FA0 · ∫(dX / −rA)        Levenspiel integral
          For first order: V = (v0/k) · ln(1/(1−X))

 Usage:
   python3 reactor_sizing.py
=============================================================
"""

import math


# ── Constants ─────────────────────────────────────────────────────────────────
R_GAS = 8.314   # J/mol·K — universal gas constant


# ── Utilities ──────────────────────────────────────────────────────────────────
def print_header(title: str) -> None:
    width = 56
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_result(label: str, value: float, unit: str) -> None:
    print(f"  {label:<38} {value:>10.4f}  {unit}")


def get_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """Prompt for a float with optional range validation."""
    while True:
        try:
            val = float(input(f"  {prompt}: "))
            if min_val is not None and val < min_val:
                print(f"  ⚠  Value must be ≥ {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"  ⚠  Value must be ≤ {max_val}.")
                continue
            return val
        except ValueError:
            print("  ⚠  Please enter a valid number.")


# ── Arrhenius Equation ─────────────────────────────────────────────────────────
def arrhenius(A_pre: float, Ea: float, T_C: float) -> float:
    """
    Calculate reaction rate constant using the Arrhenius equation.

        k(T) = A · exp(−Ea / R·T)

    The Arrhenius equation describes how reaction rate increases
    exponentially with temperature. It is one of the most fundamental
    equations in chemical kinetics.

    Parameters
    ----------
    A_pre : float — pre-exponential factor (1/s for first-order)
    Ea    : float — activation energy (J/mol)
    T_C   : float — temperature (°C)

    Returns
    -------
    float — rate constant k (1/s)
    """
    T_K = T_C + 273.15
    return A_pre * math.exp(-Ea / (R_GAS * T_K))


# ── CSTR Design Equation ───────────────────────────────────────────────────────
def cstr_volume(v0: float, CA0: float, k: float, X: float) -> float:
    """
    Calculate CSTR volume using the design equation.

    For a first-order liquid-phase reaction  A → Products:
        −rA = k · CA = k · CA0 · (1 − X)

    CSTR design equation:
        V = FA0 · X / (−rA_exit)
          = v0 · CA0 · X / (k · CA0 · (1−X))
          = (v0 · X) / (k · (1−X))

    In a CSTR the entire reactor operates at the EXIT concentration —
    the lowest concentration in the system. This makes it the least
    efficient reactor for positive-order reactions.

    Parameters
    ----------
    v0  : float — volumetric flow rate (L/s)
    CA0 : float — inlet concentration of A (mol/L)
    k   : float — rate constant (1/s)
    X   : float — target fractional conversion (0–1)

    Returns
    -------
    float — required CSTR volume (L)
    """
    rA_exit = k * CA0 * (1 - X)        # reaction rate at exit conditions
    FA0 = v0 * CA0                      # molar feed rate of A (mol/s)
    return FA0 * X / rA_exit


def pfr_volume(v0: float, CA0: float, k: float, X: float) -> float:
    """
    Calculate PFR volume using the integrated design equation.

    For a first-order liquid-phase reaction:
        V = (v0 / k) · ln(1 / (1−X))

    This result comes from integrating the PFR design equation:
        dF_A / dV = r_A
        → V = FA0 · ∫₀ˣ dX / (k · CA0 · (1−X))
        → V = (v0/k) · ln(1/(1−X))

    A PFR always requires less volume than a CSTR for the same
    conversion because it never forces the reaction to proceed
    at the low exit concentration.

    Parameters
    ----------
    v0  : float — volumetric flow rate (L/s)
    CA0 : float — inlet concentration of A (mol/L)
    k   : float — rate constant (1/s)
    X   : float — target fractional conversion (0–1)

    Returns
    -------
    float — required PFR volume (L)
    """
    return (v0 / k) * math.log(1 / (1 - X))


# ── Main Calculator ────────────────────────────────────────────────────────────
def run_calculator() -> None:
    """Collect inputs, compute reactor volumes, display comparison."""

    print_header("Reaction & Feed Conditions")

    print("""
  Reaction:  A  →  Products   (irreversible, first-order)
  Rate law:  −rA = k · CA
    """)

    # ── Feed conditions ────────────────────────────────────────────────────────
    v0  = get_float("Volumetric flow rate v₀  (L/s)",    min_val=0)
    CA0 = get_float("Inlet concentration CA0  (mol/L)",  min_val=0)
    X   = get_float("Target conversion X       (0–0.99)", min_val=0, max_val=0.99)

    # ── Kinetic parameters ─────────────────────────────────────────────────────
    print_header("Kinetic Parameters (Arrhenius)")
    print("  Enter Arrhenius parameters for the reaction.")
    print("  (If you only know k directly, enter A = k and Ea = 0)\n")

    A_pre = get_float("Pre-exponential factor A  (1/s)", min_val=0)
    Ea    = get_float("Activation energy Ea      (J/mol)", min_val=0)
    T_C   = get_float("Operating temperature     (°C)")

    # ── Calculate rate constant ────────────────────────────────────────────────
    k = arrhenius(A_pre, Ea, T_C)

    # ── Calculate reactor volumes ──────────────────────────────────────────────
    V_cstr = cstr_volume(v0, CA0, k, X)
    V_pfr  = pfr_volume(v0, CA0, k, X)

    # Derived quantities
    tau_cstr = V_cstr / v0              # residence time CSTR (s)
    tau_pfr  = V_pfr  / v0             # residence time PFR  (s)
    ratio    = V_cstr / V_pfr           # volume ratio

    # ── Results ────────────────────────────────────────────────────────────────
    print_header("Results")

    print(f"\n  Operating temperature:  {T_C} °C  ({T_C + 273.15:.2f} K)")
    print_result("Rate constant k (Arrhenius)", k, "1/s")

    print("\n  ── CSTR ───────────────────────────────────────────")
    print("  (Perfectly mixed — operates at exit concentration)")
    print_result("Required volume",    V_cstr,    "L")
    print_result("Residence time τ",   tau_cstr,  "s")

    print("\n  ── PFR ────────────────────────────────────────────")
    print("  (Plug flow — concentration varies along length)")
    print_result("Required volume",    V_pfr,     "L")
    print_result("Residence time τ",   tau_pfr,   "s")

    print("\n  ── Comparison ─────────────────────────────────────")
    print_result("CSTR / PFR volume ratio", ratio, "—")
    if ratio > 1:
        print(f"\n  → PFR requires {ratio:.2f}× LESS volume than CSTR")
        print(f"    for {X*100:.1f}% conversion of this first-order reaction.")
    else:
        print(f"\n  → Reactors are equivalent at this conversion.")

    print("\n  ── Design Equations Used ──────────────────────────")
    print("  Arrhenius:  k = A·exp(−Ea/RT)")
    print("  CSTR:       V = v₀·X / [k·(1−X)]")
    print("  PFR:        V = (v₀/k)·ln[1/(1−X)]")


# ── Main Menu ──────────────────────────────────────────────────────────────────
def main() -> None:
    banner = r"""
  ╔══════════════════════════════════════════════════╗
  ║      Ideal Reactor Sizing Calculator  v1.0      ║
  ║         CSTR and PFR for A → Products           ║
  ╚══════════════════════════════════════════════════╝
    """
    print(banner)

    while True:
        run_calculator()
        again = input("\n  Run another calculation? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
