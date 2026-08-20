from __future__ import annotations

from datetime import timezone
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from platform_core.data.gold_public_product_service import (
    GoldPublicProductService,
)

app = FastAPI(
    title="Gold Intelligence",
    description="Public Gold Intelligence product powered by FIOS.",
)

app.mount(
    "/static",
    StaticFiles(
        directory="07_public_products/gold_intelligence/static"
    ),
    name="static",
)

product_service = GoldPublicProductService()

IST = ZoneInfo("Asia/Kolkata")


def format_ist(timestamp) -> str:
    if timestamp is None:
        return "?"

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp.astimezone(IST).strftime(
        "%d %b %Y at %I:%M:%S %p IST"
    )


def format_ist_short(timestamp) -> str:
    if timestamp is None:
        return "?"

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp.astimezone(IST).strftime(
        "%d %b %Y at %I:%M %p IST"
    )


def format_money(value: float | None) -> str:
    if value is None:
        return "?"

    return f"&#8377;{value:,.0f}"


@app.get("/", response_class=HTMLResponse)
def home() -> str:

    product = product_service.generate()

    change = (
        f"{product.change_pct:+.2f}%"
        if product.change_pct is not None
        else "?"
    )

    # Source-backed Indian gold rates.
    # These are not derived from the global USD/oz quote.
    price_24k = product.india_24k_10g

    price_22k = product.india_22k_10g

    price_18k = product.india_18k_10g

    # ------------------------------------------------------------
    # FIOS INVENTORY EXPOSURE
    # Reuses the live India 24K reference rate.
    # Measures exposure; does not forecast price.
    # ------------------------------------------------------------

    inventory_exposure_card = (
        '<div class="action-card">'
        '<div class="action-kicker">'
        'INVENTORY EXPOSURE CALCULATOR'
        '</div>'
        '<h3>Measure your gold price exposure</h3>'
        '<div class="action-form">'
        '<label>'
        'Gold held (grams)'
        '<input '
        'id="inventory-weight" '
        'type="number" '
        'min="0" '
        'step="0.01" '
        'value="500">'
        '</label>'
        '<button '
        'type="button" '
        'onclick="calculateInventoryExposure()">'
        'Calculate exposure'
        '</button>'
        '</div>'
        '<div '
        'id="inventory-result" '
        'class="action-result">'
        'Enter your gold holding to estimate current value '
        'and scenario exposure.'
        '</div>'
        '<small>'
        'Uses the current FIOS 24K India reference rate. '
        'Scenario figures show exposure to price movement, '
        'not a prediction of future gold prices.'
        '</small>'
        '</div>'
    )

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # FIOS INDIA PREMIUM / DISCOUNT
    # Compares the global gold + FX implied India value
    # against the published India 24K reference rate.
    # This is a market transmission diagnostic, not a forecast.
    # ------------------------------------------------------------

    global_implied_india_24k = (
        product.price
        * product.usd_inr
        * 10.0
        / 31.1034768
        if product.price is not None
        and product.usd_inr is not None
        else None
    )

    india_reference_premium = (
        product.india_24k_10g - global_implied_india_24k
        if global_implied_india_24k is not None
        and product.india_24k_10g is not None
        else None
    )

    india_reference_premium_pct = (
        india_reference_premium
        / global_implied_india_24k
        * 100.0
        if global_implied_india_24k
        else None
    )

    india_premium_card = (
        '<div class="action-card">'
        '<div class="action-kicker">'
        'INDIA PREMIUM / DISCOUNT'
        '</div>'
        '<h3>Global-to-India transmission</h3>'
        '<div class="action-result">'
        '<div class="inventory-result-grid">'

        '<div>'
        '<small>GLOBAL IMPLIED INDIA VALUE</small>'
        '<strong>'
        + (
            "&#8377;" + f"{global_implied_india_24k:,.0f}"
            if global_implied_india_24k is not None
            else "Unavailable"
        )
        + '</strong>'
        '<small>24K / 10g</small>'
        '</div>'

        '<div>'
        '<small>PUBLISHED INDIA REFERENCE</small>'
        '<strong>'
        + (
            "&#8377;" + f"{product.india_24k_10g:,.0f}"
            if product.india_24k_10g is not None
            else "Unavailable"
        )
        + '</strong>'
        '<small>24K / 10g</small>'
        '</div>'

        '<div>'
        '<small>PREMIUM / DISCOUNT</small>'
        '<strong>'
        + (
            (
                "+" if india_reference_premium >= 0 else ""
            )
            + f"&#8377;{india_reference_premium:,.0f}"
            + (
                f" ({india_reference_premium_pct:+.2f}%)"
                if india_reference_premium_pct is not None
                else ""
            )
            if india_reference_premium is not None
            else "Unavailable"
        )
        + '</strong>'
        '</div>'

        '</div>'
        '</div>'

        '<small>'
        'The premium or discount is the difference between the '
        'published Indian 24K reference and the value implied by '
        'global gold and USD/INR. It is a transmission diagnostic, '
        'not a prediction or dealer quote.'
        '</small>'

        '</div>'
    )

    # ------------------------------------------------------------
    # FIOS DECISION SCORECARD
    # Uses existing FIOS signals only.
    # No new forecasting model is introduced here.
    # ------------------------------------------------------------

    base_scenarios = [
        item
        for item in product.scenarios
        if item.scenario == "BASE"
    ]

    base_directions = [
        str(item.direction).upper()
        for item in base_scenarios
    ]

    transmission = str(
        product.india_transmission
    ).upper()

    bullish_base_count = sum(
        "BULLISH" in direction
        for direction in base_directions
    )

    bearish_base_count = sum(
        "BEARISH" in direction
        for direction in base_directions
    )

    supportive_transmission = (
        "UPSIDE" in transmission
        or "SUPPORT" in transmission
        or "FAVORABLE" in transmission
        or "FAVOURABLE" in transmission
    )

    adverse_transmission = (
        "DOWNSIDE" in transmission
        or "PRESSURE" in transmission
        or "BEARISH" in transmission
        or "NEGATIVE" in transmission
    )

    if (
        supportive_transmission
        and bullish_base_count > bearish_base_count
    ):
        decision_label = "FAVOURABLE"
        decision_class = "favourable"
        decision_reason = (
            "Existing FIOS signals show supportive India "
            "transmission and a bullish base-case bias."
        )

    elif (
        adverse_transmission
        or bearish_base_count > bullish_base_count
    ):
        decision_label = "CAUTION"
        decision_class = "caution"
        decision_reason = (
            "Existing FIOS signals show downside or bearish "
            "pressure in the current transmission/base-case view."
        )

    else:
        decision_label = "NEUTRAL"
        decision_class = "neutral"
        decision_reason = (
            "Existing FIOS signals do not establish a sufficiently "
            "clear directional advantage."
        )

    decision_confidence = str(
        product.overall_confidence
    ).upper()

    decision_scorecard = (
        '<div class="decision-scorecard '
        + decision_class
        + '">'
        '<div class="decision-score-top">'
        '<div>'
        '<span class="action-kicker">FIOS DECISION SCORECARD</span>'
        '<h3>'
        + decision_label
        + '</h3>'
        '</div>'
        '<div class="decision-confidence">'
        '<small>CONFIDENCE</small>'
        '<strong>'
        + decision_confidence
        + '</strong>'
        '</div>'
        '</div>'
        '<p>'
        + decision_reason
        + '</p>'
        '<div class="decision-signals">'
        '<div>'
        '<small>INDIA TRANSMISSION</small>'
        '<strong>'
        + transmission.replace("_", " ")
        + '</strong>'
        '</div>'
        '<div>'
        '<small>BASE-CASE SIGNALS</small>'
        '<strong>'
        + str(bullish_base_count)
        + ' bullish / '
        + str(bearish_base_count)
        + ' bearish'
        + '</strong>'
        '</div>'
        '</div>'
        '<small>'
        'Decision is derived from existing FIOS intelligence signals '
        'and is not personalized investment advice.'
        '</small>'
        '</div>'
    )

    # FIOS B3 ACTION BRIDGE
    # Converts the existing decision scorecard into an operational
    # posture using existing FIOS signals only.
    # No new forecasting model is introduced.
    # ------------------------------------------------------------

    if decision_label == "FAVOURABLE":
        action_posture = "MAINTAIN / PROCEED WITH DISCIPLINE"
        action_reason = (
            "Bullish base-case signals currently outweigh bearish "
            "signals, while India transmission remains supportive."
        )
    elif decision_label == "CAUTION":
        action_posture = "PROTECT / REDUCE NEW EXPOSURE"
        action_reason = (
            "Existing FIOS signals show downside pressure or a "
            "bearish balance. Protect existing exposure and avoid "
            "unnecessary new commitments."
        )
    else:
        action_posture = "WAIT / GATHER MORE EVIDENCE"
        action_reason = (
            "Existing FIOS signals do not establish a sufficiently "
            "clear directional advantage for an aggressive action."
        )

    base_invalidations = []
    for item in base_scenarios:
        for invalidation in item.invalidation:
            if invalidation not in base_invalidations:
                base_invalidations.append(invalidation)

    watch_items = "".join(
        f"<li>{item}</li>"
        for item in base_invalidations[:4]
    )

    action_bridge = (
        '<div class="action-bridge">'
        '<div class="action-bridge-top">'
        '<div>'
        '<span class="action-kicker">ACTION POSTURE</span>'
        '<h3>'
        + action_posture
        + '</h3>'
        '</div>'
        '<div class="decision-confidence">'
        '<small>CONFIDENCE</small>'
        '<strong>'
        + decision_confidence
        + '</strong>'
        '</div>'
        '</div>'
        '<p>'
        + action_reason
        + '</p>'
        '<div class="action-bridge-section">'
        '<small>WHY</small>'
        '<p>'
        + decision_reason
        + '</p>'
        '</div>'
        '<div class="action-bridge-section">'
        '<small>WATCH / INVALIDATION</small>'
        '<ul>'
        + (
            watch_items
            if watch_items
            else "<li>No current BASE invalidation signals available.</li>"
        )
        + '</ul>'
        '</div>'
        '<small>'
        'Operational posture is derived from existing FIOS '
        'intelligence signals and is not personalized investment advice.'
        '</small>'
        '</div>'
    )


    drivers = "".join(
        f"""
        <div class="driver">
            <div>
                <span class="driver-name">{item.driver}</span>
                <small>{item.evidence_count} evidence items</small>
            </div>
            <strong>{item.confidence}</strong>
        </div>
        """
        for item in product.driver_assessments
    )

    horizons = "".join(
        f"""
        <div class="horizon">
            <small>{item.horizon}</small>
            <strong>{item.confidence}</strong>
            <span>{item.direction}</span>
        </div>
        """
        for item in product.scenarios
        if item.scenario == "BASE"
    )

    evidence = "".join(
        f"""
        <article class="evidence">
            <div class="evidence-top">
                <span class="source">{item.source}</span>
                <span class="evidence-query">{item.query}</span>
            </div>

            <a
                class="evidence-title"
                href="{item.url}"
                target="_blank"
                rel="noopener noreferrer"
            >
                {item.title}
            </a>

            <div class="evidence-times">
                <span>
                    Published
                    <strong>{format_ist_short(item.published_at)}</strong>
                </span>

                <span>
                    Retrieved
                    <strong>{format_ist_short(item.retrieved_at)}</strong>
                </span>
            </div>
        </article>
        """
        for item in product.evidence[:10]
    )

    return f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta
            name="viewport"
            content="width=device-width,initial-scale=1"
        >

        <meta
            http-equiv="refresh"
            content="60"
        >

        <title>Gold Intelligence &middot; FIOS</title>

        <link
            rel="stylesheet"
            href="/static/gold.css"
        >
    
<style>
.purpose-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    margin: 28px 0;
}}

.purpose-card,
.bottom-line {{
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 18px;
    padding: 24px;
    background: rgba(255,255,255,.025);
}}

.purpose-card h2,
.bottom-line h2 {{
    margin: 6px 0 16px;
}}

.purpose-card ul {{
    margin: 0;
    padding-left: 20px;
}}

.purpose-card li {{
    margin: 9px 0;
    line-height: 1.55;
}}

.section-kicker {{
    font-size: .72rem;
    letter-spacing: .14em;
    font-weight: 700;
    opacity: .65;
}}

.answer-card {{
    margin: 18px 0 28px;
}}

.answer-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}}

.answer-grid p,
.bottom-line p {{
    line-height: 1.6;
    opacity: .78;
}}

.bottom-line {{
    margin: 30px 0;
}}

.bottom-line-detail {{
    border-top: 1px solid rgba(255,255,255,.10);
    padding-top: 16px;
}}

@media (max-width: 800px) {{{{
    .purpose-grid,
    .answer-grid {{{{
        grid-template-columns: 1fr;
    }}}}
}}}}

.action-layer {{
    margin: 30px 0;
}}

.action-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
}}

.action-card,
.decision-card {{
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 14px;
    padding: 22px;
    background: rgba(255,255,255,.025);
}}

.action-kicker {{
    font-size: .72rem;
    letter-spacing: .12em;
    opacity: .65;
    margin-bottom: 8px;
}}

.action-card h3 {{
    margin: 0 0 18px;
}}

.action-form {{
    display: grid;
    gap: 12px;
}}

.action-form label {{
    display: grid;
    gap: 6px;
    font-size: .82rem;
}}

.action-form input {{
    width: 100%;
    box-sizing: border-box;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(0,0,0,.20);
    color: inherit;
}}

.action-form button {{
    margin-top: 4px;
    padding: 11px 14px;
    border: 0;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
}}

.action-result {{
    margin-top: 16px;
    padding: 14px;
    border-radius: 9px;
    background: rgba(255,255,255,.05);
    line-height: 1.7;
}}

.action-card small,
    .action-bridge {{
        margin-top: 18px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
    }}

    .action-bridge-top {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: flex-start;
    }}

    .action-bridge h3 {{
        margin: 6px 0 0;
    }}

    .action-bridge-section {{
        margin-top: 14px;
    }}

    .action-bridge-section > small {{
        display: block;
        margin-bottom: 6px;
        font-weight: 700;
    }}

    .action-bridge-section p {{
        margin: 0;
    }}

    .action-bridge ul {{
        margin: 6px 0 0;
        padding-left: 20px;
    }}

    .action-bridge li {{
        margin: 4px 0;
    }}

.decision-card small {{
    display: block;
    margin-top: 14px;
    opacity: .62;
    line-height: 1.5;
}}

.decision-card {{
    line-height: 1.7;
}}

/* ============================================================
   FIOS GOLD ACTION LAYER ? REFERENCE UI
   ============================================================ */

.action-form {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px 18px;
}}

.action-form label {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
}}

.action-form input,
.action-form select {{
    width: 100%;
    min-height: 42px;
    box-sizing: border-box;
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 8px;
    background: rgba(255,255,255,.025);
    color: #f5f7fa;
    padding: 10px 12px;
    font: inherit;
    outline: none;
    appearance: none;
    -webkit-appearance: none;
}}

.action-form select {{
    cursor: pointer;
    padding-right: 36px;
    background-image:
        linear-gradient(45deg, transparent 50%, rgba(255,255,255,.75) 50%),
        linear-gradient(135deg, rgba(255,255,255,.75) 50%, transparent 50%);
    background-position:
        calc(100% - 16px) 18px,
        calc(100% - 11px) 18px;
    background-size:
        5px 5px,
        5px 5px;
    background-repeat: no-repeat;
}}

.action-form select option {{
    background: #111316;
    color: #f5f7fa;
}}

.action-form input:focus,
.action-form select:focus {{
    border-color: rgba(0,210,255,.55);
    box-shadow: 0 0 0 2px rgba(0,210,255,.08);
}}

.action-form label:nth-child(5),
.action-form button {{
    grid-column: 1 / -1;
}}

.action-form button {{
    min-height: 44px;
    margin-top: 2px;
}}

.action-result {{
    margin-top: 16px;
    padding: 16px;
    border-radius: 10px;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.06);
    line-height: 1.65;
}}

.action-result strong {{
    font-size: 1.02rem;
}}

.action-card small {{
    display: block;
    margin-top: 14px;
    opacity: .62;
    line-height: 1.5;
}}

@media (max-width: 800px) {{
    .action-grid {{
        grid-template-columns: 1fr;
    }}
}}

</style>

</head>

    <body>

        <main>

            <header>

                <div>
                    <span class="eyebrow">
                        FIOS PUBLIC INTELLIGENCE
                    </span>

                    <h1>Gold Intelligence</h1>

                    <p>
                        Global gold &rarr; India transmission
                    </p>
                </div>

                <div class="live-panel">

                    <span class="live">
                        <i></i> SYSTEM LIVE
                    </span>

                    <div
                        id="live-clock"
                        class="live-clock"
                    >
                        Loading live clock...
                    </div>

                    <small>
                        Browser clock &middot; Asia/Kolkata
                    </small>

                </div>

            </header>


            <section class="freshness">

                <div>
                    <span class="eyebrow">
                        DATA STATUS
                    </span>

                    <strong>
                        LIVE FIOS PRODUCT
                    </strong>
                </div>

                <div class="freshness-meta">

                    <span>
                        Intelligence retrieved
                        <strong>
                            {format_ist(product.retrieved_at)}
                        </strong>
                    </span>

                    <span>
                        Market quote timestamp
                        <strong>
                            {format_ist(product.quote_timestamp)}
                        </strong>
                    </span>

                </div>

            </section>


    
        <section class="purpose-grid">

            <div class="purpose-card">
                <div class="section-kicker">WHO IT'S FOR</div>
                <h2>Built for people who need to understand gold.</h2>
                <ul>
                    <li><strong>Gold investors</strong> &mdash; understand what is moving gold and the current risk picture.</li>
                    <li><strong>Indian savers & households</strong> &mdash; see source-backed 24K, 22K and 18K reference rates.</li>
                    <li><strong>Jewellers & gold businesses</strong> &mdash; monitor gold, currency and demand signals.</li>
                    <li><strong>Importers & traders</strong> &mdash; understand global-price and USD/INR transmission.</li>
                    <li><strong>Analysts & researchers</strong> &mdash; combine market movement, news evidence and scenarios.</li>
                    <li><strong>Businesses exposed to gold</strong> &mdash; understand potential cost, inventory and pricing pressure.</li>
                </ul>
            </div>

            <div class="purpose-card">
                <div class="section-kicker">WHO IT'S NOT FOR</div>
                <h2>Know what this product does not promise.</h2>
                <ul>
                    <li>Guaranteed future gold prices.</li>
                    <li>Personalized investment recommendations.</li>
                    <li>Exact jewellery-shop selling prices.</li>
                    <li>Exchange-grade tick-by-tick market data.</li>
                    <li>A simple price-only gold-rate lookup.</li>
                </ul>
            </div>

        </section>

        <section class="purpose-card answer-card">
            <div class="section-kicker">WHAT FIOS ANSWERS</div>
            <h2>From price to understanding.</h2>

            <div class="answer-grid">
                <div>
                    <strong>01 - What is happening?</strong>
                    <p>Gold movement, Indian rates, market timestamps and data freshness.</p>
                </div>
                <div>
                    <strong>02 - Why is it happening?</strong>
                    <p>Evidence-backed assessment of the strongest observed drivers.</p>
                </div>
                <div>
                    <strong>03 - What does it mean for India?</strong>
                    <p>Global gold movement combined with USD/INR transmission.</p>
                </div>
                <div>
                    <strong>04 - What should I watch next?</strong>
                    <p>Scenario direction, confidence, assumptions and invalidation signals.</p>
                </div>
            </div>
        </section>

        <section class="hero">

                <div class="hero-price">

                    <span class="eyebrow">
                        <span class="gold-mark">Au</span>
                        GOLD &middot; 24K
                    </span>

                    <div class="price gold-market-price">
                        ${product.price:,.2f}
                        <small>/ troy oz</small>
                    </div>

                    <div class="change">
                        {change}
                        <span>daily move</span>
                    </div>

                </div>

                <div class="hero-india">

                    <span class="eyebrow">
                        INDIA VALUE
                    </span>

                    <div class="rupee-price">
                        {format_money(price_24k)}
                    </div>

                    <div class="unit">
                        per 10g &middot; 24K
                    </div>

                </div>

                <div class="signal">

                    <span>CONFIDENCE</span>

                    <strong>
                        {product.overall_confidence}
                    </strong>

                </div>

            </section>


            <section class="quote-details">

                <div class="section-title">
                    MARKET QUOTE
                </div>

                <div class="quote-grid">

                    <div>
                        <small>INSTRUMENT</small>
                        <strong>{product.instrument}</strong>
                    </div>

                    <div>
                        <small>SOURCE</small>
                        <strong>{product.source}</strong>
                    </div>

                    <div>
                        <small>USD / INR</small>
                        <strong>
                            {
                                f"{product.usd_inr:,.4f}"
                                if product.usd_inr is not None
                                else "?"
                            }
                        </strong>
                    </div>

                    <div>
                        <small>QUOTE TIME</small>
                        <strong>
                            {format_ist_short(product.quote_timestamp)}
                        </strong>
                    </div>

                </div>

                <p class="freshness-note">
                    System clock is live. Market freshness reflects
                    the timestamp supplied by the acquisition source;
                    this product does not claim tick-level streaming
                    data unless the source provides it.
                </p>

            </section>


            <section class="carats">

                <div class="section-title">
                    INDIA GOLD VALUE BY CARAT
                </div>

                <div class="carat-grid">

                    <div class="carat featured">
                        <small>24K</small>
                        <strong>{format_money(price_24k)}</strong>
                        <span>per 10g</span>
                    </div>

                    <div class="carat">
                        <small>22K</small>
                        <strong>{format_money(price_22k)}</strong>
                        <span>per 10g</span>
                    </div>

                    <div class="carat">
                        <small>18K</small>
                        <strong>{format_money(price_18k)}</strong>
                        <span>per 10g</span>
                    </div>

                </div>

                <div class="india-rate-source">
                    Source:
                    {product.india_rate_source}
                    &middot; retrieved
                    {format_ist(product.india_rate_timestamp)}
                </div>

                <p class="calculation-note">
                    India gold rates are sourced from
                    GoodReturns and shown by carat for 10g.
                    These are published Indian reference rates and
                    may differ from a dealer quote, taxes, premiums,
                    making charges, or local market spreads.
                </p>

            </section>


            <section>

                <div class="section-title">
                    WHY IT MOVED
                </div>

                <div class="drivers">
                    {drivers}
                </div>

            </section>


            <section class="india">

                <div>

                    <div class="section-title">
                        INDIA TRANSMISSION
                    </div>

                    <h2>
                        {
                            product.india_transmission
                            .replace("_", " ")
                        }
                    </h2>

                </div>

                <div class="horizons">
                    {horizons}
                </div>

            </section>


            <section>

                <div class="section-title">
                    INTELLIGENCE BRIEF
                </div>

                <p class="summary">
                    {product.summary}
                </p>

            </section>

            <section class="action-layer">

                <div class="section-title">
                    ACTION LAYER
                </div>

                <div class="action-grid">

                    <div class="action-card">
                        <div class="action-kicker">
                            JEWELLERY INVOICE ESTIMATOR
                        </div>

                        <h3>Estimate your final jewellery bill</h3>

                        <div class="action-form">

                            <label>
                                Karat
                                <select
                                    id="jewellery-karat"
                                    onchange="syncPurityToKarat('jewellery-karat', 'jewellery-purity')"
                                >
                                    <option value="24" selected>24K</option>
                                    <option value="22">22K</option>
                                    <option value="21">21K</option>
                                    <option value="18">18K</option>
                                </select>
                            </label>

                            <label>
                                Purity
                                <select id="jewellery-purity">
                                    <option value="99.9" selected>99.9%</option>
                                    <option value="95">95%</option>
                                    <option value="92">92%</option>
                                    <option value="91.6">91.6%</option>
                                    <option value="90">90%</option>
                                    <option value="87.5">87.5%</option>
                                    <option value="75">75%</option>
                                </select>
                            </label>

                            <label>
                                Weight (grams)
                                <input
                                    id="jewellery-weight"
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value="10"
                                >
                            </label>

                            <label>
                                Making charge (%)
                                <input
                                    id="making-charge"
                                    type="number"
                                    min="0"
                                    step="0.1"
                                    value="10"
                                >
                            </label>

                            <label>
                                Hallmark fee (INR)
                                <input
                                    id="hallmark-fee"
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value="53.10"
                                    autocomplete="off"
                                >
                            </label>

                            <button
                                type="button"
                                onclick="calculateJewellery()"
                            >
                                Calculate estimate
                            </button>

                        </div>

                        <div
                            id="jewellery-result"
                            class="action-result"
                        >
                            Enter your inputs to estimate
                            the invoice.
                        </div>

                        <small>
                            Uses the current FIOS live gold reference
                            (24K / 10g). Actual shop invoices
                            may differ.
                        </small>
                    </div>


                    <div class="action-card">

                        <div class="action-kicker">
                            GOLD SCENARIO SIMULATOR
                        </div>

                        <h3>Test a global gold scenario</h3>

                        <div class="action-form">

                            <label>
                                Karat
                                <select
                                    id="scenario-karat"
                                    onchange="syncPurityToKarat('scenario-karat', 'scenario-purity')"
                                >
                                    <option value="24" selected>24K</option>
                                    <option value="22">22K</option>
                                    <option value="21">21K</option>
                                    <option value="18">18K</option>
                                </select>
                            </label>

                            <label>
                                Purity
                                <select id="scenario-purity">
                                    <option value="99.9" selected>99.9%</option>
                                    <option value="95">95%</option>
                                    <option value="92">92%</option>
                                    <option value="91.6">91.6%</option>
                                    <option value="90">90%</option>
                                    <option value="87.5">87.5%</option>
                                    <option value="75">75%</option>
                                </select>
                            </label>

                            <label>
                                Gold (USD / troy oz)
                                <input
                                    id="scenario-gold"
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value="{product.price:,.2f}"
                                >
                            </label>

                            <label>
                                USD / INR
                                <input
                                    id="scenario-fx"
                                    type="number"
                                    min="0"
                                    step="0.001"
                                    value="{product.usd_inr:,.4f}"
                                >
                            </label>

                            <button
                                type="button"
                                onclick="calculateScenario()"
                            >
                                Run scenario
                            </button>

                        </div>

                        <div
                            id="scenario-result"
                            class="action-result"
                        >
                            Test different gold and FX assumptions.
                        </div>

                        <small>
                            The result is a theoretical conversion,
                            not a dealer quote.
                        </small>

                    </div>

                </div>

            </section>


            <section class="action-layer">

                <div class="action-grid">

                    {inventory_exposure_card}

                    {india_premium_card}

                </div>

                <div class="section-title">
                    WHAT SHOULD I DO NOW?
                </div>

                <div class="decision-card">

                    {decision_scorecard}

                    {action_bridge}

                    <p>
                        Use the scenario simulator and invoice
                        estimator to test your own exposure before
                        making a purchase or inventory decision.
                    </p>

                    <small>
                        FIOS provides evidence-based market context,
                        not personalized investment advice.
                    </small>

                </div>

            </section>



            <section>

                <div class="section-title">
                    LATEST EVIDENCE
                </div>

                <div class="evidence-list">
                    {evidence}
                </div>

            </section>


            <footer>

                <div>
                    FIOS GOLD INTELLIGENCE
                </div>

                <span>
                    Product refresh: 60 seconds
                </span>

            </footer>

        </main>


        <script>

        function updateLiveClock() {{

            const now = new Date();

            const parts = new Intl.DateTimeFormat(
                "en-IN",
                {{
                    timeZone: "Asia/Kolkata",
                    weekday: "short",
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                    hour12: true
                }}
            ).formatToParts(now);

            const values = {{}};

            parts.forEach(part => {{
                values[part.type] = part.value;
            }});

            const clock =
                `${{values.weekday}} ${{values.day}} ` +
                `${{values.month}} ${{values.year}} at ` +
                `${{values.hour}}:${{values.minute}}:` +
                `${{values.second}} ${{values.dayPeriod}} IST`;

            document.getElementById(
                "live-clock"
            ).textContent = clock;
        }}

        updateLiveClock();

        setInterval(
            updateLiveClock,
            1000
        );

        

        function getStandardPurity(karat) {{

            const standardPurities = {{
                "24": 99.9,
                "22": 91.6,
                "21": 87.5,
                "18": 75
            }};

            return standardPurities[karat] || 99.9;
        }}


        function syncPurityToKarat(
            karatId,
            purityId
        ) {{

            const karat =
                document.getElementById(
                    karatId
                ).value;

            const puritySelect =
                document.getElementById(
                    purityId
                );

            const standardPurity =
                getStandardPurity(karat);

            const standardValue =
                standardPurity.toString();

            const matchingOption =
                Array.from(
                    puritySelect.options
                ).find(
                    option =>
                        option.value === standardValue
                );

            if (matchingOption) {{
                puritySelect.value =
                    standardValue;
            }}
        }}


        function resolvePurity(
            karatId,
            purityId
        ) {{

            const karat =
                document.getElementById(
                    karatId
                ).value;

            const purityValue =
                document.getElementById(
                    purityId
                ).value;

            if (purityValue === "standard") {{
                return getStandardPurity(karat);
            }}

            return Number(purityValue);
        }}




        syncPurityToKarat(
            "jewellery-karat",
            "jewellery-purity"
        );

        syncPurityToKarat(
            "scenario-karat",
            "scenario-purity"
        );


        function calculateJewellery() {{

            const weight =
                Number(
                    document.getElementById(
                        "jewellery-weight"
                    ).value
                );

            const making =
                Number(
                    document.getElementById(
                        "making-charge"
                    ).value
                );

            const hallmark =
                Number(
                    document.getElementById(
                        "hallmark-fee"
                    ).value
                );

            const rate24k =
                Number(
                    "{price_24k}"
                );

            const karat =
                document.getElementById(
                    "jewellery-karat"
                ).value;

            const purity =
                resolvePurity(
                    "jewellery-karat",
                    "jewellery-purity"
                );

            if (
                !Number.isFinite(weight) ||
                weight <= 0
            ) {{
                document.getElementById(
                    "jewellery-result"
                ).textContent =
                    "Enter a valid weight.";

                return;
            }}

            if (
                !Number.isFinite(making) ||
                making < 0
            ) {{
                document.getElementById(
                    "jewellery-result"
                ).textContent =
                    "Enter a valid making charge.";

                return;
            }}

            if (
                !Number.isFinite(hallmark) ||
                hallmark < 0
            ) {{
                document.getElementById(
                    "jewellery-result"
                ).textContent =
                    "Enter a valid hallmark fee.";

                return;
            }}

            const goldValue =
                weight *
                rate24k *
                purity /
                100 /
                10;

            const makingCharge =
                goldValue *
                making /
                100;

            const subtotal =
                goldValue +
                makingCharge +
                hallmark;

            const gst =
                subtotal *
                3 /
                100;

            const total =
                subtotal +
                gst;

            document.getElementById(
                "jewellery-result"
            ).innerHTML =
                "<strong>Estimated invoice: INR " +
                total.toLocaleString(
                    "en-IN",
                    {{
                        maximumFractionDigits: 0
                    }}
                ) +
                "</strong><br>" +
                "Selected: " +
                karat +
                "K - " +
                purity.toFixed(1) +
                "% purity<br>" +
                "Gold: INR " +
                goldValue.toLocaleString(
                    "en-IN",
                    {{
                        maximumFractionDigits: 0
                    }}
                ) +
                "<br>Making: INR " +
                makingCharge.toLocaleString(
                    "en-IN",
                    {{
                        maximumFractionDigits: 0
                    }}
                ) +
                "<br>GST: INR " +
                gst.toLocaleString(
                    "en-IN",
                    {{
                        maximumFractionDigits: 0
                    }}
                );
        }}



        function calculateInventoryExposure() {{

            const weight =
                Number(
                    document.getElementById(
                        "inventory-weight"
                    ).value
                );

            const rate24k =
                Number(
                    "{price_24k}"
                );

            const result =
                document.getElementById(
                    "inventory-result"
                );

            if (
                !Number.isFinite(weight) ||
                weight <= 0 ||
                !Number.isFinite(rate24k) ||
                rate24k <= 0
            ) {{
                result.innerHTML =
                    "Enter a valid gold holding.";
                return;
            }}

            const currentValue =
                (weight / 10) * rate24k;

            const downsideImpact =
                currentValue * -0.03;

            const upsideImpact =
                currentValue * 0.03;

            const money = value =>
                "&#8377;" +
                Math.round(
                    value
                ).toLocaleString("en-IN");

            result.innerHTML = `
                <div class="inventory-result-grid">

                    <div>
                        <small>CURRENT VALUE</small>
                        <strong>${{money(currentValue)}}</strong>
                    </div>

                    <div>
                        <small>IF GOLD FALLS 3%</small>
                        <strong>${{money(downsideImpact)}}</strong>
                    </div>

                    <div>
                        <small>IF GOLD RISES 3%</small>
                        <strong>+${{money(upsideImpact)}}</strong>
                    </div>

                </div>

                <p>
                    Exposure is proportional to your gold holding.
                    A 3% gold move changes the estimated holding
                    value by approximately 3%.
                </p>
            `;
        }}

        function calculateScenario() {{

            const gold =
                Number(
                    document.getElementById(
                        "scenario-gold"
                    ).value
                );

            const fx =
                Number(
                    document.getElementById(
                        "scenario-fx"
                    ).value
                );

            const karat =
                document.getElementById(
                    "scenario-karat"
                ).value;

            const purity =
                resolvePurity(
                    "scenario-karat",
                    "scenario-purity"
                );

            if (
                !Number.isFinite(gold) ||
                !Number.isFinite(fx) ||
                gold <= 0 ||
                fx <= 0
            ) {{
                document.getElementById(
                    "scenario-result"
                ).textContent =
                    "Enter valid gold and FX values.";

                return;
            }}

            const implied24k =
                gold *
                fx *
                10 /
                31.1034768;

            const impliedSelected =
                implied24k *
                purity /
                100;

            document.getElementById(
                "scenario-result"
            ).innerHTML =
                "<strong>Theoretical " +
                karat +
                "K / 10g: INR " +
                impliedSelected.toLocaleString(
                    "en-IN",
                    {{
                        maximumFractionDigits: 0
                    }}
                ) +
                "</strong><br>" +
                "Purity: " +
                purity.toFixed(1) +
                "%<br>" +
                "24K reference: INR " +
                implied24k.toLocaleString(
                    "en-IN",
                    {{
                        maximumFractionDigits: 0
                    }}
                ) +
                " / 10g<br>" +
                "Published India 24K reference: INR " +
                "{product.india_24k_10g}" +
                " / 10g<br>" +
                "Transmission difference: INR " +
                "{india_reference_premium}" +
                " (" +
                "{india_reference_premium_pct:.2f}%" +
                ")<br>" +
                "Gold: $" +
                gold.toLocaleString(
                    "en-US",
                    {{
                        maximumFractionDigits: 2
                    }}
                ) +
                " / troy oz<br>" +
                "USD/INR: " +
                fx.toFixed(3);
        }}



        </script>

    
        <section class="bottom-line">
            <div class="section-kicker">BOTTOM LINE</div>
            <h2>What FIOS thinks right now</h2>
            <p>
                {product.summary}
            </p>
            <p class="bottom-line-detail">
                India's currency transmission is currently
                <strong>{product.india_transmission.replace("_", " ")}</strong>.
                The most important risks to the current view are a stronger
                dollar, less-supportive rate expectations, or a reversal in
                gold momentum.
            </p>
        </section>

</body>
    </html>
    """


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "product": "gold-intelligence",
    }
