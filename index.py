import json
from datetime import datetime
import boto3
import collections

print('Loading function')

ec2 = boto3.client('ec2')

def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def findDate(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result.strftime('%m/%d/%Y') # %m/%d/%Y | %H:%M:%S
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result.strftime('%m/%d/%Y') # %m/%d/%Y | %H:%M:%S

def handler(event, context):

    # Variables
    VOLUMEID = event['volumeId'] # volumeId
    DESCRIPTION = event['description'] + ' ' + datetime.now().strftime("%c") + ' UTC'
    THRESHOLD = event['retentionDays']
    if not isinstance( THRESHOLD, int ):
        print "Converting threshold to int..."
        THRESHOLD = int(THRESHOLD)

    response = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id','Values': [VOLUMEID,]},])

    recentSnapshots_id = list(find('SnapshotId', response))
    # print recentSnapshots_id

    recentSnapshots_date = list(findDate('StartTime', response))
    # print recentSnapshots_date

    snapshotDict = dict(zip(recentSnapshots_id, recentSnapshots_date))

    # Check if there is no snapshot yet, usually first time
    if not snapshotDict:
        print "No snapshot dectected, creating initial snapshot..."
        createSnapshot = ec2.create_snapshot(
            DryRun=False,
            VolumeId=VOLUMEID,
            Description=DESCRIPTION
        )
    else:
        oldestSnap = min(snapshotDict, key=snapshotDict.get)
        # print oldestSnap
        oldestDate = datetime.strptime(min(snapshotDict.values()), "%m/%d/%Y")
        # print oldestDate

        now = datetime.strptime(datetime.now().strftime('%m/%d/%Y'), "%m/%d/%Y")

        diff = now - oldestDate

        if (diff.days >= THRESHOLD):
            print "delete this " + oldestSnap + " and create a new one"
            # Delete 7 days old snapshot
            deleteSnapshot = ec2.delete_snapshot(
                DryRun=False,
                SnapshotId=oldestSnap
            )
            # Add new snapshot
            createSnapshot = ec2.create_snapshot(
                DryRun=False,
                VolumeId=VOLUMEID,
                Description=DESCRIPTION
            )
        else:
            print "keep creating new snapshot"
            createSnapshot = ec2.create_snapshot(
                DryRun=False,
                VolumeId=VOLUMEID,
                Description=DESCRIPTION
            )

    return ("Snapshot created on " + datetime.now().strftime("%H:%M:%S"))
