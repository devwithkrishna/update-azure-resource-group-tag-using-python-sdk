import os
import argparse
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import TagsPatchResource
from dotenv import load_dotenv
from azure_resource_graph_query import run_azure_rg_query


def update_azure_tag(tag_key: str, tag_value: str, resource_group_names: str, subscription_id: str):
    """
    update a specific tag with a value using python sdk

    :param tag_key:
    :param tag_value:
    :return:
    """
    load_dotenv()
    credential = DefaultAzureCredential()

    subscription_id = os.environ["subscription_id"]
    resource_client = ResourceManagementClient(credential, subscription_id)
    # create an empty tags dictionary
    tags = {}

    # Split the comma seperated rg names to a list to iterate
    resource_groups = resource_group_names.split(",")

    for resource_group_name in resource_groups:
        # resource_group_name = "resource-graph-queries"
        # Creating the tags dictionary with tag key and value
        tags[tag_key] = tag_value

        print(f"tags are : {tags}")
        tag_resource =  TagsPatchResource(
            operation="Merge",
            properties={'tags': tags}
        )
        resource = resource_client.resources.get_by_id(
            f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}",
            "2022-09-01"
        )
        resource_client.tags.begin_update_at_scope(resource.id, tag_resource)

        print(f"Tags {tag_resource.properties.tags} were added to resource with ID: {resource.id}")


def main():
    """
    To test the script
    :return:
    """
    parser = argparse.ArgumentParser("Tag updation automation in Azure using python")
    parser.add_argument("--tag_value", help= "tag value corresponding to the key in azure", required=True, type=str)
    parser.add_argument("--tag_key", help= "tag keys in azure", required=True, type=str)
    parser.add_argument("--subscription_name", help="subscription name in azure", required=True, type=str)
    parser.add_argument("--resource_group_names", help= "names of resource groups. more than one can be provided as comma seperated values", required=True, type=str)

    args = parser.parse_args()
    tag_key = args.tag_key
    tag_value = args.tag_value
    subscription_name = args.subscription_name
    resource_group_names = args.resource_group_names

    logging.info("Proccess started......")
    subscription_id = run_azure_rg_query(subscription_name=subscription_name)
    os.environ['subscription_id'] = subscription_id
    update_azure_tag(tag_key= tag_key,tag_value=tag_value,resource_group_names= resource_group_names, subscription_id=subscription_id)
    logging.info("Process completed.")


if __name__ == "__main__":
    main()