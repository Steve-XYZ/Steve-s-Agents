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

Links the global guidance file into every installed agent CLI, and links each
skill directory under shared/ and dotnet/ into every skills directory that
belongs to an installed agent CLI.

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
writing="$repo_root/shared/global-guidance/WRITING.md"
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

link() {
	source_path=$1
	target_path=$2

	if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$source_path" ]; then
		kept=$((kept + 1))
		return 0
	fi

	if [ -e "$target_path" ] || [ -L "$target_path" ]; then
		# Flatten the path so two skills of the same name cannot collide.
		stash="$backup_dir/$(printf '%s' "${target_path#"$HOME"/}" | tr '/' '_')"
		if [ "$dry_run" -eq 1 ]; then
			echo "would back up $target_path"
		else
			mkdir -p "$backup_dir" || { failed=$((failed + 1)); return 1; }
			mv "$target_path" "$stash" || { failed=$((failed + 1)); return 1; }
			echo "backed up $target_path -> $stash"
		fi
		moved=$((moved + 1))
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
for spec in ".claude/CLAUDE.md" ".codex/AGENTS.md"; do
	target="$HOME/$spec"
	# Only install for a CLI that is actually present on this machine.
	[ -d "$(dirname "$target")" ] || continue
	link "$guidance" "$target"
done

# WRITING.md sits beside each entry point on purpose. The entry point is a
# symlink, so its relative reference to WRITING.md may be resolved either
# against the link's directory or against the clone. Linking it here makes both
# resolutions land on the same file.
for spec in ".claude/WRITING.md" ".codex/WRITING.md"; do
	target="$HOME/$spec"
	[ -d "$(dirname "$target")" ] || continue
	link "$writing" "$target"
done

# Which directory holds *personal* Codex skills depends on the installed Codex
# version, not on the operating system: 0.147 used ~/.codex/skills, 0.148 uses
# ~/.agents/skills and keeps only bundled skills under ~/.codex/skills/.system.
#
# The presence of ~/.codex/skills therefore does not mean it is a personal
# root; on a 0.148 machine it exists solely to hold .system. Treat the two as
# mutually exclusive and prefer the dedicated personal root when it exists, so
# that upgrading Codex moves the target instead of installing into both.
codex_skills_root=""
if [ -n "$codex_root_override" ]; then
	codex_skills_root="$codex_root_override"
elif [ -d "$HOME/.agents/skills" ]; then
	codex_skills_root="$HOME/.agents/skills"
elif [ -d "$HOME/.codex" ]; then
	codex_skills_root="$HOME/.codex/skills"
fi

skills_roots=""
[ -d "$HOME/.claude" ] && skills_roots="$HOME/.claude/skills"
if [ -n "$codex_skills_root" ]; then
	skills_roots="$skills_roots $codex_skills_root"
	echo "codex personal skills root: $codex_skills_root"
fi

for skills_root in $skills_roots; do
	if [ ! -d "$skills_root" ]; then
		if [ "$dry_run" -eq 1 ]; then
			echo "would create $skills_root"
		else
			mkdir -p "$skills_root" || { failed=$((failed + 1)); continue; }
		fi
	fi

	for candidate in "$repo_root"/shared/*/ "$repo_root"/dotnet/*/; do
		skill_dir=${candidate%/}
		[ -f "$skill_dir/SKILL.md" ] || continue
		link "$skill_dir" "$skills_root/$(basename "$skill_dir")"
	done
done

echo "linked=$linked kept=$kept backed-up=$moved failed=$failed"
[ "$failed" -eq 0 ] || exit 1
exit 0
