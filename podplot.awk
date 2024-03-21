#!/usr/bin/
# Author Gaurav Sablok
# Universitat Potsdam
# Date 2024-3-21
# invoking awk, a bit of the iteration and making a openGLC for the visualization by invoking a stdio. 
podplot (){
  awk '/^>/ {printf("\n%s\n",$0);next; } \
            { printf("%s",$0);} END {printf("\n");}' input.fasta > read.fasta
  declare -a sortheader=()
  for i in $(cat read.fasta | awk '/^>/ {print $1}' | sed "s/>//g");
  do 
     sortheader+=("${i}")
  done
  declare -a stringsort=()
  for i in $(cat read.fasta | awk '!/^>/ { print $1 }');
  do 
     stringsort+=("${i}")
  done
  declare -a length=()
  for i in $(cat read.fasta | awk '!/^>/ { print $1 }'); 
  do 
    length+=$(awk print $length($i))
  done
 
}
