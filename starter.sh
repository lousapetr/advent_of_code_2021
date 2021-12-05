#!/bin/bash

YEAR=2021
TOKEN=$(cat aoc_token.txt)
# find your token like this https://github.com/wimglenn/advent-of-code-wim/issues/1
# and save to file 'aoc_token.txt' - add it to .gitignore to not share


##############################
# Read day number, set paths
day=$1

# check if there are any parameters
if [ $# -eq 0 ]
then
    echo "No arguments supplied, aborting"
    echo "Use day number as parameter"
    exit
elif [ -z "${day##*[!0-9]*}" ]  # https://stackoverflow.com/a/2704760/9003767
then
    echo "Non-integer supplied, aborting"
    echo "Use day number as parameter"
    exit
else
    echo "Day $day begins!"
fi

day_pad=$(printf '%02s' $day)

daily_url="https://adventofcode.com/${YEAR}/day/${day}"
input_url="${daily_url}/input"
input_file="./inputs/${day_pad}_input.txt"
example_file="./inputs/${day_pad}_input_example.txt"
code_file="./${day_pad}.py"


##############################
# Download puzzle input
echo "================================"
echo "Check the puzzle at ${daily_url}"
echo "================================"

if [ -f "$input_file" ]
then
    echo "Solution file $input_file already exists."
else
    echo "Downloading input from ${input_url}"
    curl --cookie "session=${TOKEN}" "$input_url" --output "$input_file"

    if grep -q -e "Please don't .* before it unlocks!" -e "404 Not Found" "$input_file"
    then
        echo "Puzzle for day ${day} not accessible!"
        rm "$input_file"
        exit
    else
        touch $example_file
        echo "Please fill the example file ${example_file}"
        echo "Check the input file ${input_file}"
    fi
fi


##############################
# Create python template for solution
if [ -f "$code_file" ]
then
    echo "Solution file $code_file already exists."
    exit
fi

echo "Creating solution file ${code_file}"

cat <<EOF >"${code_file}"
import pandas as pd
from wrapper import Wrapper

# ${daily_url}


class Solver(Wrapper):

    def __init__(self, day: int):
        super().__init__(day=day)
        self.parser = 
        self.input = super().load_input(example=False, show=False)
        self.example = super().load_input(example=True)

    def parse_custom(self, path):
        pass

    def task_1(self, input):
        pass

    def task_2(self, input):
        pass


solver = Solver(${day})

print('=' * 15)
print("Part 1 example:")
print(solver.task_1(solver.example))  # == solution
print("Part 1 solution:")
print(solver.task_1(solver.input))

print('=' * 15)
print("Part 2 example:")
print(solver.task_2(solver.example))  # == solution
print("Part 2 solution:")
print(solver.task_2(solver.input))
EOF