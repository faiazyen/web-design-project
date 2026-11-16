#!/bin/sh
# Build the "Seminar 4 Submission" folder and zip from the files in the repo, and verify the copies.
# Run from the repo root:  sh scripts/make-submission-4.sh
set -e
DIR="Seminar 4 Submission"
rm -rf "$DIR" "$DIR.zip"
mkdir -p "$DIR/docs/evidence"
cp -R web "$DIR/web"
find "$DIR/web" -name .DS_Store -delete
cp progress-03.md "$DIR/progress-03.md"
cp presentation-seminar4.pptx "$DIR/presentation.pptx"
cp docs/evidence/web-verification.md docs/evidence/web-*.png docs/evidence/web-*.jpg "$DIR/docs/evidence/"
cmp -s progress-03.md "$DIR/progress-03.md" && echo "identical: progress-03.md" || { echo "DIFFERENT: progress-03.md"; exit 1; }
cmp -s presentation-seminar4.pptx "$DIR/presentation.pptx" && echo "identical: presentation.pptx" || { echo "DIFFERENT: presentation.pptx"; exit 1; }
diff -rq --exclude=.DS_Store web "$DIR/web" && echo "identical: web/"
zip -qrX "$DIR.zip" "$DIR" -x "*.DS_Store"
echo "zip written: $DIR.zip"
