class IterableObject:
    class Iterator:
        def __init__(self, entities):
            self._elements = entities
            self._keys = list(self._elements._data)
            self._current_position = 0

        def __next__(self):
            if self._current_position == len(self._elements._data):
                raise StopIteration()
            current_key = self._keys[self._current_position]
            self._current_position += 1
            return self._elements._data[current_key]

    def __init__(self):
        self._data = {}

    def __iter__(self):
        return self.Iterator(self)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __len__(self):
        return len(self._data)


def shell_sort(array, sort_key):
    """
    Sorts a given array by a given sort key using shell sort
    :return:-
    """
    leng = len(array)
    gap = leng // 2

    while gap > 0:

        for i in range(gap, leng):
            temp = array[i]

            j = i
            while j >= gap and sort_key(temp, array[j - gap]):
                array[j] = array[j - gap]
                j -= gap

            array[j] = temp

        gap //= 2


def filter_entities(array, condition):
    """
    Filters a given array by a certain condition
    :return: the filtered array
    """
    filtered_array = [element for element in array if condition(element)]
    return filtered_array
