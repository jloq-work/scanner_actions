from typing import List

#############################################
#Centraliser la liste des actions SRD
#Fournir une API simple pour le scanner
#Être facilement maintenable (ajout / retrait de valeurs)
##############################################


# ============================================================
# SRD SYMBOL LIST (Yahoo Finance format)
# ============================================================

SRD_SYMBOLS: List[str] = [
    # valeurs SRD elligibles (exemples)
    "VTR.PA" , #Vitura
    "ETL.PA" , #Eutelsat
    "ADOC.PA" , #Adocia
    "AL2SI.PA" , #2CRSI
    "MEDCL.PA" , #Medincell
# CAC 40 / grandes capitalisations (exemples)
    "AIR.PA",    # Airbus
    "AI.PA",     # Air Liquide
    "BNP.PA",    # BNP Paribas
    "CAP.PA",    # Capgemini
    "CS.PA",     # AXA
    "DG.PA",     # Vinci
    "DSY.PA",    # Dassault Systèmes
    "ENGI.PA",   # Engie
    "KER.PA",    # Kering
    "MC.PA",     # LVMH
    "OR.PA",     # L'Oréal
    "RI.PA",     # Pernod Ricard
    "SAF.PA",    # Safran
    "SAN.PA",    # Sanofi
    "SGO.PA",    # Saint-Gobain
    "SU.PA",     # Schneider Electric
    "TTE.PA",    # TotalEnergies
    "VIV.PA",    # Vivendi

]


# ============================================================
# PUBLIC API
# ============================================================

def get_srd_symbols() -> List[str]:
    """
    Return the list of SRD symbols.

    Returns
    -------
    List[str]
        Yahoo Finance symbols for SRD stocks
    """
    return SRD_SYMBOLS.copy()
