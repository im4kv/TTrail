import boto3
import pandas as pd
from collections.abc import MutableMapping
import json
from rich.console import Console


class Cloudtrail():
    def __init__(self, start_time, end_time, filter, source, aws_profile, aws_region, skip_service_events) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.filter = filter
        self.source = source
        self.events_df = pd.DataFrame()
        self.events = []
        self.aws_profile = aws_profile
        self.aws_region = aws_region
        self.skip_service_events = skip_service_events

    def load_from_aws_event_history(self):
        console = Console()
        total_df = pd.DataFrame()
        event_count = 0
        session = boto3.Session(profile_name=self.aws_profile, region_name=self.aws_region)
        cloudtrail = session.client('cloudtrail')
        paginator = cloudtrail.get_paginator('lookup_events')
        page_iterator = paginator.paginate(LookupAttributes=[
                        {
                            'AttributeKey': 'ReadOnly',
                            'AttributeValue': 'false'
                        },
                    ],
                    StartTime=self.start_time)
        with console.status("[bold green] Downloading events from AWS Cloudtrail Event History..." ) as status:
            for page in page_iterator:
                event_count += len(page['Events'])
                status.update(f"[bold green] Total events downloaded: {event_count},  Downloading next batch...")
                for event in page['Events']:
                    event['CloudTrailEvent'] = json.loads(event['CloudTrailEvent'])
                    event = self.flatten_dict(event)
                    self.events.append(event)
        
        self.events_df = pd.DataFrame(self.events)
        return self.events_df

    def flatten_dict(self, d: MutableMapping, parent_key: str = '', sep: str ='.') -> MutableMapping:
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def normalize_fields(self):
        pass   
    