from dns.rdatatype import NULL

def process_argument_xy(argTPR, argSL, argBE):
    argTPRbinaire = None
    argSLbinaire = None
    argBEbinaire = None
    
    if argTPR == "atteint":
        argTPRbinaire = True
    elif argTPR == "nonAtteint":
        argTPRbinaire = False
    elif argTPR == "":
        argTPRbinaire = None
    elif argSL == "atteint":
        argSLbinaire = True
    elif argSL == "partiel":
        argSLbinaire = False
    elif argSL == "":
        argSLbinaire = None
    elif argBE == "true":
        argBEbinaire = True
    elif argBE == "":
        argBEbinaire = None
    else:
        argTPRbinaire = None
        argSLbinaire = None
        argBEbinaire = None
        return None  # Ou lever une exception appropriée selon le cas

    return argTPRbinaire, argSLbinaire, argBEbinaire
