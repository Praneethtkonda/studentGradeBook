COEFFICIENT = 53
'''
    Utility method to compute the hash code for strings
    hash(s)=s[0]+s[1]⋅p+s[2]⋅p^2+...+s[n−1]⋅p ^ n−1 mod m= ∑i=0n−1s[i]⋅pimodm,
    sum([ord(c) for c in key])
'''
def hashCode(key):
    return sum(ord(v) * (COEFFICIENT ** i) for i, v in enumerate(key))

class HashTable:
    ''' HashTable with open addressing with linear probing'''
    _AVAIL = object()
    def __init__(self, capacity=11, p=109345121):
        self._table = capacity * [None] # Initializing the list
        self._capacity = len(self._table) # Initially 11
        self._prime = p
        self._scale = 109345119 # 1 + randrange(p-1)
        self._shift = 109345101 # randrange(p)
        self._n = 0 # Number of entries
    
    # private
    def _hash_function(self, key):
        # (hash(k)* 109345119 + 109345101) % 109345121 % 11
        # [(ai+b) mod p] mod N MAD method for compression map
        return (hashCode(key) * self._scale + self._shift) % self._prime % self._capacity
    
    # def _hash1(self, bucket_index):
    #     return bucket_index % len(self._table) 
    # def _hash2(self, PRIME, bucket_index):
    #     return PRIME - bucket_index % PRIME

    def _resize(self, updated_capacity):
        older_entries = list(self._table)
        self._table = updated_capacity * [None]
        self._n = 0 # Computed 
        for entry in older_entries:
            if entry != None:
                key = entry[0]
                value = entry[1]
                self[key] =  value

    def _is_available(self, bucket_index):
        """Return True if bucket_item is available in table."""
        #return self._table[bucket_index] is None or isinstance(self._table[bucket_index], list)
        return self._table[bucket_index] is None or self._table[bucket_index] is HashTable._AVAIL
    
    def _find_bucket_index(self, bucket_index, key):
        firstAvail = None
        while True:
            if(self._is_available(bucket_index)):
                if firstAvail is None:
                    firstAvail = bucket_index
                if self._table[bucket_index] is None:
                    return (False, firstAvail)
            elif key == self._table[bucket_index][0]:
                return (True, bucket_index)
            bucket_index = (bucket_index + 1) % len(self._table)

    def _set_bucket_item(self, bucket_index, key, value):
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            self._table[latest_bucket_index] = [key, value]
            self._n += 1
        # Just updating the value
        self._table[latest_bucket_index][1] = value
    
    def _get_bucket_item(self, bucket_index, key):
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            raise KeyError('KeyError: Key not found '+ key)
        bucket_item = self._table[latest_bucket_index]
        return bucket_item[1] # value
    
    def _delete_bucket_item(self, bucket_index, key):
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            raise KeyError('KeyError: Key not found '+ key)
        self._table[bucket_index] = HashTable._AVAIL
        self._n -= 1

    # public
    def set(self, key, value):
        # TODO: Validation of the input
        # [None, [key, value], [key2, value2], None] => Bucket array
        bucket_index = self._hash_function(key)

        self._set_bucket_item(bucket_index, key, value)

        if self._n > len(self._table) // 2: # Floor division with 2 => To keep load factor below 0.5
            self._resize(2 * len(self._table) - 1)
    
    def get(self, key):
        bucket_index = self._hash_function(key)
        # print("Got the key: ", key)
        return self._get_bucket_item(bucket_index, key)

    def keys(self):
        return list(map(lambda entry: (entry[0]), filter(lambda entry: (entry != None and entry != HashTable._AVAIL), self._table)))
    
    def values(self):
        return list(map(lambda entry: (entry[1]), filter(lambda entry: (entry != None and entry != HashTable._AVAIL) , self._table)))

    def prune(self):
        ''' Function to reset the hash table '''
        self._table = self._capacity * [None]
        return 0
    
    def delete(self, key):
        bucket_index = self._hash_function(key)
        self._delete_bucket_item(bucket_index, key)

    def has(self, key):
        bucket_index = self._hash_function(key)
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            return False
        return True

    # Dunder methods
    def __len__(self):
        return self._n

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)
    
    def __delitem__(self, key):
        return self.delete(key)


# --------- USAGE -----------
# h = HashTable()
# h.set('Praneeth', 23)
# h.set('Prateek', 19)
# h.set('Prateek2', 20)
# h.set('Prateek3', 21)
# h.set('Prateek4', 22)
# h.set('Prateek5', 24)
# h.set('Prateek6', 25)
# h.set('Prateek7', 26)
# h.set('Prateek8', 27)
# h.set('Prateek9', 29)
# h.set('Prateek10', 30)
# h.set('Prateek11', 31)
# h.set('Prateek12', 31)
# h.set('Prateek13', 31)
# h.keys()

# # h.prune()
# # h.keys()

# print(h['Praneeth'])
# print(h.get('Prateek8'))
# print(h['Prateek7'])
# print(h['Prateek11'])
# # print(h._AVAIL)
# print(len(h))

# h.set('2010CSE1223', 3.5)
# h.set('2010CSE1224', 3.9)
# h.set('2010CSE1225', 4.5)
# h.set('2010CSE1226', 3.5)
# h.set('2010CSE1227', 4.8)
# h.set('2010CSE1228', 4.1)
# h.set('2010CSE1229', 4.2)
# h.set('2010CSE1230', 4.9)
# h.set('2010CSE1231', 5.0)

# print("Is  key present:", h.has('2010CSE1231'))
# print("Is  key present:", h.has('a'))
# print(h.keys())
# print(h.get('2010CSE1230'))
# print("The number of keys inserted are: ", len(h))