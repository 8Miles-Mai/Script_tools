import os

file_path = 'exec'
if os.path.isdir(file_path):
    print 'pass'
    pass
else:
    os.mkdir(file_path)
