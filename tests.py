import base64


def padding(s):
    missing_padding = len(s) % 4
    if missing_padding:
        s += '=' * (4 - missing_padding)
    return s


def decode(text: str) -> str:
    decoded = base64.urlsafe_b64decode(padding(text.strip())).decode("utf-8")
    return decoded


def test_client():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/api/v1/subscription", params={"token": "test"})
    assert response.status_code
    text = response.text
    decoded = decode(text)
    print(decoded)


def test_sub_link():
    from util import get_sub_link
    with open("index.html") as f:
        html: str = f.read()
    url: str = get_sub_link(html, "SSSIP002_4")
    print(url)


def test_encode_decode():
    from util import encode, decode
    text: str = "Hello World!"
    encoded: str = encode(text)
    decoded: str = decode(encoded)
    assert text == decoded
