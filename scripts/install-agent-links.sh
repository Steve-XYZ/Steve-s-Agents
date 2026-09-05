#!/bin/sh

# Create or repair this machine's canonical agent symlinks.
#
# Idempotent: a target that is already the correct link is left untouched.
# Anything else occupying a target path is moved into a timestamped backup
# directory before the link is created, so nothing is silently discarded.
set -u

usage() {
	cat <<'USAGE'
Usage: install-agent-links.sh [--dry-run]

Links the global guidance file into every installed agent CLI, grants Claude
read access to on-demand guidance, and links each skill directory under shared/
and dotnet/ into every skills directory that belongs to an installed agent CLI.

  --dry-run             report the actions without changing anything
  --codex-skills-root=DIR
                        install personal skills into DIR instead of the
                        detected Codex root
USAGE
}

dry_run=0
codex_root_override=""
for arg in "$@"; do
	case "$arg" in
		--dry-run) dry_run=1 ;;
		--codex-skills-root=*) codex_root_override=${arg#*=} ;;
		-h|--help) usage; exit 0 ;;
		*) echo "unknown option: $arg" >&2; usage >&2; exit 2 ;;
	esac
done

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd) || exit 1
guidance="$repo_root/shared/global-guidance/ENGINEERING.md"
claude_settings_merger="$repo_root/scripts/merge-claude-settings.py"
if [ ! -f "$guidance" ]; then
	echo "not a Steve-s-Agents clone: $repo_root" >&2
	exit 1
fi

backup_root="$HOME/.agent-links-backup"
backup_dir="$backup_root/$(date +%Y%m%d-%H%M%S)"
linked=0
kept=0
moved=0
failed=0
retired=0
codex_home_dir=${CODEX_HOME:-$HOME/.codex}

backup() {
	# Refuse collisions rather than overwriting a backup from an earlier run.
	backup_target="$backup_dir/$(printf '%s' "${1#"$HOME"/}" | tr '/' '_')"
	if [ "$dry_run" -eq 1 ]; then
		echo "would back up $1"
	else
		mkdir -p "$backup_dir" || { failed=$((failed + 1)); return 1; }
		if [ -e "$backup_target" ] || [ -L "$backup_target" ]; then
			echo "backup already exists: $backup_target" >&2
			failed=$((failed + 1)); return 1
		fi
		mv "$1" "$backup_target" || { failed=$((failed + 1)); return 1; }
		echo "backed up $1 -> $backup_target"
	fi
	moved=$((moved + 1))
}

retire_link() {
	# Only migrate the exact links this installer used to create. Real files,
	# other clones, and links with uncertain ownership remain untouched.
	[ -L "$1" ] && [ "$(readlink "$1")" = "$2" ] || return 0
	backup "$1" || return 1
	retired=$((retired + 1))
}

link() {
	source_path=$1
	target_path=$2

	if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$source_path" ]; then
		kept=$((kept + 1))
		return 0
	fi

	if [ -e "$target_path" ] || [ -L "$target_path" ]; then
		backup "$target_path" || return 1
	fi

	if [ "$dry_run" -eq 1 ]; then
		echo "would link $target_path -> $source_path"
	else
		ln -s "$source_path" "$target_path" || { failed=$((failed + 1)); return 1; }
		echo "linked $target_path -> $source_path"
	fi
	linked=$((linked + 1))
}

# Global guidance, once per installed CLI.
for target in "$HOME/.claude/CLAUDE.md" "$codex_home_dir/AGENTS.md"; do
	# Only install for a CLI that is actually present on this machine.
	[ -d "$(dirname "$target")" ] || continue
	link "$guidance" "$target"
done

retire_link "$HOME/.agent-guidance" "$repo_root/shared/global-guidance"

# Skills are symlinked into ~/.claude/skills, so Claude resolves their
# reference files back to this clone. Grant read access to the clone itself.
# Merge only this array entry and preserve every existing setting.
claude_settings_status="skipped"
if [ -d "$HOME/.claude" ]; then
	if ! command -v python3 >/dev/null 2>&1; then
		echo "python3 is required to merge Claude settings" >&2
		claude_settings_status="failed"
		failed=$((failed + 1))
	elif [ ! -f "$claude_settings_merger" ]; then
		echo "missing Claude settings merger: $claude_settings_merger" >&2
		claude_settings_status="failed"
		failed=$((failed + 1))
	else
		if [ "$dry_run" -eq 1 ]; then
			claude_settings_status=$(python3 "$claude_settings_merger" \
				--dry-run \
				--settings "$HOME/.claude/settings.json" \
				--backup-dir "$backup_dir" \
				--required-directory "$repo_root") || {
				claude_settings_status="failed"
				failed=$((failed + 1))
			}
		else
			claude_settings_status=$(python3 "$claude_settings_merger" \
				--settings "$HOME/.claude/settings.json" \
				--backup-dir "$backup_dir" \
				--required-directory "$repo_root") || {
				claude_settings_status="failed"
				failed=$((failed + 1))
			}
		fi
	fi
fi

# Current Codex documents ~/.agents/skills for user skills. CODEX_HOME selects
# configuration and global guidance, not necessarily the personal skill root.
# Older installations observed using CODEX_HOME/skills can pass an explicit
# override. Confirm discovery in the target harness, not from directory presence.
codex_skills_root=""
if [ -n "$codex_root_override" ]; then
	codex_skills_root="$codex_root_override"
elif [ -d "$codex_home_dir" ]; then
	codex_skills_root="$HOME/.agents/skills"
fi

set --
[ -d "$HOME/.claude" ] && set -- "$@" "$HOME/.claude/skills"
if [ -n "$codex_skills_root" ]; then
	set -- "$@" "$codex_skills_root"
	echo "codex personal skills root: $codex_skills_root"
fi

for skills_root do
	if [ ! -d "$skills_root" ]; then
		if [ "$dry_run" -eq 1 ]; then
			echo "would create $skills_root"
		else
			mkdir -p "$skills_root" || { failed=$((failed + 1)); continue; }
		fi
	fi
	retire_link "$skills_root/engineering-judgment" "$repo_root/shared/engineering-judgment"

	for candidate in "$repo_root"/shared/*/ "$repo_root"/dotnet/*/; do
		skill_dir=${candidate%/}
		[ -f "$skill_dir/SKILL.md" ] || continue
		link "$skill_dir" "$skills_root/$(basename "$skill_dir")"
	done
done

echo "linked=$linked kept=$kept backed-up=$moved retired=$retired claude-settings=$claude_settings_status failed=$failed"
[ "$failed" -eq 0 ] || exit 1
exit 0
