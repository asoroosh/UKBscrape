# UKBscrape

Requirements

You should have a linux/mac machine with an internet connection. 

### Code
Python packages: `os`, `numpy`, `pandas` and `re`

### Data
You should have a text file which conatins _all_ FieldIDs available in your UKB application. If you have a CSV file of all the variables, you can do 
`cat head YOUR_UKB_APPLICATION_XXX.{tsv,csv} >> ukbXXXX_Headers.txt`


## Configuration



## Function & Usage

### Matching 
It helps you find intersection between variables available through your application and (almost) all other UKB advertised through https://biobank.ctsu.ox.ac.uk/

### Dictionary 
It acts as a dictionary, you can pass a variable Field ID and it will return the variable name and its category (by category I mean *UKbiobank* pre-defined categories.)

