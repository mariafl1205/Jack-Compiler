// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/SimpleFunction/SimpleFunctionVME.tst

load Main.vm,
output-file Main.out,
compare-to Main.cmp,
output-list RAM[16384]%D1.8.1 RAM[16416]%D1.8.1 RAM[16448]%D1.8.1 
            RAM[16480]%D1.8.1 RAM[16512]%D1.8.1 RAM[16544]%D1.8.1
            RAM[16576]%D1.8.1 RAM[16608]%D1.8.1 RAM[16640]%D1.8.1
            RAM[16672]%D1.8.1 RAM[16704]%D1.8.1 RAM[16736]%D1.8.1
            RAM[16768]%D1.8.1 RAM[16800]%D1.8.1 RAM[16385]%D1.8.1;


repeat 100 {
  vmstep;
}

output;
