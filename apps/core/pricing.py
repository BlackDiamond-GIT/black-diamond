"""Multi-currency price helpers (CZK base, EUR/USD display)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CurrencySettings:
    eur_rate: Decimal = Decimal('22.09')
    usd_rate: Decimal = Decimal('20.00')
    show_eur: bool = True
    show_usd: bool = True


@dataclass(frozen=True)
class PriceDisplay:
    czk: int
    eur: int | None = None
    usd: int | None = None


def _to_int(amount_czk: int | float | Decimal | str) -> int:
    return int(Decimal(str(amount_czk)).quantize(Decimal('1')))


def czk_to_eur(amount_czk: int, rate: Decimal) -> int:
    if rate <= 0:
        return 0
    return round(_to_int(amount_czk) / float(rate))


def czk_to_usd(amount_czk: int, rate: Decimal) -> int:
    if rate <= 0:
        return 0
    return round(_to_int(amount_czk) / float(rate))


def build_price_display(amount_czk: int | float | Decimal, settings: CurrencySettings) -> PriceDisplay:
    czk = _to_int(amount_czk)
    eur = czk_to_eur(czk, settings.eur_rate) if settings.show_eur else None
    usd = czk_to_usd(czk, settings.usd_rate) if settings.show_usd else None
    return PriceDisplay(czk=czk, eur=eur, usd=usd)


def format_price_plain(amount_czk: int | float | Decimal, settings: CurrencySettings) -> str:
    display = build_price_display(amount_czk, settings)
    parts = [f'{display.czk} Kč']
    if display.eur is not None:
        parts.append(f'€{display.eur}')
    if display.usd is not None:
        parts.append(f'${display.usd}')
    return ' · '.join(parts)
