#!/bin/sh
set -e

SOURCE_DIR="/theme-sources" # Volume mounted by Paragon plugin
FINAL_BUILD_DIR="/compiled-themes" # Volume mounted by Paragon plugin
TMP_BUILD_DIR="$(mktemp -d /tmp/paragon-build.XXXXXX)"


has_themes() {
    # This function checks if the --themes flag is present in the arguments
    # Returns 0 if --themes is found, 1 otherwise
    # Usage: has_themes "$@"

    for arg in "$@"; do
        [ "$arg" = "--themes" ] && return 0
    done
    return 1
}

parse_args() {
    # This function parses arguments injected by Tutor.
    # Tutor runs jobs via `sh -e -c '…'`, reserving $1–$3 for its wrapper and
    # bundling all user flags into $4. The function then extracts the raw flags
    # string from $4, shifts off the wrapper args, and verifies—or appends—the
    # selected themes definition.

    if [ "$#" -lt 4 ]; then
        echo "Error: Expected at least 4 args, got $#. Must run via tutor."
        exit 1
    fi

    shift 3

    if ! has_themes "$@"; then
        if [ -n "${PARAGON_ENABLED_THEMES:-}" ]; then
            echo "Using PARAGON_ENABLED_THEMES: ${PARAGON_ENABLED_THEMES}"
            set -- "$@" --themes "${PARAGON_ENABLED_THEMES}"
        fi
    fi

    printf '%s\n' "$@"
}

set -- $(parse_args "$@")

# Executes the Paragon CLI to build themes.
# It uses a temporary directory to avoid volume permissions issues
npx paragon build-tokens \
    --source "$SOURCE_DIR" \
    --build-dir "$TMP_BUILD_DIR" \
    "$@"

# Moves the built themes to the final volume directory.
mkdir -p "$FINAL_BUILD_DIR"
cp -a "$TMP_BUILD_DIR/." "$FINAL_BUILD_DIR/"
chmod -R a+rw "$FINAL_BUILD_DIR"

# Clean up
rm -rf "$TMP_BUILD_DIR"

exit 0
