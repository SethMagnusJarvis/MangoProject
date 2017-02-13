import os
import sys
import csv
import glob
import urllib2
import subprocess

def blast_sequence(sequence, gbk):
    # Write sequence into file to blast
    with open("sequence.fasta", "w") as fasta_sequence:
        fasta_sequence.write(">%s" % sequence)

    # Blast sequence
    
    # Local or Remote blast against nr database with filtering using organism 
    #command = "blastn  -entrez_query 'Pteropus alecto[Organism] OR Hendra virus[Organism]' -db nr -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out " + remote_arg

    # Local or Remote blast against nr database
    command = "blastn  -db nr -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out " + remote_arg

    # Local blast: BatVirus
    #command = "blastn -db BatVirus -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out"

    # Local blast: Pteropus alecto
    #command = "blastn -db ptv -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out"
    
    subprocess.call(command, shell=True)

    # Get GI, accession number and FPKM value
    lines = open("sequence.out").readlines()
    if lines:
        lines = lines[0].replace("\t", "|").split("|")
        gene_gi = lines[2]
        accession_number = lines[4]
        label, fpkm_value = sequence.split("\n")[0].split()[:]
        transcript_id = label.split("-")[1]

        # Find gene name
        gene_name = ""
        if gbk:
            gene_name = gbk.get(accession_number, "")
        else:
            for report in ["genbank", "gbwithparts"]:
                url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=%s&db=nuccore&report=%s&retmode=text" % (gene_gi, report)
                data = urllib2.urlopen(url).readlines()
                i = 0
                for j, t in enumerate(data):
                    t = t.strip()
                    if t.startswith("gene"):
                        i = j + 1
                        break
                if i != 0:
                    gene_name = data[i].strip().replace("/gene=", "").replace('"', "")
                    break

        # Remove temporary files
        subprocess.call("rm -f sequence.fasta sequence.out", shell=True)

        return [accession_number, gene_name, transcript_id, fpkm_value]

    return ["", "", "", ""]


# Start program
if __name__ == '__main__':

    # Check if one need to use blast databases remotelly or not
    remote_arg = ""
    gbk_filename = ""
    if len(sys.argv) > 1 and sys.argv[1] == "-remote":
        remote_arg = "-remote"
    else:
        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                gbk_filename = arg

    # Input data directory
    data_directory = ""
    while not data_directory:
        data_directory = raw_input("Enter data directory path: ")
        if not (data_directory and os.path.exists(data_directory)):
            print "Error: wrong data directory path"
            data_directory = ""

    # Read gene names from gbk file
    gbk = {}
    if gbk_filename:
        print "Parsing %s..." % gbk_filename

        accession_number = ""
        gene_name = ""

        for line in open(gbk_filename):
            line = line.strip()

            if line.startswith("VERSION"):
                if accession_number and gene_name:
                    gbk[accession_number] = gene_name
                accession_number = line.split()[1]
                gene_name = ""
                continue

            if line.startswith("/gene=") and not gene_name:
                gene_name = line.replace("/gene=", "").replace('"', "")

        if accession_number and gene_name:
            gbk[accession_number] = gene_name

    # Input species, delimeter is comma or space
    #species = []
    #while not species:
    #    species = raw_input("Enter species: ")
    #    species = species.replace(",", " ").split()

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
            writer.writerow(["Accession Number", "Gene Symbol", "Transcript Id", "FPKM Value"])

            # Iterate via sequences
            sequence = ""

            for line in open(fasta):
                if line.startswith('>') and sequence.startswith('>'):
                        # Run blast
                        row = blast_sequence(sequence, gbk)
                        # Save row
                        writer.writerow(row)
                        # Start new sequence
                        sequence = line
                else:
                    sequence += "%s\n" % line

            # If the last sequence is not empty
            if sequence and sequence.startswith('>'):
                # Run blast
                row = blast_sequence(sequence, gbk)
                # Save row
                writer.writerow(row)
