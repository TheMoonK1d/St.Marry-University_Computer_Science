import sys
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Erteb token v.0.1")
outfile = open('public_record.txt', 'a')
outfile.write('Session' + str(now))
outfile.write("date and time =" + str(dt_string))
def checksum8(name):
   sum = 0

   for c in name.upper():
       sum += ord(c)

   return sum & 0xff

def checkByte(id_High, id_Low, iters):
    cb = (id_High + id_Low) & 0xff
    if cb == 0:
        cb = 1
    if iters == 0:
        iters = 1

    for _ in range(iters):
        tmp = (cb << 1) & 0xff
        tmp ^= cb
        tmp = (tmp << 1) & 0xff
        tmp ^= cb
        tmp = (tmp << 2) & 0xff
        tmp ^= cb
        cb = (cb << 1) & 0xff
        if tmp & 0x80:
            cb |= 0x01

    return cb

def block_id(id_High, checkByte, id_Low):
    accountBits = id_High << 16 | checkByte << 8 | id_Low
    account = []
    for _ in range(4):
        second = accountBits & 0x07
        accountBits >>= 3
        first = accountBits & 0x07
        accountBits >>= 3
        account.append(first)
        account.append(second)

    return ''.join(map(str, account))
 
if len(sys.argv) < 3:
    print("Error on the blockchain")
    print("Usage: %s Enter your Name and a private key" % sys.argv[0])
    print("..." + '\n')
    outfile.write("# Session started by unknown key" + '\n')
    outfile.write("> This block is recorded in log but will be ignored!"+ '\n')
    outfile.write("# Session ended on unknown"+ '\n')
    outfile.write(" "+ '\n')
    print("..." + '\n')
    outfile.close()
    sys.exit(1)

name = sys.argv[1][0:18]
id_High = (int(sys.argv[2][0]) - 0) * 16 + int(sys.argv[2][1]) - 0
id_Low = (int(sys.argv[2][2]) - 0) * 16 + int(sys.argv[2][3]) - 0

iters = checksum8(name)
cb = checkByte(id_High, id_Low, iters)


print("Block ID = " + block_id(id_High, cb, id_Low))
print("Found on block "+ str(id_High))
print("Port number " + str(id_Low))

outfile.write("Session started on "+ str(id_Low))
outfile.write(name + block_id(id_High, cb, id_Low))
outfile.write("Session ended on "+ str(id_Low))
outfile.close()
print("Sync failed!")
print("Could not join the block...server not found or may be disconnected")