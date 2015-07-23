# https://gist.github.com/mjbommar/5070899

# Imports
import re
import sys

import boto


def main():
    '''
    Main method
    '''

    if len(sys.argv) > 1 and sys.argv[1] == 'delete':
        deleteSnapshots = True
    else:
        deleteSnapshots = False

    # Open connection to EC2
    ec2Connection = boto.connect_ec2()

    # Get the list of registered AMIs.
    imageIds, imageNames = zip(
        *[(image.id, image.name + ", " + image.description) for image in ec2Connection.get_all_images(owners=['self'])])
    imageNames = dict(zip(imageIds, imageNames))

    # Get list of snapshots and AMIs
    reAmi = re.compile('ami-[^ ]+')
    snapshots = []
    snapshotsToDelete = []
    snapshotsUnknown = []
    imageSnapshots = {}

    for snapshot in ec2Connection.get_all_snapshots(owner='self'):
        # Get id and image ID via regex.
        snapshotId = snapshot.id
        snapshotImageId = reAmi.findall(snapshot.description)
        if len(snapshotImageId) != 1:
            snapshotsUnknown.append(snapshotId)
        else:
            snapshotImageId = snapshotImageId[0]

        # Update lists
        snapshots.append(snapshotId)
        if snapshotImageId not in imageIds:
            snapshotsToDelete.append(snapshotId)
        else:
            if snapshotImageId in imageSnapshots:
                imageSnapshots[snapshotImageId].append(snapshotId)
            else:
                imageSnapshots[snapshotImageId] = [snapshotId]

    print "Mapped snapshots:"
    for image in sorted(imageSnapshots.keys()):
        print image + ": " + imageNames[image]
        for snapshot in imageSnapshots[image]:
            print "\t- " + snapshot

    print
    print "Orphans: " + ','.join(sorted(snapshotsToDelete))
    print
    print "Unknown: " + ','.join(sorted(snapshotsUnknown))

    if deleteSnapshots == True:
        deleteConfirm = raw_input("Are you sure you want to delete the above orphan snapshots [y/n]? ")
        if deleteConfirm == 'y':
            for snapshot in snapshotsToDelete:
                print 'Removing ' + snapshot + '...'
                ec2Connection.delete_snapshot(snapshot)

    # Close connection to EC2.
    ec2Connection.close()


if __name__ == "__main__":
    main()
