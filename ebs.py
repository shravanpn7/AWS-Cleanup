__author__ = 'spapanaidu'
import sys

from boto import ec2

conn = ec2.connect_to_region('us-east-1')
gp2 = 0
magnetic = 0
total = 0
io1 = 0
volToDelete = []

vols = conn.get_all_volumes(filters={'status': 'available'})

if len(sys.argv) > 1 and sys.argv[1] == 'delete':
    deleteVols = True
else:
    deleteVols = False

for vol in vols:
    print 'checking vol:', vol.id, vol.status, 'type:', vol.type
    volToDelete.append(str(vol.id))
    total = total + vol.size
    if vol.type == 'gp2':
        gp2 = gp2 + vol.size
    elif vol.type == 'standard':
        magnetic = magnetic + vol.size
    elif vol.type == 'io1':
        io1 = io1 + vol.size

print 'total volume size:', total, 'GB'
print 'gp2 volume size:', gp2, 'GB'
print 'magnetic volume size:', magnetic, 'GB'
print 'io volume size:', io1, 'GB'
#
if deleteVols == True:
    deleteConfirm = raw_input("Are you sure you want to delete the above orphan volumes [y/n]? ")
    if deleteConfirm == 'y':
        for vols in volToDelete:
            print "Deleting " + vols
            conn.delete_volume(vols)

conn.close()
