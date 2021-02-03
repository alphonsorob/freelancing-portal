import math, random

def getFinalList(N, n, input_tuple, pc1, pc2, pc3):
    i1, i2, i3 = input_tuple
    f1 = []
    f2 = []
    f3 = []
    
    pc1 = pc1 / (pc1+pc2+pc3)
    pc2 = pc2 / (pc1+pc2+pc3)
    pc3 = pc3 / (pc1+pc2+pc3)
    
    ceil1 = math.ceil(N*pc1)
    ceil2 = math.ceil(N*pc2)
    ceil3 = N-ceil1-ceil2

    if (len(i1) >= ceil1):
        #fill bucket 1 to the brim with only i1 elements
        f1 += i1[:ceil1]
        #f1 is full now with only i1 elements, i2 and i3 are untouched
        #now fill f2 (and f3) with i2 and i3 elems
        if (len(i2) >= ceil2):
            #fill f2 to the brim with only i2 elements
            f2 += i2[:ceil2]
            #f2 also is full now with only i2 elements, i3 is untouched
            #now fill f3 with i3 elements
            if (len(i3) >= ceil3):
                #fill f3 to the brim with i3 elems
                f3 += i3[:ceil3]
            else:
                #fill as many as are available
                f3 += i3
        
        else:
            #fill as many i2 elems as available
            f2 += i2
            #and fill remaining space in f2 with same no of initial i3 elements, (if also available)
            rem2 = ceil2-len(f2)
            if (len(i3) >= rem2):
                #fill remaining space in f2 with i3 elems
                f2.extend(i3[:rem2])
                #now f2 also is full
                #now move to f3 and fill with remaining i3 elems
                f3 += i3[rem2:ceil3]
            else:
                #fill as many i3 elems as availabe
                f2.extend(i3)
                
                
    else:
        #fill bucket 1 with as many i1 elems as available
        f1 += i1
        #fill remainng space in bucket 1 with b2 and b3 elements with their respective proportion, f1.append...(from i2 and/or i3)
        pcn2 = pc2_new = pc2 / (pc2+pc3)
        pcn3 = pc3_new = pc3 / (pc2+pc3)
        rem1 = ceil1-len(i1)  
        ceiln2 = ceil2_new = math.ceil(pcn2*rem1)
        ceiln3 = rem1-ceiln2

        if (len(i2) >= ceiln2):
            f1.extend(i2[:ceiln2])
            if (len(i3) >= ceiln3):
                f1.extend(i3[:ceiln3])
                if (len(i2[ceiln2:]) >= ceil2):
                    f2.extend(i2[ceiln2:ceiln2+ceil2])
                    if (len(i3[ceiln3:]) >= ceil3):
                        f3.extend(i3[ceiln3:ceiln3+ceil3])
                    else:
                        f3.extend(i3[ceiln3:])
                else:
                    f2.extend(i2[ceiln2:])
                    rem2 = ceil2-len(f2)
                    if (len(i3[ceiln3:]) >= rem2):
                        f2.extend(i3[ceiln3:ceiln3+rem2])
                        if (len(i3[ceiln3+rem2:]) >= ceil3):
                            f3.extend(i3[ceiln3+rem2:ceiln3+rem2+ceil3])
                        else:
                            f3.extend(i3[ceiln3+rem2:])
                    else:
                        f2.extend(i3[ceiln3:])
            else:
                f1.extend(i3)
                if (len(i2[ceiln2:]) >= ceil2):
                    f2.extend(i2[ceiln2:ceiln2+ceil2])
                else:
                    f2.extend(i2[ceiln2:])
        else:
            f1.extend(i2)
            if len(i3) >= (ceiln2-len(i2)):
                f1.extend(i3[:ceiln2-len(i2)])
                if (len(i3[ceiln2-len(i2):]) >= ceiln3):
                    f1.extend(i3[ceiln2-len(i2):ceiln2-len(i2)+ceiln3])
                    if (len(i3[ceiln2-len(i2)+ceiln3:]) >= ceil2):
                        f2.extend(i3[ceiln2-len(i2)+ceiln3:ceiln2-len(i2)+ceiln3+ceil2])
                        if (len(i3[ceiln2-len(i2)+ceiln3+ceil2:]) >= ceil3):
                            f3.extend(i3[ceiln2-len(i2)+ceiln3+ceil2:ceiln2-len(i2)+ceiln3+ceil2+ceil3])
                        else:
                            f3.extend(i3[ceiln2-len(i2)+ceiln3+ceil2:])
                    else:
                        f2.extend(i3[ceiln2-len(i2)+ceiln3:])
                else:
                    f1.extend(i3[ceiln2-len(i2):])
            else:
                f1.extend(i3[:])

        
    #f = f1 + f2 + f3
    
    #print('f1: ',f1)
    #print('f2: ',f2)
    #print('f3:', f3)
    f = []
    roof1 = math.ceil((len(f1)/N)*n)
    roof2 = math.ceil((len(f2)/N)*n)
    roof3 = n-roof1-roof2

    pages = math.ceil(N/n)

    for page in range(pages):
        temp = f1[:roof1] + f2[:roof2] + f3[:roof3]
        #print('              original: ',temp)
        random.shuffle(temp)
        #print('              Shuffled: ',temp)
        f = f + temp
        f1 = f1[roof1:]
        f2 = f2[roof2:]
        f3 = f3[roof3:]
    
    return f
    
    
    