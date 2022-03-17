#!/usr/bin/python
class FilterModule(object):

    def filters(self):
        return {
            'get_ranges': self.get_ranges,
        }

    def get_ranges(self, data, safe: bool = False, validate: bool = True, remove_unwanted: bool = True):
        try:
            if validate:
                if type(data) != list:
                    raise TypeError(f'Invalid type received, expected list, got {type(data)})')

                if len(data) == 0:
                    raise ValueError('Received list that did not contain any data')

            if safe:
                if len(data) != len([x for x in data if type(x) == int]):
                    raise ValueError('Received list that contained items that were not of type `int`')

            if remove_unwanted:
                original_size = len(data)
                data = [x for x in data if type(x) == int]

        except Exception as e:
            print(f'fatal: {e}')

        # Ensure we only have unique values and resort
        data = sorted(list(set(data)))
        worked_list = []

        while len(data) > 0:
            working_list = []
            for i in range(len(data)):
                if (data[0] + i) == data[0+i]:
                    working_list.append(data[i])
                else:
                    break
            data = sorted(list(set(data) - set(working_list)))
            if len(working_list) == 1:
                worked_list.append(f'{working_list[0]}')
            else:
                worked_list.append(f'{working_list[0]}-{working_list[-1]}')

        return worked_list
