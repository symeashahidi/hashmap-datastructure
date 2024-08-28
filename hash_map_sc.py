# Name: Syme Shahidi
# OSU Email: shahidis@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6- Hashmap Implementation
# Due Date: 12/7/2023
# Description: Created 10 functions: put, resize_table, table_load,
#              empty_buckets, get, contains_key, remove, get_keys_and_values,
#              clear, and find_mode using Hashmaps and chaining.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        load_factor = total_elements_in_table/total_buckets

        # If the load factor is greater or equal to 1,
        # resize the table with double the capacity
        if load_factor >= 1.0:
            self.resize_table(total_buckets * 2)

        # Calculate hash_value and index and then find the
        # correct linked_list
        hash_value = self._hash_function(key)
        index = hash_value % self._buckets.length()
        linked_list = self._buckets[index]

        # If there are no nodes, add the key and value to the linked list
        # and update size
        if linked_list.length() == 0:
            linked_list.insert(key, value)
            self._size += 1
        else:
            for node in linked_list:
                # If the key is found, update the value
                if node.key == key:
                    node.value = value
                    break
                # If the key is not found, add the key and value
                # and update size
                if node.next is None:
                    linked_list.insert(key, value)
                    self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        This function resizes the hashmap by changing the capacity.
        """
        if new_capacity < 1:
            return

        # If the new_capacity is not prime, update it to the next
        # prime number
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)

        # Save the old array from the created get keys and values method
        old_array = self.get_keys_and_values()

        original_size = self._size

        # Reinitialize self._buckets to an empty dynamic array,
        # update capacity to new_capacity, and reset size
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        # Add the correct amount of linked lists to the array
        # by using new_capacity as the range
        for index in range(new_capacity):
            self._buckets.append(LinkedList())

        # While loop runs until all original keys and values are added
        while self._size != original_size:
            # Fills the linked lists in the dynamic array
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
        if self._size == 0:
            return self._capacity

        empty_bucket_count = 0

        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            # If the bucket is empty, increment the empty bucket count
            if bucket.length() == 0:
                empty_bucket_count += 1

        return empty_bucket_count

    def get(self, key: str) -> object:
        """
        This function returns the value of the inputted key if the key exists.
        Otherwise, it returns None.
        """
        # Calculate hash_value and index and then find the correct
        # linked_list
        hash_value = self._hash_function(key)
        index = hash_value % self._buckets.length()
        linked_list = self._buckets[index]

        for node in linked_list:
            if node.key == key:
                return node.value

        # If the key wasn't found, the loop is finished and return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        This function returns True if the inputted key is found. Otherwise,
        it returns False.
        """
        if self._size == 0:
            return False

        # Calculate hash_value and index and then find the correct
        # linked_list
        hash_value = self._hash_function(key)
        index = hash_value % self._buckets.length()
        linked_list = self._buckets[index]

        for node in linked_list:
            if node.key == key:
                return True

        # If the key wasn't found, the loop is finished and return False
        return False

    def remove(self, key: str) -> None:
        """
        This function removes the key from the hashmap.
        """
        # Calculate hash_value and index and then find the correct
        # linked_list
        hash_value = self._hash_function(key)
        index = hash_value % self._buckets.length()
        linked_list = self._buckets[index]

        for node in linked_list:
            # If the key is found, remove the key and decrement size
            if node.key == key:
                linked_list.remove(key)
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        This function returns an array with a tuple containing a key and value pair
        at each index.
        """
        new_array = DynamicArray()
        for index in range(self._capacity):
            # Obtains each bucket to create the tuple with each node's keys
            # and values
            bucket = self._buckets.get_at_index(index)
            # Creates tuple and adds it to the new array
            for node in bucket:
                key_value_tuple = (node.key, node.value)
                new_array.append(key_value_tuple)

        return new_array

    def clear(self) -> None:
        """
        This function clears the hashmap.
        """
        # Empty buckets and sets size to 0
        self._buckets = DynamicArray()
        self._size = 0

        # Add the right amount of linked lists to the hashmap
        for index in range(self._capacity):
            self._buckets.append(LinkedList())

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function finds the mode from the inputted array and
    returns a tuple with a new array filled with all the mode values
    and the frequency of the mode.
    """
    map = HashMap()
    mode_array = DynamicArray()

    # Adds the values from da into map. The key is the element from da
    # and the value is the frequency
    for index in range(da.length()):
        new_key = da.get_at_index(index)
        new_value = 1
        # If the key is already in map, obtain the value and increment it
        if map.contains_key(new_key):
            new_value = map.get(new_key)
            new_value += 1
        map.put(new_key, new_value)

    # Creates a new dynamic array with the keys and values in tuples
    find_mode_array = map.get_keys_and_values()
    mode_value = 0

    # Adds the mode values to mode_array
    for index in range(find_mode_array.length()):
        # Unpack tuple
        find_mode_array_tuple = find_mode_array[index]
        find_mode_array_key = find_mode_array_tuple[0]
        find_mode_array_value = find_mode_array_tuple[1]
        # If the value from the tuple is equal than the mode_value,
        # add the key from the tuple to the mode_array
        if find_mode_array_value == mode_value:
            mode_array.append(find_mode_array_key)
        # If the value from the tuple is greater than the mode_value,
        # clear the mode_array, update the mode_value, and add the key
        # from the tuple to the mode_array
        if find_mode_array_value > mode_value:
            mode_array = DynamicArray()
            mode_value = find_mode_array_value
            mode_array.append(find_mode_array_key)

    find_mode_tuple = (mode_array, mode_value)
    return find_mode_tuple

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
