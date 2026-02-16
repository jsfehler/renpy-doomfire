#!/usr/bin/env bash
set -e

lint_c() (
    clang-tidy backend/c/main.c -- -O3 -flto -fPIC -std=c17
)

lint_c_xorshift() (
    clang-tidy backend/c_xorshift/main.c -- -O3 -flto -fPIC -std=c17
)

lint_cy() (
    cd backend/cy

    python -m venv .lint_venv
    source .lint_venv/bin/activate
    pip install cython-lint

    cython-lint doom_fire_cy.pyx
)

lint_cy_randbytes() (
    cd backend/cy_randbytes

    python -m venv .lint_venv
    source .lint_venv/bin/activate
    pip install cython-lint

    cython-lint doom_fire_cy_rand_bytes.pyx
)

lint_py() (
    cd backend/py

    python -m venv .lint_venv
    source .lint_venv/bin/activate
    pip install ruff

    ruff check .
)

lint_rust() (
    cd backend/rust
    cargo clippy
)

lint_perf() (
    cd performance

    python -m venv .lint_venv
    source .lint_venv/bin/activate
    pip install ruff

    ruff check run.py
)

case "${1}" in
    c)                   lint_c ;;
    c_xorshift)          lint_c_xorshift ;;
    cy)                  lint_cy ;;
    cy_randbytes)        lint_cy_randbytes ;;
    py)                  lint_py ;;
    rust)                lint_rust ;;
    perf)                lint_perf ;;
    *)                   echo "Unknown target: $1"; exit 1 ;;
esac
