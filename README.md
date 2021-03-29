# PodPlot
![](podplot.cov.png)

![](podplot.perc.png)


## Dependencies

- Python3
- Matplotlib

## Usage

1. Make a fasta/fastq index with [samtools](https://github.com/samtools/samtools).
2. List the index files:

```
$ cat fai.fofn
reads.1.fasta.fai	Shadowfax
reads.2.fasta.fai	Snowmane	
reads.3.fasta.fai	Bill
```

4. `python3 podplot.py fai.fofn` or `python3 podplot.py -g 1500000000 fai.fofn`
