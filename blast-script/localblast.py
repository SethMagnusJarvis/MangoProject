import os
import sys
import csv
import glob
import urllib2
import subprocess

def blast_sequence(sequence):
    # Write sequence into file to blast
    with open("sequence.fasta", "w") as fasta_sequence:
        fasta_sequence.write(">%s" % sequence)

    # Blast sequence
    command = "blastn -db Database/BtVrDb -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out "
    subprocess.call(command, shell=True)

    # Get GI, accession number and FPKM value
    lines = open("sequence.out").readlines()
    if lines:
        lines = lines[0].replace("\t", "|").split("|")
        gene_gi = lines[2]
        accession_number = lines[4]
        label, fpkm_value = sequence.split("\n")[0].split()[:]

        # Remove temporary files
        subprocess.call("rm -f sequence.fasta sequence.out", shell=True)

        return [accession_number, fpkm_value]

    return ["", "", "", ""]


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

    # Read FASTA files and fix header line format
    for fasta in glob.glob(os.path.join("test_fasta_results", "*.fasta")):
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
    for fasta in glob.glob(os.path.join("test_fasta_results", "*_fixed.fasta")):
        print "Blast file %s ..." % fasta

        # Open CSV file to write results
        report = fasta.replace("_fixed.fasta", ".csv")
        with open(report, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Accession Number", "Transcript Id", "FPKM Value"])

            # Iterate via sequences
            sequence = ""

            for line in open(fasta):
                if line.startswith('>') and sequence.startswith('>'):
                        # Run blast
                        row = blast_sequence(sequence)
                        # Save row
                        writer.writerow(row)
                        # Start new sequence
                        sequence = line
                else:
                    sequence += "%s\n" % line

            # If the last sequence is not empty
            if sequence and sequence.startswith('>'):
                # Run blast
                row = blast_sequence(sequence)
                # Save row
                writer.writerow(row)
