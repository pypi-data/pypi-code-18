# pylint: disable=C0103

from . import parser
from . import message

my_message = message.Message()
my_message.set_header({'message':'hello world'})
my_message.set_body(b'1234567890')
print(my_message.encode())

# standard message
my_parser = parser.Parser()
parsed = my_parser.parse(my_message.encode())
print(parsed.header)
print(parsed.body)
print('----')

# standard message + remaining
my_parser = parser.Parser()
parsed = my_parser.parse(my_message.encode() + b'112233445566')
print(parsed.header)
print(parsed.body)
print(my_parser.remaining)
print('----')

# message in 2 pieces
my_parser = parser.Parser()
binary_string = my_message.encode()
parsed = my_parser.parse(binary_string[:10])
print(parsed)
parsed = my_parser.parse(binary_string[10:])
print(parsed.header)
print(parsed.body)
print('----')

# 2 standard messages
message1 = message.Message()
message1.set_header({'message':'hello world 1'})
message1.set_body(b'1111')
message2 = message.Message()
message2.set_header({'message':'hello world 2'})
message2.set_body(b'2222')

my_parser = parser.Parser()
parsed = my_parser.parse(message1.encode() + message2.encode())
print(parsed.header)
print(parsed.body)
print(my_parser.remaining)
parsed = my_parser.parse(b'')
print(parsed.header)
print(parsed.body)
print(my_parser.remaining)
print('----')
