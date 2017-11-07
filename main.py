'''
    The arguments must given in order -> python main.py [pcap-file(without .pacp)] outputsFiles
    outputFiles ->
        1) csv
        2) byte
        3) unhex // First generates the hex file in the 'HexFiles' Directory, then unhexlify it to unhex file in 'UnHexFiles' Directory
        4) ip

    example:
        1 ) python main.py iperf-mptcp-0-0 csv byte unhex
            This will generate all of the given files
        2 ) python main.py iperf-mptcp-0-0 byte
            This will generate only byte File

        ** if you don't give output Files -> All of the outputs will be generated
        example :
            python main.py iperf-mptcp-0-0
'''


import binascii, os, sys, re

def generateCSV(pcapFile):
    print("Going to make " + pcapFile + " csv File\n\n")
    os.system("tshark -r " + "pcaps/" + pcapFile +".pcap -T fields -e _ws.col.Info > "+ "csvs/" + pcapFile +".csv")
    print ("csv file created\n\n*******************\n\n")

def generateBytes(pcapFile):
    print("Going to make " + pcapFile + " byte File\n\n")
    os.system("tshark -r " + "pcaps/" + pcapFile + ".pcap -x >" + "Bytes/" + pcapFile)
    print("byte file Created\n\n*******************\n\n")

def generateHEX(pcapFile):
    print("Going to make " + pcapFile + " hex File\n\n")
    os.system("tshark -r " + "pcaps/" + pcapFile + ".pcap -T fields -e data >" + "HexFiles/" + pcapFile + "-hex")
    print("hex file Created\n\n*******************\n\n")

def generateUnHex(pcapFile):
    print("Hex File should be generated first \n\n")
    generateHEX(pcapFile)
    print("Going to make " + pcapFile + " unhex File\n\n")
    lines = filter(None, (line.rstrip() for line in open('HexFiles/' +  pcapFile + "-hex", 'r')))
    finalLines = []
    for line in lines:
        finalLines.append(binascii.unhexlify(line))
    #re.sub("[^0-9]", "", finalLines[1])

    myUnHexFile = open('UnHexFiles/' + pcapFile + "-unhex", 'w')


    for finalLine in finalLines:
        tmp = ""
        flag = False
        for inMyLine in finalLine:
            if(inMyLine.isdigit() or inMyLine.isalpha()):
                tmp += inMyLine
                if(not flag):
                    flag = True
            if((inMyLine == " " or inMyLine == ".") and flag):
                tmp += inMyLine
            finalLine = tmp
        myUnHexFile.write(finalLine)
        myUnHexFile.write("\n")
    myUnHexFile.close()
    print("unhex file Created\n\n*******************\n\n")

def generateIPs(pcapFile):
    print("Going to make " + pcapFile + " IPs File\n\n")
    os.system("tshark -r " + "pcaps/" + pcapFile + ".pcap -T fields -e ip.dst -e ip.src >" + "IPs/" + pcapFile + "-ips")
    print("IPs file Created\n\n*******************\n\n")

def main():

    myArgs = sys.argv
    if(len(myArgs[1:]) == 0):
        myFlag = False
        print("You did not give any pcap file!")
    else:
        pcapFile = myArgs[1]
        myFlag = True
        print("pcap file -> " + pcapFile + " Captured\n\n*******************")

    if(myFlag):
        outputArgs = myArgs[2:]
        if(len(outputArgs) == 0):
            print("Going to Generate all the output files !\n\n*******************\n\n")
            generateCSV(pcapFile)
            generateBytes(pcapFile)
            generateUnHex(pcapFile)
            generateIPs(pcapFile)

        else:
            for outputArg in outputArgs:
                if(outputArg == "csv"):
                    generateCSV(pcapFile)

                elif(outputArg == "byte"):
                    generateBytes(pcapFile)

                elif(outputArg == "unhex"):
                    generateUnHex(pcapFile)

                elif(outputArg == "ip"):
                    generateIPs(pcapFile)

                else:
                    print("Given Argument is not correct")


if __name__ == "__main__":
    main()
