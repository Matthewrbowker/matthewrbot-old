def pages(cat,scat,sscat,subject):
    switch(cat):
        case 'aas':
            return "User:Matthewrbot/testbed1";
            break
        default:
            return -1;
def section(cat,scat,sscat,subject):
    if cat == 'aas':
        return "1";
    else:
        return -1;
