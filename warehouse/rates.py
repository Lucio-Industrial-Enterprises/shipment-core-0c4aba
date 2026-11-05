"""Shipping rate calculations."""

_ZONE_BASE = {"local": 5.0, "regional": 8.0}
_SERVICE_SURCHARGE = {"standard": 0.0, "express": 7.0}


def shipping_quote(weight_kg: float, zone: str, service: str = "standard") -> float:
    """Return a shipping quote in dollars.

    Parameters
    ----------
    weight_kg:
        Parcel weight; must be positive.
    zone:
        Delivery zone – ``"local"`` or ``"regional"``.
    service:
        Shipping service – ``"standard"`` (default) or ``"express"``.
        Express adds a $7.00 surcharge on top of the standard rate.

    Returns
    -------
    float
        Quoted price rounded to two decimal places.

    Raises
    ------
    ValueError
        If *weight_kg* is not positive, *zone* is unknown, or *service* is
        unknown.
    """
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    if zone not in _ZONE_BASE:
        raise ValueError(f"unknown zone: {zone!r}")
    if service not in _SERVICE_SURCHARGE:
        raise ValueError(f"unknown service: {service!r}")
    base = _ZONE_BASE[zone]
    surcharge = _SERVICE_SURCHARGE[service]
    return round(base + 1.5 * weight_kg + surcharge, 2)
