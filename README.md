# ar-ddns
ArvanCloud Dynamic DNS Tool

### Setup
replace variables and set as crontab using `crontab -e`
```
* * * * * curl --interface $INTERFACE 'https://napi.arvancloud.com/cdn/4.0/domains/yazdatba.com/dns-records/$RECORD_ID/' \
  -X 'PUT' \
  -H 'accept: application/json, text/plain, */*' \
  -H "authorization: $API_KEY" \
  -H 'content-type: application/json;charset=UTF-8' \
  --data-binary "{'id':'$RECORD_ID','type':'$RECORD_TYPE','name':'$NAME','cloud':$CLOUD,'value':[{'ip':'$(curl ifconfig.me)','port':null,'weight':100,'country':null}],'ttl':120,'ip_filter_mode':{'count':'single','order':'none','geo_filter':'location'},'upstream_https':'default'}' \
  --compressed
```

| Name                                 | Description                                               |  Type | Default
|:-------------------------------------|:----------------------------------------------------------|:-----:|:--------:|
| `INTERFACE` | network interface | string | -
| `RECORD_ID` | arvan dns record id | string | -
| `API_KEY` | arvan api key | string | -
| `NAME` | record name | string | -
| `CLOUD` | arvan cloud enable | bool | -

---
# Brief
Some Times the origin servers don't have the static IP and their IP may change after a while.
With this tool the user can update DNS record in ArvanCloud DNS service automatically.

## Input
User API Token available in ArvanCloud panel

## Capabalities
* Set DNS Record 
* Update DNS Record
* ...

## Useful Link
[CDN API Documentation](https://www.arvancloud.com/docs/api/cdn/4.0)


## Terms and Conditions
* All projects received to ArvanCloud will be reviewed, and the price will be paid to the first approved project.
* All projects have to have test and execution document.
* The project doer has to solve issues and apply required changes for 6 months after approval of the project.
* General changes or changing programming language in each project has to be approved by ArvanCloud.
* In case more than one project is approved by ArvanCLoud, the project fee will be equally divided between winning projects.
* In the evaluation and code reviews stages of a project, no new request for the same project will be accepted. In case the reviewed project fails to pass the quality assessments, the project will be reactivated.
* If projects require any update or edit, merge requests will be accepted in GitHub after reassessment and reapproval.
* Approved projects will be forked in GitHub, and ArvanCloud will star them.
* GitHub name and address of the approved project doer will be published alongside the project. 
