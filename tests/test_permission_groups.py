# test_permission_groups.py

import pytest
from permission_groups import merge_permissions, get_perm_status, check_admin_perm, show_inherited_perms

# Mock perm module to simulate the permissions structure
@pytest.fixture(autouse=True)
def mock_perm(monkeypatch):
    mock_groups = {
        "base": {"send_post": True, "edit_post": False},
        "moderator": {"extends": "base", "delete_post": True},
        "admin": {"extends": "moderator", "manage_users": True},
    }
    monkeypatch.setattr("permission_groups.perm.groups", mock_groups)

def test_merge_permissions():
    # Test merging for 'admin' group
    expected_admin_perms = {
        "send_post": True,
        "edit_post": False,
        "delete_post": True,
        "manage_users": True,
    }
    assert merge_permissions("admin") == expected_admin_perms

    # Test merging for 'moderator' group
    expected_moderator_perms = {
        "send_post": True,
        "edit_post": False,
        "delete_post": True,
    }
    assert merge_permissions("moderator") == expected_moderator_perms

    # Test merging for 'base' group
    expected_base_perms = {"send_post": True, "edit_post": False}
    assert merge_permissions("base") == expected_base_perms

def test_get_perm_status():
    # Test fetching the full permission status
    expected_status = {
        "base": {"send_post": True, "edit_post": False},
        "moderator": {"extends": "base", "delete_post": True},
        "admin": {"extends": "moderator", "manage_users": True},
    }
    assert get_perm_status() == expected_status

def test_check_admin_perm():
    # Test checking permissions for 'admin'
    assert check_admin_perm("send_post") is True  # Inherited from 'base'
    assert check_admin_perm("delete_post") is True  # Inherited from 'moderator'
    assert check_admin_perm("manage_users") is True  # Defined in 'admin'
    assert check_admin_perm("non_existent_action") is False  # Non-existent action

def test_show_inherited_perms():
    # Test showing inherited permissions for 'admin'
    expected_admin_perms = {
        "send_post": True,
        "edit_post": False,
        "delete_post": True,
        "manage_users": True,
    }
    assert show_inherited_perms("admin") == expected_admin_perms

