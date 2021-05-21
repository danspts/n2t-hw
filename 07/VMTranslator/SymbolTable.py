__addresses = dict(
    local='LCL',
    argument='ARG',
    this='THIS',
    that='THAT',
    pointer=3,
    temp=5,
    static=16
)

unary = ['neg', 'not']

def get_address(symbol):
    return __addresses.get(symbol, 'constant')