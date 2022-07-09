import pandas as pd
from rich.tree import Tree
from rich import print as richprint
from rich.text import Text

class Treeview():
    EVENT_TYPE_ADDITION = {
        "IAMUser": "CloudTrailEvent.userIdentity.userName",
        "Root": "CloudTrailEvent.userIdentity.userName",
        "AssumedRole": "CloudTrailEvent.userIdentity.sessionContext.sessionIssuer.arn",
        "Role": "",
        "FederatedUser": "",
        "Directory": "",
        "AWSAccount": "CloudTrailEvent.userIdentity.accountId",
        "AWSService": "CloudTrailEvent.userIdentity.invokedBy",
        "SAMLUser": "CloudTrailEvent.userIdentity.userName",
        "WebIdentityUser": "CloudTrailEvent.userIdentity.userName",
        "Unknown": ""
    }
    EVENT_NAME_ADDITION = {
            "AssumeRole" : ['CloudTrailEvent.requestParameters.roleArn'],
            'default' : []
    }
    DEFAULT_GROUP = ['EventSource',	'EventName', 'CloudTrailEvent.eventType', 'CloudTrailEvent.userIdentity.type']

    def __init__(self, cloudtrail) -> None:
        self.events_df = cloudtrail.events_df
        self.base_df = cloudtrail.events_df.groupby(['EventSource',	'EventName', 'CloudTrailEvent.eventType', 'CloudTrailEvent.userIdentity.type']).agg({'EventId': ['count']}).reset_index()
        # Check if we should skip AWS Service events
        if cloudtrail.skip_service_events:
            self.base_df.drop(self.base_df[self.base_df['CloudTrailEvent.userIdentity.type'] == 'AWSService'].index, inplace = True)
        self.tree = Tree(f":orange_book: TTrail Events from {cloudtrail.start_time} to {cloudtrail.end_time}")
    
    def generate(self):
        tree_events = set()
        group_with_errorcode = False
        for row in self.base_df.itertuples(index=False, name=None):
            if row[1] not in tree_events:
                subtree_title = Text.assemble((row[0], "bold green"), f" {row[1]}")
                subtree = self.tree.add( Text('📒 ') + subtree_title)
                tree_events.add(row[1])
            group_fields = list(Treeview.DEFAULT_GROUP)
            # Add errorcode column to the groupby only it exists
            if 'CloudTrailEvent.errorCode' in self.events_df.columns:
                group_with_errorcode = True
                group_fields.append('CloudTrailEvent.errorCode')
            group_fields.append(Treeview.EVENT_TYPE_ADDITION[row[3]])
            event_type_position = len(group_fields) - 1
            group_fields += Treeview.EVENT_NAME_ADDITION.get(row[1], Treeview.EVENT_NAME_ADDITION['default'])
            group_df = self.events_df[ 
                (self.events_df['EventSource'] == row[0]) &
                (self.events_df['EventName'] == row[1]) &
                (self.events_df['CloudTrailEvent.eventType'] == row[2]) &
                (self.events_df['CloudTrailEvent.userIdentity.type'] == row[3])].groupby(group_fields, dropna=False).agg({'EventTime': ['count', 'min', 'max']}).reset_index()
            for r in group_df.itertuples(index=False, name=None):
                additional_info = ''.join(f' {group_fields[i][16:]}: {r[i]}' for i in range(event_type_position + 1 ,len(group_fields)))
                error_info = f' CloudTrailEvent.errorCode: {r[4]} ' if group_with_errorcode and (not pd.isna(r[4])) else ''
                row_text = Text.assemble(f' {Treeview.EVENT_TYPE_ADDITION[row[3]][16:]}: ', (f'{r[event_type_position]}', 'yellow'), (error_info, 'red') ,f' ({r[3]})',' event.Type: ' ,(f'{r[2]}', "blue"), additional_info, f'  repeated: {r[-3]} time(s)',  '\n')
                subtree.add(row_text)
    
    def __repr__(self) -> str:
        richprint(self.tree)
        return ''