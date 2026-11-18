import zlib 

def crc32_hash(plain_text : str) -> str:
    """Convert plaintext to CRC32 hash.
    
    Args: 
        plain_text: Plain-text string.

    Returns: 
        CRC32 hash of plain-text.
    """
    # is input a string?
    if not isinstance(plain_text, str): 
        raise TypeError("crc32_hash expects string input.")
    # output hash of original URL
    return str(hex(zlib.crc32(plain_text.encode())))[2:]




