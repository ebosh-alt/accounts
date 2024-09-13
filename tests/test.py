# Encoding a message in UTF-8
message = "Hello, World!"
message_encoded = message.encode('utf-8')
print("Encoded in UTF-8:", message_encoded)


import base64

base64_encoded = base64.b64encode(message_encoded)
# print("Encoded in Base64:", base64_encoded.decode())
print("Decoded in Base64:", base64.b64decode(s=base64_encoded.decode()))
