# UKBscrape

## Requirements

You should have a linux/mac machine with an internet connection. 

### Code
Python packages: `os`, `numpy`, `pandas` and `re`

### Data
You should have a text file which conatins _all_ FieldIDs available in your UKB application. If you have a CSV file of all the variables, you can do 
`head -n 1 /path/2/your/UKB/ukbXXXXX.csv > ukbXXXX_Headers.txt`

## Configuration

If it is your first time that you use the UKBscrape, please make sure you are connected to the internet and run the following in the same directory as UKBscrape: 

```
import UKBscrape as ukbs
ukbs.update()
```

This will make a sub-directory `~/IDLabCat` which contains list of all variables and their categories.


## Function & Usage

### Matching 
It helps you find intersection between variables available through your application and (almost) all other UKB advertised through https://biobank.ctsu.ox.ac.uk/

```
ukbs.match(UKBCSVFile = 'ukbXXXX_Headers.txt',Report2 = '/write/me/down/a/report/')
```

Report2 [optional]: if you need to save the reports, set a path for the results. 
This will produce two csv files: 
*YouDontHave.csv`: FieldID, label and category of the variables that you don't have
*WasntParsed.csv`: the variables that may have missed in parsing but your application has! 

### Dictionary 
It acts as a dictionary, you can pass a variable Field ID and it will return the variable name and its category (by category I mean *UKbiobank* pre-defined categories.)
```
ukbs.dictionary(UKBCSVFile = '', FieldID = '' ,SaveMe2 = '')
```

*`UKBCSVFile`: path to the file of your UKB csv file (it is only to check whether you have that specific Field ID)
*`FieldID`: The Field ID that you need to use the dictionary for. This has to be list of integers
*`SaveMe2` [optional]: path to a directory to save the results as tsv file. It saves the FieldID, labels and categories of passed FieldIDs

For example:

```

ukbs.dictionary(UKBCSVFile = 'ukb25120_Headers.txt',FieldID=['4056','26412']);

You requested dictionary for 2 data fields.
                            Label                         Category WeHave
4056         Age stroke diagnosed               Medical conditions   True
26412  Employment score (England)  Indices of Multiple Deprivation  False
```

