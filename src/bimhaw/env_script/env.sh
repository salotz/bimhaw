# common environment in all shells

# the place your dotfiles is installed
export BIMHAW_DIR="$HOME/.bimhaw";

export ARCHIVE_DIR="$BIMHAW_DIR/archive";
export BIN_DIR="$BIMHAW_DIR/bin";
export DOCS_DIR="$BIMHAW_DIR/docs";
export PROFILES_DIR="$BIMHAW_DIR/profiles";
export UTILS_DIR="$BIMHAW_DIR/utils";

# the symlink to the active profile directory
export ACTIVE_PROFILE_DIR="$BIMHAW_DIR/active";

# TODO DEPRECATE, small paths are alright here and just as easy to
# remember and less opaque

# libraries for the profile
export ACTIVE_SHELLS_DIR="$ACTIVE_PROFILE_DIR/lib/shell";
export ACTIVE_CONFIGS_DIR="$ACTIVE_PROFILE_DIR/lib/configs";
export ACTIVE_SETUPS_DIR="$ACTIVE_PROFILE_DIR/lib/setups";
export ACTIVE_BIN_DIR="$ACTIVE_PROFILE_DIR/lib/bin";
export ACTIVE_CHECKINS_DIR="$ACTIVE_PROFILE_DIR/lib/checkins";
export ACTIVE_CHECKOUTS_DIR="$ACTIVE_PROFILE_DIR/lib/checkouts";
export ACTIVE_INITS_DIR="$ACTIVE_PROFILE_DIR/lib/inits";
export ACTIVE_RESOURCES_DIR="$ACTIVE_PROFILE_DIR/lib/resources";

# shell specific things since they are relatively finite
export ACTIVE_BASH_DIR="$ACTIVE_SHELLS_DIR/bash";
export ACTIVE_SH_DIR="$ACTIVE_SHELLS_DIR/sh";
export ACTIVE_XONSH_DIR="$ACTIVE_SHELLS_DIR/xonsh";

# other shared directories
export LIB_DIR="$BIMHAW_DIR/lib";

# TODO DEPRECATE

# binaries
export BIN_LIB_DIR="$LIB_DIR/bin";
# configs
export CONFIGS_LIB_DIR="$LIB_DIR/configs";
# setup scripts
export SETUPS_LIB_DIR="$LIB_DIR/setups";

# END DEPRECATE

### Shell configs

## POSIX sh dirs

# the hierarchy for this shell
export SHELL_LIB_DIR="$LIB_DIR/shell/sh";

# the different categories of libs (for POSIX sh these are often
# shared with POSIX derivateives like bash)
export SHELL_FUNC_DIR="$SHELL_LIB_DIR/funcs";
export SHELL_ALIAS_DIR="$SHELL_LIB_DIR/aliases";
export SHELL_ENV_DIR="$SHELL_LIB_DIR/envs";
export SHELL_LOGOUT_DIR="$SHELL_LIB_DIR/logouts";
export SHELL_PROMPT_DIR="$SHELL_LIB_DIR/prompts";

## BASH dirs
export BASH_LIB_DIR="$LIB_DIR/shell/bash";

export BASH_ENV_DIR="$BASH_LIB_DIR/envs";
export BASH_LOGOUT_DIR="$BASH_LIB_DIR/logouts";
export BASH_ALIAS_DIR="$BASH_LIB_DIR/aliases";
export BASH_FUNC_DIR="$BASH_LIB_DIR/funcs";
export BASH_PROMPT_DIR="$BASH_LIB_DIR/prompts";

# bash specific features
export BASH_AUTOCOMPLETE_DIR="$BASH_LIB_DIR/autocomplete";

## XONSH dirs
export XONSH_LIB_DIR="$LIB_DIR/shell/bash";

export XONSH_ENV_DIR="$XONSH_LIB_DIR/envs";
export XONSH_LOGOUT_DIR="$XONSH_LIB_DIR/logouts";
export XONSH_ALIAS_DIR="$XONSH_LIB_DIR/aliases";
export XONSH_FUNC_DIR="$XONSH_LIB_DIR/funcs";
export XONSH_PROMPT_DIR="$XONSH_LIB_DIR/prompts";

# xonsh specific features
export XONSH_AUTOCOMPLETE_DIR="$XONSH_LIB_DIR/autocomplete";

# a function that defines a way to easily redirect output to stderr
# (for debugging this init configuration) so that we keep stdout
# clean. This is necessary for remote execution stuff

#errcho(){ >&2 echo $@; };

