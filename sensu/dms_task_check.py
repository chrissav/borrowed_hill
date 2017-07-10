import argparse
import sys
import boto3

WARNING = 1
CRITICAL = 2

def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--task-name", action="store", type=str, required=True)

    args = parser.parse_args()

    client = boto3.client('dms', region_name='us-west-2')

    response = client.describe_replication_tasks(Filters=[{'Name': 'replication-task-id',
                                                           'Values': [args.task_name]}])

    if response['ReplicationTasks'][0]['Status'] == 'failed':
        print 'CRITICAL: task {} has failed'.format(args.task_name)
        exit(CRITICAL)

    tables_errored = response['ReplicationTasks'][0]['ReplicationTaskStats']['TablesErrored']

    if tables_errored:
        print 'WARNING: task {} has {} tables that errored'.format(args.task_name, tables_errored)
        exit(WARNING)

    print 'OK: task {} is running'.format(args.task_name)

if __name__ == '__main__':
    main()