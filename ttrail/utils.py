import click 
import dateparser
import boto3

def validate_time(ctx, param, value):
    """Parse and validate Click arguments (start-time & end-time) with dateparser module to easily parse localized dates in almost any string formats commonly found on web pages.
    Examples: "July 4, 2021 PST" , "21 July 2013 10:15 pm +0500" or \
               human readables "1 hour ago", "in 2 days", "now", "2021-01-01" and "one hour ago """

    time = dateparser.parse(value , settings={'RETURN_AS_TIMEZONE_AWARE': True})
    if time:
        return time
    
    raise click.BadParameter('Invalid start/end time argument')


def validate_aws_profile(ctx, param, value):
    """check if AWS profile is exist and a session could be set up with the specified profile """
    try:
        session = boto3.Session(profile_name=value)
        return value
    except Exception as e:
        raise click.BadParameter(e)
