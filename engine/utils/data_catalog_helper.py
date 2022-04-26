import google.auth
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import json


def create_tag_templates(location, tagtemplate_name):
    credentials, project = google.auth.default()
    service = googleapiclient.discovery.build(
        'datacatalog', 'v1beta1', credentials=credentials)

    response = get_tag_templates(location, tagtemplate_name)
    if 'error' in response and 'code' in response['error'] and response['error']['code'] == 403:
        return 'data catalog exist.'

    tag_template = service.projects().locations().tagTemplates().create(
        parent='projects/{project}/locations/{location}'.format(project=project, location=location),
        tagTemplateId=tagtemplate_name,
        body={
            "displayName": "Data Governance",
            "fields": {
                "data_governor": {
                    "displayName": "Data Governor",
                    "type": {
                        "primitiveType": "STRING"
                    },
                    "description": "Name of the Data Governor responsible for the governance of the data asset",
                    "order": 9
                },
                "encrypted_data_asset": {
                    "displayName": "Is Encrypted",
                    "type": {
                        "primitiveType": "BOOL"
                    },
                    "description": "Specifies whether this data asset is encrypted",
                    "order": 1
                },
                "approved_by_governance_date": {
                    "displayName": "Date of Governance Approval",
                    "type": {
                        "primitiveType": "TIMESTAMP"
                    },
                    "description": "The date when the asset was approved by Governance",
                    "order": 5
                },
                "data_classfication": {
                    "displayName": "Data Classification",
                    "type": {
                        "enumType": {
                            "allowedValues": [
                                {
                                    "displayName": "Public"
                                },
                                {
                                    "displayName": "Sensitive"
                                },
                                {
                                    "displayName": "Confidential"
                                }
                            ]
                        }
                    },
                    "description": "The data classification of the asset",
                    "order": 7
                },
                "approved_by_governance": {
                    "displayName": "Approved By Governance",
                    "type": {
                        "primitiveType": "BOOL"
                    },
                    "description": "All approved data assets must marked with this seal of approval",
                    "order": 6
                },
                "data_lifecycle": {
                    "displayName": "Data Lifecycle",
                    "type": {
                        "enumType": {
                            "allowedValues": [
                                {
                                    "displayName": "TEST"
                                },
                                {
                                    "displayName": "DEV"
                                },
                                {
                                    "displayName": "QA"
                                },
                                {
                                    "displayName": "PRODUCTION"
                                },
                                {
                                    "displayName": "OTHER"
                                },
                                {
                                    "displayName": "DEPRECATED"
                                }
                            ]
                        }
                    },
                    "description": "The lifecycle stage of the asset",
                    "order": 4
                },
                "retention_date": {
                    "displayName": "Retention Date",
                    "type": {
                        "primitiveType": "TIMESTAMP"
                    },
                    "description": "The date when retention for the asset ends",
                    "order": 3
                },
                "has_pii": {
                    "displayName": "Has PII",
                    "type": {
                        "primitiveType": "BOOL"
                    },
                    "description": "Specifies whether the asset contains PII data"
                },
                "deletion_date": {
                    "displayName": "Delete By Date",
                    "type": {
                        "primitiveType": "TIMESTAMP"
                    },
                    "description": "The date by which the asset must be deleted",
                    "order": 2
                },
                "business_owner": {
                    "displayName": "Business Owner",
                    "type": {
                        "primitiveType": "STRING"
                    },
                    "description": "Name of the owner or contact for the data asset",
                    "order": 8
                }
            }
        }
    ).execute()
    return tag_template


def get_tag_templates(location, tagtemplate_name):
    credentials, project = google.auth.default()
    service = googleapiclient.discovery.build(
        'datacatalog', 'v1beta1', credentials=credentials)

    try:
        tag_template = service.projects().locations().tagTemplates().get(
            name='projects/{project}/locations/{location}/tagTemplates/{tagtemplate}'.format(
                project=project, location=location, tagtemplate=tagtemplate_name),
        ).execute()

        return tag_template

    except HttpError as e:
        return (json.loads(e.content.replace('\\', '\\\\'), strict=False))
    except Exception as e:
        return {'error': {'code': 500, 'message': str(e), 'status': 'ERROR'}}