from functools import reduce 

def w3toconll_token(token):
    """
    transform a single token from w3 to conll
    e.g. 
    """
    spl = token.split('|')
    if len(spl) < 3:
        return ''
    if len(spl[2]) > 1 and spl[2][1] == '-':
        spl[2] = spl[2][2:]
    spl[1], spl[2] = spl[2], spl[1]
    
    return '\t'.join(spl)


def w3toconll(infile, outfile):
    """
    transform corpus fron w3 format (in infile) to conll and put in into outfile 
    """
    with open(infile) as f:
        corpus = f.readlines()
        
    tokens = []
    for i in map(lambda sent: sent.strip('\n').split(' '), corpus):
        tokens+=i
    
    tokens = list(filter(lambda x: x != '', map(w3toconll_token, tokens)))
    
    with open(outfile, 'w') as f:
        for token in tokens:
            print(token, file=f)