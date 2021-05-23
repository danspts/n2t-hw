__addresses = dict(
    SP = 0,
    local='LCL',
    argument='ARG',
    this='THIS',
    that='THAT',
    pointer=3,
    temp=5,
    static=16,
    frame = 14
)

__addresses['return'] = 13

unary = ['neg', 'not']

def get_address(symbol):
    return __addresses.get(symbol, symbol)