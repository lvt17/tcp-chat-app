import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.protocol import *

# test normal message
msg1 = chat("user1", "hello")
print("Test 1:", decode_message(encode_message(msg1)) == msg1)

# test unicode
msg2 = chat("user1", "xin chào")
print("Test 2:", decode_message(encode_message(msg2)) == msg2)

# test emoji
msg3 = chat("user1", "hello 😊")
print("Test 3:", decode_message(encode_message(msg3)) == msg3)

# test empty message
msg4 = chat("user1", "")
print("Test 4:", decode_message(encode_message(msg4)) == msg4)
