import zlib 

def crc32_hash(plain_text : str) -> str:
    """Convert plaintext to CRC32 hash.
    
    Args: 
        plain_text: Plain-text string.

    Returns: 
        CRC32 hash of plain-text.
    """
    return str(hex(zlib.crc32(plain_text.encode())))


