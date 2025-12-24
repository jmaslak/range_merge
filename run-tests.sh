#!/bin/sh

uv build && \
    uv run mypy src && \
    uv run stubtest range_merge && \
    uv run ruff check && \
    uv run --python=3.14 pytest && \
    uv run --python=3.10 --resolution=lowest pytest && \
    echo "Everythin glooks good!"

