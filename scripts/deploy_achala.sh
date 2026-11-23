#!/bin/bash
# Deploy the Achala site build to the gh-pages branch of DeepMindQ/achala.
# Requires the GitHub token at /tmp/.ghtoken (0600).
# Usage: bash /home/z/my-project/achala-main/scripts/deploy_achala.sh
# Layout (2026-11-23): source worktree = achala-main (branch main),
# deployed-site worktree = achala (branch gh-pages). Build happens HERE.
set -euo pipefail
cd /home/z/my-project/achala-main

if [ ! -s /tmp/.ghtoken ]; then
  echo "ERROR: /tmp/.ghtoken missing — write the GitHub token to that file first:"
  echo "  install -m 600 /dev/stdin /tmp/.ghtoken <<< 'github_pat_...'"
  exit 1
fi

# 1. credential helper (tmpfs-safe)
cat > /tmp/ghcred.sh <<'EOF'
#!/bin/bash
echo "username=DeepMindQ"
echo "password=$(cat /tmp/.ghtoken)"
EOF
chmod 700 /tmp/ghcred.sh
git config --local credential.helper /tmp/ghcred.sh

# 2. fresh export build with basePath /achala
#    Next 16 writes the export into distDir (.next-export) — mirror it to out/
#    so a stale no-basePath out/ can never reach gh-pages (2026-11-23 outage).
cd site
rm -rf out .next-export out-gh
NEXT_STATIC_EXPORT=1 GHPAGES=1 NEXT_TELEMETRY_DISABLED=1 npx next build
mv .next-export out
rm -rf out-gh
cp -r out out-gh
python3 ../scripts/postbuild.py out-gh
cd ..

# 3. sync worktree with remote gh-pages
git fetch origin gh-pages 2>/dev/null || true
git worktree remove --force .gh-deploy 2>/dev/null || true
rm -rf .gh-deploy
git worktree prune
git worktree add --force .gh-deploy gh-pages
git -C .gh-deploy reset --hard origin/gh-pages 2>/dev/null || true

# 4. ADDITIVE overlay — keep .git AND every previously deployed hashed asset
#    (2026-11-23: full-wipe deploys deleted _next chunks still referenced by
#    cached HTML, so pages rendered blank until a hard refresh. GitHub Pages
#    serves HTML with max-age=600, so old chunk files MUST stay reachable.)
#    CRITICAL: no CNAME (custom domain belongs to the DataQ repo)
cd .gh-deploy
cp -r ../site/out-gh/. .
rm -f CNAME
touch .nojekyll
cd ..

# 5. commit + push
MAIN_TIP=$(git rev-parse --short main)
LABEL="${WAVE_LABEL:-site update}"
git -C .gh-deploy add -A
git -C .gh-deploy commit -m "Deploy Achala site — ${LABEL} (main tip ${MAIN_TIP})" --quiet
git push origin gh-pages 2>&1 | tail -2
git worktree remove --force .gh-deploy
echo "DEPLOY DONE — verify https://deepmindq.github.io/achala/"
