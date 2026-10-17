#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
printf '==============================\nStudent Information\n==============================\n\n'
if [[ -f "$ROOT/Kim_Vyacheslav_info.txt" ]]; then
  cat "$ROOT/Kim_Vyacheslav_info.txt"
else
  printf 'Name: Vyacheslav\nSurname: Kim\nGroup: IT2-2312\nStudent ID: 37746\n'
fi
printf '\n==============================\nSystem Information\n==============================\n\n'
printf 'Username: '; whoami
printf 'Hostname: '; hostname
printf 'Current Date: '; date
printf 'Operating System: '; uname -a
printf '\nDisk Usage:\n'; df -h /
printf '\nMemory Usage:\n'; free -h
if [[ -f "$ROOT/Kim_Vyacheslav_info.txt" ]]; then
  echo 'Student information file exists.'
else
  echo 'Student information file does not exist.'
fi
