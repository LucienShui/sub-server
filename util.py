import base64


def get_sub_link(html: str, sid: str) -> str:
    line: str = next(filter(lambda x: f'id="{sid}"' in x, html.split("\n")))
    url: str = line.split("'")[1]
    return url


def padding(encoded: str) -> str:
    missing_padding = len(encoded) % 4
    if missing_padding:
        encoded += "=" * (4 - missing_padding)
    return encoded


def encode(decoded: str) -> str:
    encoded: str = base64.urlsafe_b64encode(decoded.encode("utf-8")).decode("utf-8").rstrip("=")
    return encoded


def decode(encoded: str) -> str:
    decoded: str = base64.urlsafe_b64decode(padding(encoded.strip())).decode("utf-8")
    return decoded
