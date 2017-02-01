import os
import sys
import csv
import glob
import urllib2
import subprocess


# Start program
if __name__ == '__main__':

    # Check if one need to use blast databases remotelly or not
    remote_arg = ""
    if len(sys.argv) > 1 and sys.argv[1] == "-remote":
        remote_arg = "-remote"

    # Input species, delimeter is comma or space
    #species = []
    #while not species:
    #    species = raw_input("Enter species: ")
    #    species = species.replace(",", " ").split()

    # Input data directory
    data_directory = ""
    while not data_directory:
        data_directory = raw_input("Enter data directory path: ")
        if not (data_directory and os.path.exists(data_directory)):
            print "Error: wrong data directory path"
            data_directory = ""

    # Read FASTA files and fix header line format
    for fasta in glob.glob(os.path.join(data_directory, "*.fasta")):
        # Skip fixed file
        if "_fixed.fasta" in fasta:
            continue

        print "Fixing file %s ..." % fasta
        basename, ext = os.path.splitext(fasta)
        with open(basename + "_fixed" + ext, "wb") as fasta_fixed:
            # Read content of original FASTA file
            for line in open(fasta):
                # Replace "_" by "-"
                line = line.replace("_", "-")

                # Replace ";" by " "
                line = line.replace(";", " ")

                # Insert '>'
                if "-" in line:
                    line = ">%s" % line

                # Write fixed text to new file ends with "_fixed"
                fasta_fixed.write(line)

    # BLAST fasta files and find gene
    for fasta in glob.glob(os.path.join(data_directory, "*_fixed.fasta")):
        print "Blast file %s ..." % fasta

        # Open CSV file to write results
        report = fasta.replace("_fixed.fasta", ".csv")
        with open(report, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Accession Number", "Gene Symbol", "FPKM Value"])

            # Iterate via sequences
            for sequence in open(fasta).read().split('>'):
                # Skip emtpy lines
                if not sequence:
                    continue

                # Write sequence into file to blast
                with open("sequence.fasta", "w") as fasta_sequence:
                    fasta_sequence.write(">%s" % sequence)

                # Blast sequence
                command = "blastn -db nr -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out " + remote_arg
                subprocess.call(command, shell=True)

                # Get GI, accession number and FPKM value
                line = open("sequence.out").readlines()
                if line:

                    line = line[0].replace("\t", "|").split("|")
                    gene_gi = line[2]
                    accession_number = line[4]
                    fpkm_value = sequence.split("\n")[0].split()[-1]

                    # Find gene name
                    url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=%s&db=nuccore&report=genbank&retmode=text" % gene_gi
                    data = urllib2.urlopen(url).readlines()
                    i = 0
                    for j, t in enumerate(data):
                        t = t.strip()
                        if t.startswith("gene"):
                            i = j + 1
                            break
                    gene_name = data[i].strip().replace("/gene=", "").replace('"', "")

                    # Save data
                    writer.writerow([accession_number, gene_name, fpkm_value])

                    # Remove temporary files
                    subprocess.call("rm -f sequence.fasta sequence.out", shell=True)

