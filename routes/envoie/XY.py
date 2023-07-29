from dns.rdatatype import NULL

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
