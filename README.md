# Custom Ansible Filters

Storage of useful filters I've created to solve specific data manipulation issues
while working with Ansible.

### `get_ranges`

This filter resolves an issue I have when I need to compress lists that contain
integers such as VLAN ranges to make them more readable and ensure I'm not
overloading a networking device's CLI.

#### Use

Given a list of integers, we want to get a list of compressed values like so:

```python
[1,2,3,4,5,6,7,8,9,10
# ['1-10']

[1,3,5,6,7,8,9,10]
# ['1', '3', '5-10']

[1,1,1,1,2,2,2,2,3,3,3,3]
# ['1-3']

['a', 'b', 1, 3, 2]
# ['1-3']
```

This could then be used when formatting CLI configuration for Cisco devices:

```text
# Old
# {{ [1,2,3,4,5,6,7,9,10] }}
# New
# {{ [1,2,3,4,5,6,7,9,10] | get_ranges | join(',') }}

interface GigabitEthernet1/0/1
  switchport mode trunk
  # Old
  switchport trunk allowed vlan 1,2,3,4,5,6,7,8,9,10
  # New
  switchport trunk allowed vlan 1-10
```

###### Arguments

| name | type | default | description |
|------|------|---------|-------------|
| safe | bool | false | Forces all items to be of type `int` when running |
| validate | bool | true | Checks to ensure that a list was received and it was non-zero in length |
| remove\_unwanted | bool | false | When enabled, will only keep items in given list that are `int` |

###### Demo

```yaml
---
- name: Demo usage of `get_ranges` filter
  hosts: localhost
  gather_facts: no
  vars:
    cleantestdata:
        # Sequential
      - [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # Mixture of sequential and non-sequential
      - [1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 100]
        # Non-sequential and out of order ranges
      - [1, 2, 5, 4, 9, 8, 7, 6, 10]
        # Sequential w/ removal of duplicates
      - [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 4, 5, 6, 7, 7, 7, 7]
    dirtytestdata:
        # Bad types in list
      - [1, '2', 3, 'a', 'b', 4, 5, 6, true]
    unworkabletestdata:
      # Types of data that will fail
      - 0
      - False
      - {'test': 1}
      - []
  tasks:
    - name: "[clean] no opts"
      ansible.builtin.debug:
        msg: "{{ item | get_ranges }}"
      loop: "{{ cleantestdata }}"

    # Dirty Test Data
    - name: "[dirty] no opts"
      ansible.builtin.debug:
        msg: "{{ item | get_ranges }}"
      loop: "{{ dirtytestdata }}"

    # Un-workable Test Data
    - name: "[un-workable] no opts"
      ansible.builtin.debug:
        msg: "{{ item | get_ranges }}"
      loop: "{{ unworkabletestdata }}"
```
