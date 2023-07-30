from dns.rdatatype import NULL

# TPR
def process_argument_xyTPR(argTPR):
    argTPRbinaire = None
    
    if argTPR == "atteint":
        argTPRbinaire = True
    elif argTPR == "nonAtteint":
        argTPRbinaire = False
    elif argTPR == "":
        argTPRbinaire = None
    else:
        argTPRbinaire = None
        return None

    return argTPRbinaire

# SL
def process_argument_xySL(argSL):
    argSLbinaire = None
    if argSL == "atteint":
        argSLbinaire = True
    elif argSL == "partiel":
        argSLbinaire = False
    elif argSL == "":
        argSLbinaire = None
    else:
        argSLbinaire = None
        return None

    return argSLbinaire

# BE
def process_argument_xyBE(argBE):
    argBEbinaire = None
    
    if argBE == "true":
        argBEbinaire = True
    elif argBE == "":
        argBEbinaire = None
    else:
        argBEbinaire = None
        return None

    return argBEbinaire

# sortie manuelle
def process_argument_xySortieManuelle(argSortManu):
    argSortManuBinaire = None
    
    if argSortManu == "true":
        argSortManuBinaire = True
    if argSortManu == "false":
        argSortManuBinaire = False
    elif argSortManu == "":
        argSortManuBinaire = None
    else:
        argSortManuBinaire = None
        return None

    return argSortManuBinaire

# tilt
def process_argument_xyTilt(argTilt):
    argTiltBinaire = None
    
    if argTilt == "true":
        argTiltBinaire = True
    if argTilt == "false":
        argTiltBinaire = False
    elif argTilt == "":
        argTiltBinaire = None
    else:
        argTiltBinaire = None
        return None

# viole strategie
def process_argument_xyVioleStrat(argVioleStrat):
    argVioleStratBinaire = None
    
    if argVioleStrat == "true":
        argVioleStratBinaire = True
    if argVioleStrat == "false":
        argVioleStratBinaire = False
    elif argVioleStrat == "":
        argVioleStratBinaire = None
    else:
        argVioleStratBinaire = None
        return None

    return argVioleStratBinaire

# annonce economique
def process_argument_xyAnnEco(argAnnEco):
    argAnnEcoBinaire = None
    
    if argAnnEco == "true":
        argAnnEcoBinaire = True
    if argAnnEco == "false":
        argAnnEcoBinaire = False
    elif argAnnEco == "":
        argAnnEcoBinaire = None
    else:
        argAnnEcoBinaire = None
        return None

    return argAnnEcoBinaire

