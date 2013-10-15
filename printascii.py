if __name__ == "__main__":
    print "SYMBOL"
    print "WINDOWS's lame extended ASCII (CP850)"
    print "UNICODE"
    S = ""
    for y in range(16):
        for x in range(16):
            if chr(y*16+x) != "\r" and chr(y*16+x) != "\n": S += chr(y*16+x)+"    "
            else: S += "   "
        S = S[:-1] + "\n"
        for x in range(16):
            S += str(y*16+x)+" "*(5-len(str(y*16+x)))
        S = S[:-1] + "\n"
        for x in range(16):
            S += str(ord(uchr(y*16+x)))+" "*(5-len(str(ord(uchr(y*16+x)))))
        S = S[:-1] + "\n\n"
    print S
