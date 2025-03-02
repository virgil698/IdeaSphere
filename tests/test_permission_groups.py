import pytest
from permission_groups import extend_permission, base_dict, basic_perm_dict, read_perm_from_yaml, parse_basic_perm_data, get_perm_dict, parser

def test_extend_permission():
    @extend_permission(base_dict)
    def test_func(perm):
        return perm
    result = test_func()
    assert result == base_dict

def test_read_perm_from_yaml():
    perm_yaml = read_perm_from_yaml()
    assert isinstance(perm_yaml, dict)

def test_parse_basic_perm_data():
    perm_yaml = parse_basic_perm_data()
    assert 'basic' in perm_yaml

def test_get_perm_dict():
    perm_dict = get_perm_dict()
    assert isinstance(perm_dict, dict)

def test_parser():
    parsed_perm_dict = parser()
    assert isinstance(parsed_perm_dict, dict)