# Python 2.7 code
file_path = './example.txt'

# Open the file for reading
file = open(file_path, 'r')

# Initialize a list to hold lines
lines = []

# Read the contents line by line
for line in file:
    # Strip whitespace and append to the list
    lines.append(line.strip())

# Print the total number of lines
print "Total lines:", len(lines)

# Print each line with its line number
for index, line in enumerate(lines):
    print "Line {}: {}".format(index + 1, line)

# Close the file
file.close()