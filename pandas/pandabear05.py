#!/usr/bin/python3

import pandas as pd
import xlsxwriter

def main():
    # create a dataframe ciscocsv
    ciscocsv = pd.read_csv("ciscodata.csv")
    # create a dataframe ciscojson
    ciscojson = pd.read_json("ciscodata2.json")

    # The line below concats and reapplies the index value
    ciscodf = pd.concat([ciscocsv, ciscojson], ignore_index=True, sort=False)
    
    ## export to json
    ## do not include index number
    ciscodf.to_json("combined_ciscodata.json", orient="records")

    ## export to csv
    ## do not include index number
    ciscodf.to_csv("combined_ciscodata.csv", index=False)
    
    ## export to Excel
    ## do not include index number to xls
    ciscodf.to_excel("combined_ciscodata.xls", index =False, engine='xlsxwriter')
    ## do not include index number to xlsx
    ciscodf.to_excel("combined_ciscodata.xlsx", index=False, engine='xlsxwriter')
    
    ## create a python dictionary
    ## do not include index number
    x = ciscodf.to_dict(orient='records')
    print(x)
    
if __name__ == "__main__":
    main()

