#!/bin/bash
# Generate all 12 Achala IT Solutions docx files, post-process, run TOC placeholders.
set -e
BASE=/home/z/my-project/scripts/achalasolutions
OUT=/home/z/my-project/download/achalasolutions-website-content
DOCX_SCRIPTS=/home/z/my-project/skills/docx/scripts
cd "$BASE"

declare -A FILES=(
  [BLUEPRINT]="$OUT/achala_Soft_Website_Blueprint.docx"
  [V01]="$OUT/Content_Volumes/V01_Home_and_Services.docx"
  [V02]="$OUT/Content_Volumes/V02_Industries_A_Hubs_and_Sub-Industries.docx"
  [V03]="$OUT/Content_Volumes/V03_Industries_B_Hubs_and_Sub-Industries.docx"
  [V04]="$OUT/Content_Volumes/V04_Industry_Capability_Pages_A.docx"
  [V05]="$OUT/Content_Volumes/V05_Industry_Capability_Pages_B.docx"
  [V06]="$OUT/Content_Volumes/V06_Sub-Industry_Capability_Pages_A.docx"
  [V07]="$OUT/Content_Volumes/V07_Sub-Industry_Capability_Pages_B.docx"
  [V08]="$OUT/Content_Volumes/V08_Solutions_and_Platforms.docx"
  [V09]="$OUT/Content_Volumes/V09_Case_Studies.docx"
  [V10]="$OUT/Content_Volumes/V10_Company_Approach_Contact.docx"
  [V11]="$OUT/Content_Volumes/V11_Insights_Library.docx"
)

for KEY in BLUEPRINT V01 V02 V03 V04 V05 V06 V07 V08 V09 V10 V11; do
  SRC="$BASE/out/${KEY}.json"
  DST="${FILES[$KEY]}"
  echo "=== $KEY → $DST"
  node "$BASE/docgen/render_docx.js" "$SRC" "$DST"
  if [ "$KEY" = "BLUEPRINT" ]; then
    python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" "$DST" --auto
  else
    ENTRIES=$(python3 "$BASE/dqs_toc_entries.py" "$SRC")
    python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" "$DST" --entries "$ENTRIES"
  fi
  python3 "$BASE/dqs_docx_post.py" "$DST"
done
echo "ALL DOCX GENERATED"
