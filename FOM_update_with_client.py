import logging
import os
import csv
from progress.bar import Bar

import libplanon
import requests
import resources.logger

get_token = libplanon.TokenManager(
    url=os.environ.get("PLN_URL"),
    username=os.environ.get("PLN_USR"),
    password=os.environ.get("PLN_PWD")
).get_token

pln_client = libplanon.APIManager(url=os.environ.get("PLN_URL"), services=["Property"])
pln_Property_client = pln_client["Property"]


# ===========================================================================================
# MAIN
#Loop through all the Buildings - read , update with semi-colon and save
# if len(FOM_String) ==30 , then Assign "Freestring45" to ; + FOM_String else skip
# after updating if if len(FOM_String) ==31, then write to check.csv
# if len(FOM_String) ==25, update with semicolon and check for len==26, write to special.csv
# if exception & none of above cases, then write to fail.csv
# Write to CSV file with Building code, FOM string & Name 
# ===========================================================================================
log = logging.getLogger(__name__)

succeeded = []
check=[]
special=[]
skipped = []
failed = []

success_count=0
check_count=0
special_count=0
skip_count=0
fail_count=0

pln_Property_ids= pln_Property_client.find(get_token(), {})
log.info(f"Found {len(pln_Property_ids)} Planon Properties")
bar = Bar("Processing", max=len(pln_Property_ids))

# https://www.geeksforgeeks.org/working-csv-files-python/
column_headers = ['Building_Code','FOM_Chartstring','Buiding_name']

for Property in pln_Property_ids: 
    pln_Property = pln_Property_client.read(get_token(), Property)
    Property_code = pln_Property["code"]
    FOM_String = pln_Property["freeString45"] 
    Property_name = pln_Property["name"]
    row_data=[Property_code, FOM_String,Property_name]   

    try:
        if len(FOM_String) != None and len(FOM_String)==30: 
            pln_Property["freeString45"]= ';'+FOM_String
            pln_Property_client.save(get_token(),pln_Property)
            
            if len(pln_Property["freeString45"])==31:
                succeeded.append(Property)
                success_count=success_count+1
                log.info(f"FOM Chartstring {pln_Property['freeString45']} updated with semicolon for {Property_code}")
                
                with open("succeeded.csv", 'a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row_data)
                
            if len(pln_Property["freeString45"])>31:
                check.append(Property)
                check_count=check_count+1
                log.info(f"Length of {pln_Property['freeString45']} incorrect , check {Property_code}")
                
                with open("check.csv", 'a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row_data)

        elif len(FOM_String)!= None and len(FOM_String) > 0 and len(FOM_String) < 30:
            pln_Property["freeString45"]= ';'+FOM_String
            pln_Property_client.save(get_token(),pln_Property)
            
            if len(pln_Property["freeString45"])==26:
                special.append(FOM_String)
                special_count=special_count+1
                log.info(f"FOM Chartstring {pln_Property['freeString45']} updated with semicolon for {Property_code}")
                with open("special.csv", 'a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row_data)

        elif len(FOM_String) != None and len(FOM_String)==31:
            skipped.append(Property_code)
            skip_count=skip_count+1
            log.info(f"Record skipped for {Property_code} as it already has a semicolon")
            with open("skipped.csv", 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row_data)

    except Exception as ex:
            failed.append(FOM_String)
            fail_count=fail_count+1
            log.info(f"Record skipped for {Property_code} due to exception {ex} ")
            with open("failed.csv", 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row_data)

log.info(f"Found {len(pln_Property_ids)} Planon Properties")
log.info(f"Total records succeeded: {success_count}")
log.info(f"Total records to check : {check_count}")
log.info(f"Total records succeeded for special case properties: {special_count}")
log.info(f"Total records skipped due to already present semicolon: {skip_count}")
log.info(f"Total records failed: {fail_count}")
