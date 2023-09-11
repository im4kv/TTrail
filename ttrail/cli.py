from wsgiref.validate import validator
import click
from ttrail.internals import events, analyze
import ttrail.utils as utils

@click.command()
@click.option('--start-time', 'start_time', default="15 min ago",callback=utils.validate_time, type=click.STRING,
              help='search start date, examples: "July 4, 2021 PST" , "21 July 2013 10:15 pm +0500" or human readables "1 hour ago", "in 2 days". Defaults to "1 hour ago". ')
@click.option('--end-time', 'end_time', default="now",callback=utils.validate_time, type=click.STRING,
              help='search end date, examples: "July 4, 2021 PST" , "21 July 2013 10:15 pm +0500" or human readables "1 hour ago", "now". Defaults to "now". ')
@click.option('--profile', 'aws_profile', default="default",callback=utils.validate_aws_profile, type=click.STRING,
              help='AWS Profile name to use. it will use "default" if nothing else is specified. ')
@click.option('--region', 'aws_region', type=click.STRING,
              help='it used in combination with AWS Profile option to specify the region for AWS client session.')
@click.option('--skip-service-events', 'skip_service_events',is_flag=True,
              help='A Display filter to skip events with the user identity of AWS service.')
@click.pass_context
def cli(ctx, start_time, end_time, aws_profile, aws_region, skip_service_events):
    cloudtrail = events.Cloudtrail(start_time= start_time, end_time= end_time, 
    filter= filter, source= None, aws_profile= aws_profile, aws_region= aws_region, skip_service_events = skip_service_events)
    cloudtrail.load_from_aws_event_history()
    if cloudtrail.events_df.empty:
        print('No events matched with the specified duration and filter')
        return
    treeview = analyze.Treeview(cloudtrail)
    treeview.generate()
    print(treeview)

