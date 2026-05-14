#!/bin/bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

if command -v tmux &>/dev/null; then
    SESSION="resume-matcher"

    # Kill any existing session with this name
    tmux kill-session -t "$SESSION" 2>/dev/null || true

    # Start backend in first window
    tmux new-session -d -s "$SESSION" -n backend \
        "cd '$REPO_ROOT/apps/backend' && uv run app; read"

    # Start frontend in second window
    tmux new-window -t "$SESSION" -n frontend \
        "cd '$REPO_ROOT/apps/frontend' && npm run dev; read"

    # Focus backend window and attach
    tmux select-window -t "$SESSION:backend"
    tmux attach -t "$SESSION"
else
    echo "tmux not found — starting backend and frontend in foreground (interleaved output)"
    echo "Install tmux for separate panes: sudo apt install tmux"
    echo ""

    cd "$REPO_ROOT/apps/backend"
    uv run app &
    BACKEND_PID=$!

    cd "$REPO_ROOT/apps/frontend"
    npm run dev &
    FRONTEND_PID=$!

    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
    wait
fi
