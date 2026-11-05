#!/bin/bash
# run_tests.sh - runs every test input through the Front End and saves the results.
#
# Usage:  ./run_tests.sh [run_name] [program]
#   run_name  name of the folder (inside tests/outputs) for this run's results
#             (default: latest)
#   program   the Front End program to test (default: ./distribution-system)
#
# For each file tests/inputs/NAME.in this script runs the program like this:
#   program currentaccounts.txt availablegames.txt gamescollection.txt NAME.atf < NAME.in > NAME.out
# and saves two files in tests/outputs/run_name/:
#   NAME.out  what the program printed on the terminal
#   NAME.atf  the daily transaction file the program wrote

RUN_NAME=${1:-latest}
PROGRAM=${2:-./distribution-system}
DATA_DIR=data
INPUT_DIR=tests/inputs
OUTPUT_DIR=tests/outputs/$RUN_NAME
WORK_DIR=$OUTPUT_DIR/work      # scratch copy of the data files

# Start from an empty results folder so old results can never be mistaken for new ones.
rm -rf "$OUTPUT_DIR"
mkdir -p "$WORK_DIR"

count=0
for input in "$INPUT_DIR"/*.in; do
    name=$(basename "$input" .in)
    echo "running test $name"

    # Give every test fresh copies of the data files. Even if the program wrongly
    # wrote to one of its input files, the originals in data/ stay untouched and
    # no test can affect the next one.
    cp "$DATA_DIR"/*.txt "$WORK_DIR"/

    # Create the .atf file empty first, so that a test where the program writes no
    # transactions still has a file to compare with.
    : > "$OUTPUT_DIR/$name.atf"

    "$PROGRAM" "$WORK_DIR/currentaccounts.txt" "$WORK_DIR/availablegames.txt" \
               "$WORK_DIR/gamescollection.txt" "$OUTPUT_DIR/$name.atf" \
               < "$input" > "$OUTPUT_DIR/$name.out"

    count=$((count + 1))
done

rm -rf "$WORK_DIR"
echo "ran $count tests; results are in $OUTPUT_DIR"