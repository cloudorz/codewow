# coding: utf-8

from flaskext.principal import RoleNeed, Permission

sa = Permission(RoleNeed('super'))
admin = Permission(RoleNeed('admin'))
normal = Permission(RoleNeed('auth'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))
