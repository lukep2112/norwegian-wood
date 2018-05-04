#  Implementing a Turing Machine Assembler

This project takes in a Turing Machine program (as described below) and a word and tests that word against the program's instructions. 

## Getting Started

This program takes in a .TM file that has a specific format. This format is shown below.

![alt text](https://i.imgur.com/RnR4I9A.jpg)

Every .TM file should have an initialization section that contains in order:

- States: **{states: q0,...,qn}** where each string is an alpha-numeric .

- Start state: **{start: q}** where q is in states.

- Accept state: **{accept: A}** where A is in states.

- Reject state: **{reject: R}** where R is in states and R != q,

- Input alphabet: **{alpha: a1,...,am}** where each a is any character besides '_' and all of a is in the Tape alphabet.

- Tape alphabet: **{tape-alpha: t1,...,tm,_}** where each t is any character, the '_' represents a blank.

The remainder of the program should contain a list of transitions for the Turing Machine. These are not sequential (they can be run in any order). Below is a list of possible commands and their syntax:

- **rwRt q t t’ q’;** : in state **q** where the head is reading **t** off of the tape, write **t’**, transition to state
**q’** and move the head right.

- **rwLt q t t’ q’;** : in state **q** where the head is reading **t** off of the tape, write **t’**, transition to state
**q’** and move the head left.

- **rRl q t;** : in state **q** where the head is reading **t** off of the tape, write **t**, transition to state **q** and
move the head right.

- **rLl q t;** : in state **q** where the head is reading **t** off of the tape, write **t**, transition to state **q** and
move the head left.

- **rRt q t q’;** : in state **q** where the head is reading **t** off of the tape, write **t**, transition to state **q’**
and move the head right.

- **rLt q t q’;** : in state **q** where the head is reading **t** off of the tape, write **t**, transition to state **q’**
and move the head left.

All lines should be ended with a ';'

Comments can be denoted with '--' and these are ignored by the parser.


### Prerequisites

The latest version of python2.This program was tested on 2.7.14. 

## Running the tests
![alt text](https://i.imgur.com/MrnQzwz.png?1)

To run the program in the command line with your directory set to the program location, simply type the command: `python project2.py`.

The program will then prompt the user for the location to the .TM file

If the file is formatted correctly, the program will then prompt the user to enter a word. If the file is not formatted correctly, there will be a message with a potential fix. 

Once the word is entered the program will then print snapshots of the machine displaying the current head location and the tape.

![alt text](https://i.imgur.com/DefUnAy.jpg)

## Built With

* [Python2](https://www.python.org/) - The programming language used

## Author

**Luke Peterson**

## Contributor

**Harley Eades III** - *.TM file formatting descriptions*
