from typing import Text
import random
import string

def UniqueID(size: int) -> Text:
    characters: Text = string.ascii_letters + string.digits
    id_: Text = ''.join(random.choice(characters) for _ in range(size))
    return id_