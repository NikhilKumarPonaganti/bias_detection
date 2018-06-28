import sys

def check_one_word(line):
	line = line.split('\t')
    # index 6 gives the biased substring
    # index 7 gives the complete string
#    if line[6] in line[7]:
#        if len(line[6].strip().split())!=1:
#            return(True)
#    return(False)
 
	if len(line[6].strip().split())!=1:
		return(True)
	return(False)

def check_npov(line):
    line = line.split('\t')
    # index 2 tells presence of npov tag
    if line[2].strip() != 'true':
        return(True)
    return(False)

def check_five_words(line):
	line = line.split('\t')
	sentence = line[8].split()
 
	if len(sentence)>5:
		return(True)
	return(False)

def main():
    try:
        src = sys.argv[1]
        dst = sys.argv[2]
    except:
        print('USAGE:\n    "python3 preprocess.py <source_address> <destination_address>"')
        exit(1)

    if sys==dst:
        print("ERROR: Source and destination arguments cannot refer to the same file")
        exit(1)

    with open(src, 'r') as src:
        with open(dst, 'w') as dst:
            for line in src:
                discard = False
                if not discard:        
                    discard = check_one_word(line)
                if not discard:
                    discard = check_npov(line)
                if not discard:
                    discard = check_five_words(line)
                if not discard:
                    dst.writelines(line)
    exit(0)

if __name__=="__main__":
    main()
