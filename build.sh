#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$ROOT_DIR/build"
C_COMPILE_FLAGS="-O3 -flto -fPIC"

mkdir -p build

build_c() (
    local SRC_DIR="$ROOT_DIR/backend/c"
    g++ $C_COMPILE_FLAGS -shared -o "$BUILD_DIR/doom_fire_c.so" "$SRC_DIR/main.c"
)

build_c_xorshift() (
    local SRC_DIR="$ROOT_DIR/backend/c_xorshift"
    g++ $C_COMPILE_FLAGS -shared -o "$BUILD_DIR/doom_fire_c_xorshift.so" "$SRC_DIR/main.c"
)

build_cy() (
    cd backend/cy

    python -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt
    python setup.py build_ext --inplace

    rm -rf build
    rm doom_fire_cy.c
    mv doom_fire_cy.cpython-312-x86_64-linux-gnu.so "$BUILD_DIR"
)

build_cy_randbytes() (
    cd backend/cy_randbytes

    python -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt
    python setup.py build_ext --inplace

    rm -rf build
    rm doom_fire_cy_rand_bytes.c
    mv doom_fire_cy_rand_bytes.cpython-312-x86_64-linux-gnu.so "$BUILD_DIR"

)

build_cy_extern() (
    cd backend/cy_extern

    python -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt
    python setup.py build_ext --inplace

    rm -rf build
    rm doom_fire_cy_extern.c
    mv doom_fire_cy_extern.cpython-312-x86_64-linux-gnu.so "$BUILD_DIR"
)

build_cy_extern_xorshift() (
    cd backend/cy_extern_xorshift

    python -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt
    python setup.py build_ext --inplace

    rm -rf build
    rm doom_fire_cy_extern_xorshift.c
    mv doom_fire_cy_extern_xorshift.cpython-312-x86_64-linux-gnu.so "$BUILD_DIR"
)

build_py() (
    cd backend/py

    cp doom_fire_py_ren.py "$BUILD_DIR"
)

build_py_randbytes() (
    cd backend/py

    cp doom_fire_py_randbytes_ren.py "$BUILD_DIR"
)

build_rust() (
    cd backend/rust

    maturin build --release
    cp target/wheels/doom_fire_rust-0.0.1-cp312-cp312-manylinux_2_34_x86_64.whl "$BUILD_DIR"
)

build_all() (
    build_c
    build_c_xorshift
    build_cy
    build_cy_randbytes
    build_cy_extern
    build_cy_extern_xorshift
    build_py
    build_py_randbytes
    build_rust
)
case "${1}" in
    c)                   build_c ;;
    c_xorshift)          build_c_xorshift ;;
    cy)                  build_cy ;;
    cy_randbytes)        build_cy_randbytes ;;
    cy_extern)           build_cy_extern ;;
    cy_extern_xorshift)  build_cy_extern_xorshift ;;
    py)                  build_py ;;
    py_randbytes)        build_py_randbytes ;;
    rust)                build_rust ;;
    all)                 build_all ;;
    *)                   echo "Unknown target: $1"; exit 1 ;;
esac
