#!/bin/bash
# Deploy out-gh/ to gh-pages. Requires the GitHub token at /tmp/.ghtoken (0600).
# Usage: bash /home/z/my-project/scripts/deploy_gh.sh
set -euo pipefail
cd /home/z/my-project

if [ ! -s /tmp/.ghtoken ]; then
  echo "ERROR: /tmp/.ghtoken missing — write the GitHub token to that file first:"
  echo "  install -m 600 /dev/stdin /tmp/.ghtoken <<< 'ghp_...'"
  exit 1
fi

# 1. recreate credential helper (tmpfs-safe)
cat > /tmp/ghcred.sh <<'EOF'
#!/bin/bash
echo "username=DeepMindQ"
echo "password=$(cat /tmp/.ghtoken)"
EOF
chmod 700 /tmp/ghcred.sh
git config --local credential.helper /tmp/ghcred.sh

# 2. sync worktree with remote gh-pages (may have moved)
git fetch origin gh-pages 2>/dev/null || true
git worktree remove --force .gh-deploy 2>/dev/null || true
rm -rf .gh-deploy
git worktree add --force .gh-deploy gh-pages
git -C .gh-deploy reset --hard origin/gh-pages 2>/dev/null || true

# 3. replace content, keep .git
cd .gh-deploy
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r ../site/out-gh/. .
cd ..

# 4. commit + push
MAIN_TIP=$(git rev-parse --short main)
LABEL="${WAVE_LABEL:-site update}"
git -C .gh-deploy add -A
git -C .gh-deploy commit -m "Deploy ${LABEL} (main tip ${MAIN_TIP})" --quiet
git push origin gh-pages 2>&1 | tail -2
git worktree remove --force .gh-deploy
echo "DEPLOY DONE — verify https://deepmindq.github.io/achala/services/"
