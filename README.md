#Welcome to my Carmichael number repo!

This repo is designed to reproduce and extend the research done here: "insert link to paper here".

This research was originally done between 2009-2011, and relies heavily on computation power. One of the reasons I have created this repo is to reproduce my original results on much newer hardware in a fraction of the original time. For example, it took a few months of computation time to generate the original results and I can reproduce those results in a couple of days using a Threadripper CPU or a small raspberry pi compute cluster (see below for specifics).

The original results were created with Matlab and Mathematica, when I was new to writing code. The code in this repo is written in Python and I am much better at writing code now!

##How to run the code in this repo

There are 2 main ways to run this code.

1) Use the CarmCalculator class, and run the code locally on one machine. This is mostly for demos, testing algorithm improvements, and benchmarks.

2) Use the CarmNodeCalculator class, and run the code on any number of machines as nodes which send data to a server node. See `CarmNodeCalculator_Setup_Guide.md` for instructions on how to set this up.

##How to use the CarmCalculator class

See `CarmCalculator_Instructions.md` and `carm_calculator_examples.py` for examples on how to use this class.

###TODO List
 - Add algorithms to compute 4-carmichael numbers
 - Use CUDA to compute carmichael numbers with one or more GPU's
