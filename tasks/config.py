"""User settings for a project."""

# load the system configuration. You can override them in this module,
# but beware it might break stuff
from .sysconfig import *

### Project Metadata

# the name of the project
PROJECT_NAME = "bimhaw"

# the url compatible name of the project
PROJECT_SLUG = "bimhaw"

# copyright options:
# https://en.wikipedia.org/wiki/Creative_Commons_license#Seven_regularly_used_licenses
# CCO, BY, BY-SA, BY-NC, BY-NC-SA, BY-ND, BY-NC-ND

# copyright of the project
PROJECT_COPYRIGHT = "MIT"

## Project Owner

# real name of the owner of the project
OWNER_NAME = "Samuel D. Lotz"

# email of the owner
OWNER_EMAIL = "salotz@salotz.info"

# handle/username/nickname of the owner
OWNER_NICKNAME = "salotz"

## Updating

# where to download git repos to; the "cookiejar"
COOKIEJAR_DIR = "$HOME/tmp/cookiejar"

# URL to get updates from
UPDATE_URL="https://github.com/salotz/salotz-py-cookiecutter.git"

### Environments

PY_ENV_NAME = 'bimhaw.dev'
PY_VERSION = '3.7'

SHELL_PROFILE = 'common'

### VCS

### Packaging

## Python

### Org Tangling

TANGLE_DIRS = []

TANGLE_FILES = []
