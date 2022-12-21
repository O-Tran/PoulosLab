def main(**kwargs):
    #infile, outfile,  a= 0.18, b= 0.5, g= 0 (5 value)  #default unless stated otherwise
    """
    Purpose: Convert MMPBSA Free energy data results to get LIE for NOS proteins

    Usage: python mmpbsa2lie.py -i [infile] -ip [--proteinfile] -o [file.out]
    [[optional]] -a [alpha value] -b [beta value] -g [gamma value]
     
    By: Oanh TN Tran
    Version: 1.1, started: Sept 28, 2021

------------------- DESCRIPTION --------------------------------------------------------------

    Get energy from input file.
    Parameters
    ----------
    inputfile : str
    -i  : str
        input normal mmgbsa file
    -ip : str
        Input mmgbsa file with protein charges zero in receptor
        
    -o outputfile: str
        gives Dele, Dvdw, DGlie values in a given directory

    -a : float
        Alpha values, Alpha = 0.18 unless stated otherwise
    -b : float
        Beta values, Beta =0.5 unless stated otherwise
    -g : float
        Gamma values, gamma = 0 unless stated otherwise
    
    Returns
    -------
    -o outputfile: str
        gives Dele, Dvdw, DGlie values in a doc
    
    Dglie value ? ## not sure how to implement this yet ## 
    """
    
    def makedict (infile):
    
        #reading input file, identifying type of data (GB or PB), and get specific value
        with open (infile, 'r') as mmpbsafile:
            mmpbsaread = mmpbsafile.readlines()

        componentname = ["COMPLEX", "RECEPTOR", "LIGAND", "DELTA"]
        MMdict = {}

        ##checking if the file has listed qualities:
        for i in range(len(mmpbsaread)):
            if componentname[0] in mmpbsaread[i]:
                titleline=i+4
            elif componentname[3] in mmpbsaread[i]:
                deltaline=i+4
                break
        #make empty dictionary
        for i in range(len(componentname)):
            MMdict[componentname[i]] = {}

        #make dictionary of the complex, receptor, ligand
        for i in range(titleline, titleline+9):
            splitrow = mmpbsaread[i].split()
            MMdict[componentname[0]][splitrow[0]] = float(splitrow[1])
            MMdict[componentname[1]][splitrow[0]] = float(splitrow[3])
            MMdict[componentname[2]][splitrow[0]] = float(splitrow[5])

        #make dictionary of the delta
        for i in range(deltaline,deltaline+9): #till the end
            splitrow = mmpbsaread[i].split()
            MMdict[componentname[3]][splitrow[0]] = splitrow[1]

        #ensure closing the file
        mmpbsafile.close()

        return MMdict
    
    #Make a dictionary of the two files
    MMdict = makedict(args.infile)
    protein_0 = makedict(args.proteinfile)
    
    #Identify important object:
    Ulig_protBound = MMdict['COMPLEX']['ELE'] - MMdict['RECEPTOR']['ELE']
    Ulig_watBound =  protein_0['RECEPTOR']['GB']
    Ulig_watFree = MMdict['LIGAND']['GB']

    Dele = Ulig_protBound + 2*Ulig_watBound - 2*Ulig_watFree
    
    Dvdw = MMdict['COMPLEX']['VDW'] - MMdict['RECEPTOR']['VDW']
    
    
    DGlie = args.beta*(Dele) + args.alpha*(Dvdw) + args.gamma

    #setting up the output file, write the begining part of the mmgbsaread file up until GENERALIZED BORN
    with open (args.outfile, 'w') as outputfile:
        LIEresult = """

Generated with mmpbsa2lie.py
-------------------------------------------------------------------------------

The LIE value for %s is:
Dele = %0.2f
Dvdw = %0.2f
DGLie = %0.2f

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
""" %(args.infile, Dele, Dvdw, DGlie) ## fix the % to assigment
    
        outputfile.write(LIEresult)
    
    print("Done with %s" %args.infile)
    
    #closing read/write file
    outputfile.close()
        
    return DGlie  #What do i put in the output file How do I just get return value

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
            help="Input bound MMPBSA file")
    parser.add_argument("-ip", "--proteinfile",
            help="Input ligand-free MMPBSA file")
    parser.add_argument("-o", "--outfile",
            help="Output LIE file")
    parser.add_argument("-a", "--alpha",  nargs='?', const=1, default=0.18, type=float,
            help="input alpha value, default is 0.18")
    parser.add_argument("-b", "--beta",  nargs='?', const=1, default=0.5, type=float,
            help="input beta value, default is 0.5")
    parser.add_argument("-g", "--gamma",  nargs='?', const=1, default=0, type=float,
            help="input gamma value, default is 0")

    args = parser.parse_args()
    opt = vars(args)
    
    #1main(args.infile, args.outfile) # might need to add a, b, g value
    
    main(**opt)
