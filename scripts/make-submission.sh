#!/bin/sh
# Refresh the "Seminar 2 Submission" folder from the four files in the repo root
# and check that every copy is identical. Run from the repo root:
#   sh scripts/make-submission.sh
set -e
DIR="Seminar 2 Submission"
mkdir -p "$DIR"
for f in project-specification.md data.json data.xml presentation.pptx; do
  cp "$f" "$DIR/$f"
  a=$(shasum -a 256 "$f" | cut -d' ' -f1)
  b=$(shasum -a 256 "$DIR/$f" | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then echo "identical: $f"; else echo "DIFFERENT: $f"; exit 1; fi
done
