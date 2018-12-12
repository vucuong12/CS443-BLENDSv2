def sign(sk, msg):
    '''
    sign String msg with corresponding secret key (RsaKey object) in pycryptodome library
    return hex value for signature
    '''
    pass


def verify(pk, msg, sig):
    '''
    check sign is made for msg using public key PK, string MSG, 
    and byte string SIGN.
    suppose publicExponent is fixed at 0x10001.
    return boolean
    '''
    pass


def load_secret_key(fname):
    '''
    load json information of secret key from fname. 
    This returns RSA key object.
    '''
    sk = None
    return sk


def create_secret_key(fname):
    '''
    Create a secret key: [hint] RSA.generate().
    Save the secret key in json to a file named "fname". 
    This returns RSA key object.
    '''
    sk = None
    return sk


def get_hash(msg):
    pass


def get_pk(sk):
    '''
    return pk using modulus of given RsaKey object sk.
    '''
    pk = None
    return pk
