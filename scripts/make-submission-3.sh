#!/bin/sh
# Build the "Seminar 3 Submission" folder and zip from the files in the repo, and verify the copies.
# Run from the repo root:  sh scripts/make-submission-3.sh
set -e
DIR="Seminar 3 Submission"
rm -rf "$DIR" "$DIR.zip"
mkdir -p "$DIR/docs/evidence"
cp -R prototype "$DIR/prototype"
rm -f "$DIR/prototype/.gitkeep"
cp progress-02.md "$DIR/progress-02.md"
cp presentation-seminar3.pptx "$DIR/presentation.pptx"
cp docs/design-kit.md "$DIR/docs/design-kit.md"
cp docs/evidence/prototype-verification.md docs/evidence/*.jpg "$DIR/docs/evidence/"
for f in progress-02.md; do cmp -s "$f" "$DIR/$f" && echo "identical: $f" || { echo "DIFFERENT: $f"; exit 1; }; done
cmp -s presentation-seminar3.pptx "$DIR/presentation.pptx" && echo "identical: presentation.pptx" || { echo "DIFFERENT: presentation.pptx"; exit 1; }
diff -rq --exclude=.gitkeep prototype "$DIR/prototype" && echo "identical: prototype/"
zip -qrX "$DIR.zip" "$DIR" -x "*.DS_Store"
echo "zip written: $DIR.zip"
