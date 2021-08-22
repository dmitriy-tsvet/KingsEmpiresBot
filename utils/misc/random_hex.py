import re
import os
import binascii


async def get_random_hex(length):
    result = binascii.b2a_hex(
        os.urandom(length)
    )

    result = re.findall(r"\w'(\w+)'", str(result))[0]
    return result[:length]
