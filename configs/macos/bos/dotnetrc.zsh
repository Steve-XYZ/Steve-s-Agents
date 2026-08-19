# BOS workspace .NET SDK switcher
# Usage:
#   source /Users/stive/Documents/Code/BOS/.dotnetrc.zsh
#   dotnet8      # Homebrew .NET 8
#   dotnet9      # Homebrew .NET 9
#   dotnet10     # Homebrew .NET 10
#   dotnet10201  # Local SDK 10.0.201 when available
#
# Auto-switching is enabled by default when this file is sourced from zsh.
# Disable it with: export BOS_DOTNET_AUTO=0

export BOS_ROOT="${BOS_ROOT:-/Users/stive/Documents/Code/BOS}"
export BOS_DOTNET_8_ROOT="${BOS_DOTNET_8_ROOT:-/opt/homebrew/opt/dotnet@8}"
export BOS_DOTNET_9_ROOT="${BOS_DOTNET_9_ROOT:-/opt/homebrew/opt/dotnet@9}"
export BOS_DOTNET_10_ROOT="${BOS_DOTNET_10_ROOT:-/opt/homebrew/opt/dotnet@10}"
export BOS_DOTNET_10_201_ROOT="${BOS_DOTNET_10_201_ROOT:-$HOME/.dotnet/10.0.201}"
export BOS_DOTNET_AUTO="${BOS_DOTNET_AUTO:-1}"

_bos_remove_dotnet_paths() {
  local entry
  local -a kept_paths

  for entry in ${(s/:/)PATH}; do
    case "$entry" in
      "$BOS_DOTNET_8_ROOT/bin"|"$BOS_DOTNET_9_ROOT/bin"|"$BOS_DOTNET_10_ROOT/bin"|"$BOS_DOTNET_10_201_ROOT")
        continue
        ;;
    esac
    kept_paths+=("$entry")
  done

  print -r -- "${(j/:/)kept_paths}"
}

_bos_dotnet_candidate() {
  local version="$1"
  local root=""
  local bin_path=""
  local dotnet_root=""

  case "$version" in
    8|8.*)
      root="$BOS_DOTNET_8_ROOT"
      bin_path="$root/bin"
      dotnet_root="$root/libexec"
      ;;
    9|9.*)
      root="$BOS_DOTNET_9_ROOT"
      bin_path="$root/bin"
      dotnet_root="$root/libexec"
      ;;
    10.0.201|10201)
      if [ -x "$BOS_DOTNET_10_201_ROOT/dotnet" ]; then
        bin_path="$BOS_DOTNET_10_201_ROOT"
        dotnet_root="$BOS_DOTNET_10_201_ROOT"
      else
        root="$BOS_DOTNET_10_ROOT"
        bin_path="$root/bin"
        dotnet_root="$root/libexec"
      fi
      ;;
    10|10.*)
      root="$BOS_DOTNET_10_ROOT"
      bin_path="$root/bin"
      dotnet_root="$root/libexec"
      ;;
    *)
      echo "Unsupported .NET SDK version: $version" >&2
      return 1
      ;;
  esac

  if [ ! -x "$bin_path/dotnet" ]; then
    echo "No dotnet executable found at $bin_path/dotnet" >&2
    return 1
  fi

  print -r -- "$bin_path|$dotnet_root"
}

use_dotnet() {
  local version="$1"
  local quiet="$2"
  local candidate
  local bin_path
  local dotnet_root
  local clean_path
  local selected_sdk

  if [ -z "$version" ]; then
    echo "Usage: use_dotnet 8|9|10|<8.x|9.x|10.x SDK version>" >&2
    return 1
  fi

  candidate="$(_bos_dotnet_candidate "$version")" || return 1
  bin_path="${candidate%%|*}"
  dotnet_root="${candidate#*|}"
  clean_path="$(_bos_remove_dotnet_paths)"

  selected_sdk="$(env DOTNET_ROOT="$dotnet_root" PATH="$bin_path:$clean_path" "$bin_path/dotnet" --version 2>&1)"
  if [ $? -ne 0 ]; then
    echo "Unable to activate .NET $version for $PWD:" >&2
    echo "$selected_sdk" >&2
    return 1
  fi

  export DOTNET_ROOT="$dotnet_root"
  export PATH="$bin_path:$clean_path"
  export BOS_DOTNET_REQUESTED="$version"
  export BOS_DOTNET_ACTIVE="$selected_sdk"

  hash -r
  if [ "$quiet" != "--quiet" ]; then
    echo "Using .NET $selected_sdk from $bin_path/dotnet"
  fi
}

current_dotnet() {
  echo "DOTNET_ROOT=$DOTNET_ROOT"
  command -v dotnet
  dotnet --version
  dotnet --list-sdks
}

# Function wrappers also work in non-interactive zsh shells after sourcing.
dotnet8() { use_dotnet 8; }
dotnet9() { use_dotnet 9; }
dotnet10() { use_dotnet 10; }
dotnet10201() { use_dotnet 10.0.201; }

_bos_git_common_dir() {
  git -C "$1" rev-parse --path-format=absolute --git-common-dir 2>/dev/null
}

typeset -g BOS_PLAYER_MANAGER_GIT_COMMON_DIR="${BOS_PLAYER_MANAGER_GIT_COMMON_DIR:-$(_bos_git_common_dir "$BOS_ROOT/player-manager")}"
typeset -g BOS_LOTTO_PROPAGATOR_GIT_COMMON_DIR="${BOS_LOTTO_PROPAGATOR_GIT_COMMON_DIR:-$(_bos_git_common_dir "$BOS_ROOT/lotto-propagator")}"
typeset -g BOS_DOTNET_CONTEXT_KIND=""
typeset -g BOS_DOTNET_WORKTREE_ROOT=""

_bos_refresh_context() {
  local worktree_root
  local common_dir

  BOS_DOTNET_CONTEXT_KIND=""
  BOS_DOTNET_WORKTREE_ROOT=""

  if [ "${PWD:A}" = "${BOS_ROOT:A}" ]; then
    BOS_DOTNET_CONTEXT_KIND="workspace"
    BOS_DOTNET_WORKTREE_ROOT="${BOS_ROOT:A}"
    return 0
  fi

  worktree_root="$(git rev-parse --path-format=absolute --show-toplevel 2>/dev/null)" || return 1
  common_dir="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" || return 1

  case "$common_dir" in
    "$BOS_PLAYER_MANAGER_GIT_COMMON_DIR")
      BOS_DOTNET_CONTEXT_KIND="player-manager"
      ;;
    "$BOS_LOTTO_PROPAGATOR_GIT_COMMON_DIR")
      BOS_DOTNET_CONTEXT_KIND="lotto-propagator"
      ;;
    *)
      return 1
      ;;
  esac

  BOS_DOTNET_WORKTREE_ROOT="$worktree_root"
}

_bos_find_global_json() {
  local dir="${PWD:A}"
  local worktree_root="${BOS_DOTNET_WORKTREE_ROOT:A}"

  [ -n "$BOS_DOTNET_WORKTREE_ROOT" ] || return 1

  while true; do
    if [ -e "$dir/global.json" ]; then
      print -r -- "$dir/global.json"
      return 0
    fi

    [ "$dir" = "$worktree_root" ] && break
    case "$dir/" in
      "$worktree_root/"*) dir="${dir:h}" ;;
      *) break ;;
    esac
  done

  return 1
}

_bos_dotnet_version_for_context() {
  local global_json
  local version

  case "$BOS_DOTNET_CONTEXT_KIND" in
    workspace)
      print -r -- "10"
      return 0
      ;;
    player-manager|lotto-propagator)
      if global_json="$(_bos_find_global_json)"; then
        if ! command -v jq >/dev/null 2>&1; then
          echo "jq is required to read $global_json" >&2
          return 2
        fi

        version="$(jq -er '.sdk.version | select(type == "string" and length > 0)' "$global_json" 2>/dev/null)"
        if [ $? -ne 0 ]; then
          echo "Invalid or missing sdk.version in $global_json" >&2
          return 2
        fi

        print -r -- "$version"
        return 0
      fi

      # Branches without global.json are legacy .NET 8 checkouts.
      print -r -- "8"
      return 0
      ;;
  esac

  return 1
}

_bos_auto_dotnet() {
  [ "$BOS_DOTNET_AUTO" = "1" ] || return 0

  local version
  local selected_sdk
  local resolution_rc
  version="$(_bos_dotnet_version_for_context)"
  resolution_rc=$?
  if [ $resolution_rc -ne 0 ]; then
    [ $resolution_rc -eq 1 ] && return 0
    return $resolution_rc
  fi
  [ "$version" = "$BOS_DOTNET_REQUESTED" ] && return 0

  if use_dotnet "$version" --quiet; then
    selected_sdk="$BOS_DOTNET_ACTIVE"
    echo "[BOS] .NET $selected_sdk active for $BOS_DOTNET_CONTEXT_KIND"
    return 0
  fi

  return 1
}

_bos_on_chpwd() {
  _bos_refresh_context
  _bos_auto_dotnet
}

if [ -n "$ZSH_VERSION" ]; then
  autoload -Uz add-zsh-hook

  # Remove old or duplicate registrations when this file is sourced again.
  add-zsh-hook -d chpwd _bos_auto_dotnet 2>/dev/null
  add-zsh-hook -d chpwd _bos_on_chpwd 2>/dev/null
  add-zsh-hook -d precmd _bos_auto_dotnet 2>/dev/null
  add-zsh-hook chpwd _bos_on_chpwd
  add-zsh-hook precmd _bos_auto_dotnet

  _bos_refresh_context
  _bos_auto_dotnet
fi
