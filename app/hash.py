import zlib 
import os

class UknownStrategyError(Exception):
    """Raised when URL_STRATEGY is not a supported URL conversion method."""
    pass 

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base_conversion(base_ten: int) -> str:
    """Encode a non-negative integer as a base-62 string.
    
    Args: 
        base_ten: A record's primary key in base 10. 
    Returns: 
        Base 62 encoding of primary key.
    
    """
    if base_ten == 0:
        return ALPHABET[0]
    chars = []
    n = base_ten
    while n:
        n, rem = divmod(n, 62)
        chars.append(ALPHABET[rem])
    return "".join(reversed(chars))
    
def hash_url(plain_text : str) -> str:
    """Convert plaintext to CRC32 hash.
    
    Args: 
        plain_text: Plain-text string.

    Returns: 
        CRC32 hash of plain-text.
    """
    return str(hex(zlib.crc32(plain_text.encode())))[2:] 


