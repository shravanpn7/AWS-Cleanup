__author__ = 'spapanaidu'
from boto import ec2

conn = ec2.connect_to_region('us-east-1')
gp2 = 0
magnetic = 0
total = 0
io1 = 0

vols = conn.get_all_volumes(filters={'status': 'available'})
for vol in vols:
    print 'checking vol:', vol.id, vol.status, 'type:', vol.type
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
##
