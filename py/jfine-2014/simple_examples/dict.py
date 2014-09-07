
# The empty dictionary.
d = dict()
len(d) == 0
d['key'] ** KeyError

# Storing and retrieving a value.
d = dict()
d['key'] = 'value'
d['key'] == 'value'

# Removing a key-value pair.
d = dict(key='value')
len(d) == 1
del d['key']
len(d) == 0

d = {}
d['key'] = 'value'
('key' in d) is True
('key' in (d is True)) ** TypeError
# TODO: This is really odd.
('key' in d is True) is False
bool('key' in d is True) is False
bool('key' in d) is True

# dict.get always succeeds.
d = dict(key='value')
d.get('key') == 'value'
d.get('non-key') is None
d.get('non-key', 'default') is 'default'

d = dict(key='value')
d.setdefault('key') == 'value'
d.setdefault('key2') == None
len(d) == 2
d.setdefault('key3', 'value3') == 'value3'


