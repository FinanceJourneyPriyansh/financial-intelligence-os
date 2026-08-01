"""
Financial Intelligence OS
World Bank Indicators

Commonly used World Bank indicator codes.
"""


class WorldBankIndicators:
    """
    World Bank indicator catalog.
    """

    # =========================
    # Economy
    # =========================

    GDP = "NY.GDP.MKTP.CD"
    GDP_GROWTH = "NY.GDP.MKTP.KD.ZG"
    GDP_PER_CAPITA = "NY.GDP.PCAP.CD"

    # =========================
    # Population
    # =========================

    POPULATION = "SP.POP.TOTL"
    POPULATION_GROWTH = "SP.POP.GROW"

    # =========================
    # Inflation
    # =========================

    INFLATION = "FP.CPI.TOTL.ZG"

    # =========================
    # Employment
    # =========================

    UNEMPLOYMENT = "SL.UEM.TOTL.ZS"

    # =========================
    # Trade
    # =========================

    EXPORTS = "NE.EXP.GNFS.CD"
    IMPORTS = "NE.IMP.GNFS.CD"

    # =========================
    # Government
    # =========================

    GOVERNMENT_DEBT = "GC.DOD.TOTL.GD.ZS"

    # =========================
    # Education
    # =========================

    SCHOOL_ENROLLMENT = "SE.PRM.ENRR"

    # =========================
    # Health
    # =========================

    LIFE_EXPECTANCY = "SP.DYN.LE00.IN"

    # =========================
    # Energy
    # =========================

    ELECTRICITY_ACCESS = "EG.ELC.ACCS.ZS"

    # =========================
    # Environment
    # =========================

    CO2_EMISSIONS = "EN.ATM.CO2E.PC"