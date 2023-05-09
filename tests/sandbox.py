class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


roles = {
    'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
    'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
    'Admin': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
}

default_role = 'User'
# for role in roles:
#     new_role = Role.query.filter_by(name=role).first()
#     if new_role is None:
#         new_role = Role(name=role)
#     new_role.reset_permission()

print(roles['User'])
print(roles['Admin'])