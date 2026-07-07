#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# Copy this file, edit the steps between the markers, and run it.
# The agent runs the script; the user follows the prompts in their terminal.
# Useful when reproduction requires a human action the agent cannot perform
# (staging behind VPN, manual UI steps, external-system checks).
#
# Usage:
#   bash hitl-loop.template.sh
#
# Helpers:
#   step "<instruction>"       → show instruction, wait for Enter
#   capture VAR "<question>"   → show question, read response into VAR
#
# At the end, captured values are printed as KEY=VALUE for the agent to parse.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------

step "Connect to the VPN and open the staging app."

capture ERRORED "Trigger the failing action. Did the symptom occur? (y/n)"

capture DETAILS "Paste the error message, correlation ID, or observed output (or 'none'):"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'DETAILS=%s\n' "$DETAILS"
