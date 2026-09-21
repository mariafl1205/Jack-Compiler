// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/SimpleFunction/SimpleFunctionVME.tst

load Main.vm,
output-file Main.out,
compare-to Main.cmp,
output-list RAM[268]%D1.8.1;

repeat 20 {
  vmstep;
}

// Initialize b to 2048 and length to 5
// Initialize array @ 248 too. 
set RAM[266] 3000,
set RAM[267] 5,
set RAM[3000] 427,
set RAM[3001] 125,
set RAM[3002] 647,
set RAM[3003] 356,
set RAM[3004] 270,

repeat 700 {
  vmstep;
}

output;
