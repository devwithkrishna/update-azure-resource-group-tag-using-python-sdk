# update-azure-resource-group-tag-using-python-sdk
update-azure-resource-group-tag-using-python-sdk

## Inputs 

* tag_key   --> tag name in azure
* tag_value --> tag value in azure
* resource_group_names   --> names of resource groups. more than one can be provided as comma seperated values
* subscription_name --> Azure subscription name


## How code works?

* Azure Identity - uses DefaultAzureCredential method for authentication.
  * This uses the service principal app id, service principal secret and tenant id to do the authentication make sure you have the below.
    ``` 
     AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID are the environment variables it will be using
    ``` 
I use the .env to supply the above vars and load them using python-dotenv package and use it. or you can pass it as environment variable and use by os method.
The .env file will be of following

```commandline
AZURE_CLIENT_ID = "value"
AZURE_CLIENT_SECRET = "value"
AZURE_SUBSCRIPTION_ID = "value"
AZURE_TENANT_ID = "value"
```
* This is how stuff is passed from work flow to pythin file
```
jobs:
  azure-tag-updation-using-python-github-workflow:
    runs-on: ubuntu-latest
    env:
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
    steps:
      - name: run python program
        run: |
          pipenv run python3 update_azure_tag.py --tag_key ${{ inputs.tag_key }} \
          --tag_value ${{ inputs.tag_value }} \
          --subscription_name ${{ inputs.subscription_name }} \
          --resource_group_names ${{ inputs.resource_group_names }}
  ```
:pushpin: azure_resource_graph_query --> this will use the subcription name, run azure resource graph query return the sunbscription id.

:pushpin: [yes] I have configued AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_TENANT_ID as repository secrets / organizational secrets.