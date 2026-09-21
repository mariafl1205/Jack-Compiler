load Main.vm,
output-file Main.out,
compare-to Main.cmp,
output-list RAM[266]%D1.8.1;

repeat 1000 {
  vmstep;
}

output;
