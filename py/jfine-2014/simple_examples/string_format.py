sf = str.format
sf('aaa')         == 'aaa'
sf('{0}')         ** IndexError
sf('{0}', 'abc')  == 'abc'
sf('{{')          == '{'
sf('}}') == '}'
sf('{') ** ValueError
sf('{00}', 'abc') == 'abc'
sf('{0a}', 'abc') ** KeyError
sf('{aa}', aa=3) == '3'


sf('{0}', 'abc')  \
    == 'abc'


'{0}'.format('abc')  \
    == 'abc'

'{0}'.format()  \
    ** IndexError

'{0}'.format(1, 2)  \
    == '1'

'{0}'.format(1, a=52)  \
    == '1'

# After much faffing, this is probably best.
'{0}'.format(1) == '1'
