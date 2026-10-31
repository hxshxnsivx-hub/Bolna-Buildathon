"""Electricity bill anomaly analysis — the 'brain math' for billing-dispute grievances.

Given units used + amount charged (and optionally the caller's normal/expected amount), compute
the over-charge and flag a legitimate anomaly. The slab rates are ILLUSTRATIVE / approximate
(for demo anomaly-detection only) — replace with the official TNPDCL domestic tariff for production.
"""

# (upper_unit_boundary, rate_per_unit) — progressive domestic slabs, approximate. 0-100 subsidised.
_SLABS = [(100, 0.0), (200, 2.35), (400, 4.70), (500, 6.30), (10 ** 9, 8.05)]

ANOMALY_FACTOR = 1.5    # charged >= 1.5x expected => flag as a legitimate over-charge


def _f(x, default=0.0) -> float:
    """Safe float: 'abc' / 'around 500' / None -> default (never raises)."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def estimate_bill(units) -> float:
    """Rough expected amount for `units` on the approximate TN domestic slabs."""
    units = max(_f(units), 0.0)
    total, prev = 0.0, 0
    for upper, rate in _SLABS:
        if units <= prev:
            break
        total += (min(units, upper) - prev) * rate
        prev = upper
    return round(total, 2)


def analyze(units, amount_charged, expected=None) -> dict:
    """Return the billing breakdown + anomaly flag. `expected` overrides the slab estimate.
    All inputs are parsed safely so a non-numeric caller/LLM value can never crash a live call."""
    units = _f(units)
    charged = _f(amount_charged)
    given = expected not in (None, "", 0, "0", 0.0)
    exp = _f(expected) if given else estimate_bill(units)
    if exp <= 0:                      # bad/zero 'expected' -> fall back to the slab estimate
        exp = estimate_bill(units)
    over = round(charged - exp, 2)
    pct = round(100 * over / exp, 1) if exp > 0 else 0.0
    anomaly = bool(charged > 0 and exp > 0 and charged >= exp * ANOMALY_FACTOR)
    return {"units_used": units, "amount_charged": charged,
            "expected_amount": round(exp, 2), "amount_over": over,
            "pct_over": pct, "anomaly": anomaly, "expected_estimated": not given}
