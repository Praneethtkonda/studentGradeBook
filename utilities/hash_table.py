COEFFICIENT = 53

def hashCode(key):
    """Utility method to compute the hash code for strings used to find index in compression map.
       hash(s)=s[0] + s[1]⋅a + s[2]⋅a^2 + ... + s[n−1]⋅a^n−1 mod m
       It takes weights for each character based on position and multiplies with ascii code of that character"""
    return sum(ord(v) * (COEFFICIENT ** i) for i, v in enumerate(key))

class MyHashTable:
    """ MyHashTable with open addressing with linear probing 
        Implementation Details:-
          1.) It uses a hash code which maps into a compression map.
          2.) Then it uses MAD method to map that index into the bucket array.
          3.) Works for keys as strings as we had implemented for that use case.
          4.) Values can be anything.
          5.) Bucket array is a list of format [None, [key, value], [key2, value2], None] with
              each key, value pair as a list.
          6.) For collision handling we have used linear probing.
    """
    _AVAIL = object()
    def __init__(self, capacity=11, p=109345121):
        """ Initializes the hash table with initial size of 11 or capacity and sets some properities """
        self._table = capacity * [None] # Initializing the list
        self._capacity = len(self._table) # Initially 11
        self._prime = p
        self._scale = 109345119 # 1 + randrange(p-1)
        self._shift = 109345101 # randrange(p)
        self._n = 0 # Number of entries
    
    # Note:- This is the method HashId() naming it as _hash_function for better usability and understanding
    def _hash_function(self, key):
        """ Private utility method which is a hash function gives the table index based on the calculated compression map index
           (hash(k)* 109345119 + 109345101) % 109345121 % 11
           [(ai+b) mod p] mod N MAD method to map from compression map to our bucket array """
        return (hashCode(key) * self._scale + self._shift) % self._prime % self._capacity
    
    # def _hash1(self, bucket_index):
    #     return bucket_index % len(self._table) 
    # def _hash2(self, PRIME, bucket_index):
    #     return PRIME - bucket_index % PRIME

    def _resize(self, updated_capacity):
        """ Private utility method which is used for resizing the bucket array. We use this to maintain the optimum load factor """
        older_entries = list(self._table)
        self._table = updated_capacity * [None]
        self._n = 0 # Computed 
        for entry in older_entries:
            if entry != None:
                key = entry[0]
                value = entry[1]
                self[key] =  value

    def _is_available(self, bucket_index):
        """ Return True if bucket_item is available in table """
        #return self._table[bucket_index] is None or isinstance(self._table[bucket_index], list)
        return self._table[bucket_index] is None or self._table[bucket_index] is MyHashTable._AVAIL
    
    def _find_bucket_index(self, bucket_index, key):
        """ Private utility method used for probing an ideal available slot.
           Strategy:- Linear probing
           It checks whether the index that we get for the key is available if not it probs into next.
           It goes till it finds an available slot
           Returns a tuple which has found, bucket_index
        """
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
        """ Private method which sets the value for a particular key in the bucket array """
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            self._table[latest_bucket_index] = [key, value]
            self._n += 1
        # Just update the value if key is already there in the bucket array
        self._table[latest_bucket_index][1] = value
    
    def _get_bucket_item(self, bucket_index, key):
        """ Private method which gets the value for a particular key in the bucket array """
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            raise KeyError('KeyError: Key not found '+ key)
        bucket_item = self._table[latest_bucket_index]
        return bucket_item[1] # value
    
    def _delete_bucket_item(self, bucket_index, key):
        """ Private method which deletes the value for a particular key in the bucket array """
        found, latest_bucket_index = self._find_bucket_index(bucket_index, key)
        if not found:
            raise KeyError('KeyError: Key not found '+ key)
        self._table[bucket_index] = MyHashTable._AVAIL
        self._n -= 1

    # public methods i.e API's exposed
    def set(self, key, value):
        """ Sets a value for a particular key in the hash table """
        # [None, [key, value], [key2, value2], None] => Bucket array
        bucket_index = self._hash_function(key)

        self._set_bucket_item(bucket_index, key, value)

        if self._n > len(self._table) // 2: # Note:- Floor division with 2 => To keep load factor below 0.5
            # Note:- Commenting this for log severity if records are more. Evaluators can un-comment if needed.
            # print("MyHashTable: Capacity has reached the threshold so resizing the capacity")
            self._resize(2 * len(self._table) - 1)
    
    def get(self, key):
        """ Gets a value for a particular key in the hash table """
        bucket_index = self._hash_function(key)
        # print("Got the key: ", key)
        return self._get_bucket_item(bucket_index, key)

    def keys(self):
        """ Returns a list of keys that are present in the hash table """
        return list(map(lambda entry: (entry[0]), filter(lambda entry: (entry != None and entry != MyHashTable._AVAIL), self._table)))
    
    def values(self):
        """ Returns a list of values corresponding to the keys that are present in the hash table """
        return list(map(lambda entry: (entry[1]), filter(lambda entry: (entry != None and entry != MyHashTable._AVAIL) , self._table)))

    def prune(self):
        """ Function to reset the hash table """
        self._table = self._capacity * [None]
        return 0
    
    def delete(self, key):
        """ Deletes an entry from the hash table based on the key """
        bucket_index = self._hash_function(key)
        self._delete_bucket_item(bucket_index, key)

    def has(self, key):
        """ Method to check whether a key is present in the hash table """
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
# h = MyHashTable()
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