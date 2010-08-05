"""Common configuration constants
"""

PROJECTNAME = 'ftw.task'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Task': 'ftw.task: Add Task',
}

# TODO : is a index necessarily ?
INDEXES = (("responsibility", "FieldIndex"),
          )

METADATA = ('responsibility', )
