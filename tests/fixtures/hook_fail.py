#!/usr/bin/env python3
"""Dummy hook script for tests — exit 1."""
import sys

print("hook_fail", file=sys.stderr)
sys.exit(1)
