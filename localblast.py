#load libraries
import os
import sys
import csv
import glob
import urllib2
import subprocess

#create a function which blasts a fasta sequence its fed and outputs the accession number and FPKM score if there is a match found or a blank line if there isn't
def blast_sequence(sequence):
    #Output the sequence to a temporary file to blast
    with open("sequence.fasta", "w") as fasta_sequence:
        fasta_sequence.write(">%s" % sequence)

    #Create a comamnd for blast to output to the command line
    command = "blastn -db Database/BtVrDb -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out "
    #Output command to command line
    subprocess.call(command, shell=True)

    #Read output file and retieve Accession number and FPKM
    lines = open("sequence.out").readlines()
    if lines:
        lines = lines[0].replace("\t", "|").split("|")
        gene_gi = lines[2]
        accession_number = lines[4]
        label, fpkm_value = sequence.split("\n")[0].split()[:]

        #Remove temporary files
        subprocess.call("rm -f sequence.fasta sequence.out", shell=True)
        #return FPKM value and accession number
        return [accession_number, fpkm_value]

    return ["", ""]


#Start main
if __name__ == '__main__':
    #Read FASTA files and fix header line format
    for fasta in glob.glob(os.path.join("Upload", "*.fasta")):
        #Skip fixed file
        if "_fixed.fasta" in fasta:
            continue

        #Split the name of the file so _fixed can be added to recognise fixed files
        basename, ext = os.path.splitext(fasta)
        with open(basename + "_fixed" + ext, "wb") as fasta_fixed:
            #Read content of original FASTA file
            for line in open(fasta):
                #Replace "_" by "-"
                line = line.replace("_", "-")

                #Replace ";" by " "
                line = line.replace(";", " ")

                #Insert '>'
                if "-" in line:
                    line = ">%s" % line

                #Write fixed text to new file ends with "_fixed"
                fasta_fixed.write(line)

    #BLAST fasta files and find gene
    for fasta in glob.glob(os.path.join("Upload", "*_fixed.fasta")):
        #Open CSV file to write results
        report = fasta.replace("_fixed.fasta", ".csv")
        with open(report, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Accession", "FPKM"])
            sequence = ""
            
            #Blast sequences one by one
            for line in open(fasta):
                if line.startswith('>') and sequence.startswith('>'):
                        #Run blast
                        row = blast_sequence(sequence)
                        #Save row
                        writer.writerow(row)
                        #Start new sequence
                        sequence = line
                else:
                    sequence += "%s\n" % line

            #If the last sequence is not empty
            if sequence and sequence.startswith('>'):
                #Run blast
                row = blast_sequence(sequence)
                #Save row
                writer.writerow(row)
