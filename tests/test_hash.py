import pytest 
from app.hash import crc32_hash 

@pytest.mark.parametrize(
        "plaintext", 
        ["thank", "you", "for", "reading", "my", "source", "code", ":)"]
)
def test_hash_prefix(plaintext : str): 
    """Hash function properly strips hex prefix."""
    hash_str = crc32_hash(plaintext)
    assert hash_str[:2] != "0x"


@pytest.mark.parametrize(
        "plaintext", 
        ["thank", "you", "for", "reading", "my", "source", "code", ":)"]
)
def test_hash_prefix(plaintext : str): 
    """Hash function properly strips hex prefix."""
    hash_str = crc32_hash(plaintext)
    assert hash_str[:2] != "0x"




