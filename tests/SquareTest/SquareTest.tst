load,
output-file Main.out,
compare-to Main.cmp,
output-list RAM[2050]%D1.8.1 RAM[2051]%D1.8.1 
            RAM[2054]%D1.8.1 RAM[2055]%D1.8.1 RAM[2056]%D1.8.1;

repeat 2000 {
  vmstep;
}

output;
