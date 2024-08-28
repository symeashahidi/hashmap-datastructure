# Name: Syme Shahidi
# OSU Email: shahidis@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6- Hashmap Implementation
# Due Date: 12/7/2023
# Description: Created 11 functions: put, resize_table, table_load,
#              empty_buckets, get, contains_key, remove, get_keys_and_values,
#              clear, __iter__, and __next__ using Hashmaps and open addressing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This function adds a key, and it's value to a hashmap.
        """
        total_elements_in_table = self._size
        total_buckets = self._capacity
        load_factor = total_elements_in_table / total_buckets

        # If the load factor is greater or equal to 0.5,
        # resize the table with double the capacity
        if load_factor >= 0.5:
            self.resize_table(total_buckets * 2)

        # Calculate hash_value and index. If the index is filled,
        # use quadratic probing to move to the next index and check
        # until an empty index is reached
        hash_value = self._hash_function(key)
        first_index = hash_value % self._capacity
        index = hash_value % self._capacity
        increment_value = 1
        while self._buckets[index] is not None:
            # If the key at index is already in the array, break
            if self._buckets[index].key == key:
                break
            index = (first_index + (increment_value * increment_value)) % self._capacity
            increment_value += 1

        # If the array is empty, add a HashEntry with the key and value
        # and increment size
        if self._size == 0:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        # Otherwise, either update the value if the key is already in the
        # array or, if it isn't, add the new HashEntry with the key and value
        # and increment size
        else:
            if self._buckets[index] is not None:
                if self._buckets[index].key == key:
                    self._buckets[index].value = value
                    # If the tombstone at index is true, change it to False
                    # and increment size
                    if self._buckets[index].is_tombstone is True:
                        self._buckets[index].is_tombstone = False
                        self._size += 1
            else:
                self._buckets[index] = HashEntry(key, value)
                self._buckets[index].is_tombstone = False
                self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        This function resizes the hashmap by changing the capacity.
        """
        if new_capacity < self._size:
            return

        # If the new_capacity is not prime, update it to the next
        # prime number
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)

        # Save the old array from the created get keys and values method
        old_array = self.get_keys_and_values()

        # Reinitialize self._buckets to an empty dynamic array,
        # update capacity to new_capacity, and reset size
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        for index in range(self._capacity):
            self._buckets.append(None)

        # Fills the array with the keys and values
        for index in range(old_array.length()):
            # Unpack tuple
            old_array_tuple = old_array[index]
            old_array_key = old_array_tuple[0]
            old_array_value = old_array_tuple[1]

            # Uses the created put method to add the key and value
            self.put(old_array_key, old_array_value)

    def table_load(self) -> float:
        """
        This function returns the load_factor.
        """
        load_factor = self._size / self._capacity

        return load_factor

    def empty_buckets(self) -> int:
        """
        This function returns the amount of empty buckets.
        """
        empty_buckets_count = 0

        for index in range(self._buckets.length()):
            # If the is empty at the index, increment the empty bucket count
            if self._buckets[index] is None:
                empty_buckets_count += 1

        return empty_buckets_count

    def get(self, key: str) -> object:
        """
        This function returns the value of the inputted key if the key exists.
        Otherwise, it returns None.
        """
        # Calculate hash_value and index.
        hash_value = self._hash_function(key)
        first_index = hash_value % self._capacity
        index = hash_value % self._capacity
        increment_value = 1

        while self._buckets[index] is not None:
            # If the key at index matches the inputted key and tombstone is
            # False, return the value at index
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                return self._buckets[index].value

            # Otherwise, use quadratic probing and continue the while loop
            index = (first_index + (increment_value * increment_value)) % self._capacity
            increment_value += 1

        # If the index is empty or tombstone is True, return None
        if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
            return None

        return self._buckets[index].value

    def contains_key(self, key: str) -> bool:
        """
        This function returns True if the inputted key is found. Otherwise,
        it returns False.
        """
        # Calculate hash_value and index.
        hash_value = self._hash_function(key)
        first_index = hash_value % self._capacity
        index = hash_value % self._capacity
        increment_value = 1

        while self._buckets[index] is not None:
            # If the key at index matches the inputted key and tombstone is False,
            # return True
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                return True

            # Otherwise, use quadratic probing and continue the while loop
            index = (first_index + (increment_value * increment_value)) % self._capacity
            increment_value += 1

        if self._buckets[index] is not None:
            # If tombstone is True, return false
            if self._buckets[index].is_tombstone is True:
                return False
            # If the key at index matches the inputted key, return True
            if self._buckets[index].key == key:
                return True

        # If the key was not found, return False
        return False

    def remove(self, key: str) -> None:
        """
        This function removes the key from the hashmap.
        """
        # Calculate hash_value and index.
        hash_value = self._hash_function(key)
        first_index = hash_value % self._capacity
        index = hash_value % self._capacity
        increment_value = 1

        while self._buckets[index] is not None:
            # If the key at index matches the inputted key and tombstone is
            # False, update tombstone to True, decrement size, and return
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return

            # Otherwise, use quadratic probing and continue the while loop
            index = (first_index + (increment_value * increment_value)) % self._capacity
            increment_value += 1

        if self._buckets[index] is not None:
            if self._buckets[index].key == key:
                # Updates tombstone to True and decrements size
                self._buckets[index].is_tombstone = True
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This function returns an array with a tuple containing a key and value pair
        at each index.
        """
        new_array = DynamicArray()

        for index in range(self._capacity):
            # This conditional skips the empty indices
            if self._buckets[index] is not None:
                if self._buckets[index].is_tombstone is False:
                    # Creates tuple and adds it to the new array
                    key_value_tuple = (self._buckets[index].key, self._buckets[index].value)
                    new_array.append(key_value_tuple)

        return new_array

    def clear(self) -> None:
        """
        This function clears the hashmap.
        """
        self._buckets = DynamicArray()
        self._size = 0

        # Fills self._buckets with Nones until the capacity is reached
        for index in range(self._capacity):
            self._buckets.append(None)

    def __iter__(self):
        """
        This function creates a variable for the iterator for the loop.
        """
        self.current_index = 0
        return self

    def __next__(self):
        """
        This function increments the iterator and returns the next element.
        """
        try:
            # While the element at the current index is None or the element is a tombstone,
            # increment current index
            while self._buckets[self.current_index] is None or self._buckets[self.current_index].is_tombstone == True:
                self.current_index += 1
            # Save the value of the element at the current index
            next_value = self._buckets[self.current_index]
        except DynamicArrayException:
            raise StopIteration

        self.current_index += 1
        return next_value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
