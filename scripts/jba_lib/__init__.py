"""Shared helpers for Japan Basketball Archive data-factory scripts.

This package exists to stop re-implementing the same CSV I/O, ID
allocation, and Organization-name checks in every new
`build_batch_*.py` / `validate_batch_*.py` script. It does not change
Governance v1.0: it never assigns MASTER status, never guesses at
unknown values, and never auto-merges organizations that merely look
similar. It only removes repetitive, error-prone plumbing.

Existing historical scripts (scripts/build_batch_*.py etc. from
Batch 001-006) are left untouched on purpose -- they are the audit
trail of what actually produced each approved batch. New scripts
(Batch 007 onward) should import from here instead of copy-pasting
`read`/`write`/`merge` helpers again.
"""

