
from bimhaw import CONFIG_DIR

# we just exec the configuration script, so that this module has the
# same variables as it

with open(f"{CONFIG_DIR}/config.py", 'r') as rf:
    exec(rf.read())
