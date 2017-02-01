1. Install BLAST executables.
    a) Download and extract files for your OS from
       ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
    b) Add your BLAST executables to PATH environment variable (NOT REQUIRED WHEN INSTALL USING DMG FILE ON MAC)
	export PATH=/usr/local/ncbi/blast/bin:$PATH

2. Install database (FOR LOCAL BLAST ONLY)
update_blastdb.pl nr —> Blast fasta files locally against nr database


3. Run program.

Local BLAST:
python ./blast.py

Remote BLAST:
python ./blast.py -remote

The program writes CSV files into FASTA data directory.
