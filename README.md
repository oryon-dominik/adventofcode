# My solutions for [adventofcode](https://adventofcode.com/)

Mostly written in the [python](https://www.python.org/) language.  

I love adventofcode (an 'Advent calendar of small programming puzzles'),
it's a great idea to practice your skills and intuition in
programming and a great place to learn about algorithms and principles in
computer science. Especially for a lateral entrant to IT like me.  

All kudos go to the creator [Eric Wastl](@ericwast).  

I started 2018 with some more or less naive approaches.  
Older days were added later, when I found some time to enjoy puzzling.  

The solutions are not complete, due to lack of time ;-)  
Some puzzles are solved kinda sloppy. Maybe you can see progress over time though.  

Enjoy.


## Python

Install dependencies with poetry (`poetry install`) and run inside the year's
directory and the virtual environment (`poetry shell`) -> `python <day>.py`.

## Rust

Add a new `bin` entry for every day.

    [[bin]]
    name = "2022-day1"
    path = "2022/01.rs"

Install dependencies with `cargo install --path .`. Run with `cargo run --bin 2022-day1`.
