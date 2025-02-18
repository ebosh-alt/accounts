import base64


def encode(text: str):
    encoded_message = base64.b64encode(text.encode('utf-8'))
    return encoded_message.decode()


def decode(text: str):
    decoded_message = base64.b64decode(text)
    return decoded_message.decode()
