import os
import glob

# Start program
if __name__ == '__main__':

    # Input species, delimeter is comma or space
    species = []
    while not species:
        species = raw_input("Enter species: ")
        species = species.replace(",", " ").split()

    # Input data directory
    data_directory = ""
    while not data_directory:
        data_directory = raw_input("Enter data directory path: ")
        if not (data_directory and os.path.exists(data_directory)):
            print "Error: wrong data directory path"
            data_directory = ""

    # Read FASTA files and fix header line format
    for fasta in glob.glob(os.path.join(data_directory, "*.fasta")):
        print "Fixing file %s ..." % fasta
        with open(fasta + "_fixed", "wb") as fasta_fixed:
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

