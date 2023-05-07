# TCC

## How to Use this Algorithm

### Obtaining your values for analysis

    This program uses the Class Analysis results of the program [CK](https://github.com/mauricioaniche/ck).
    They should be moved to the directory "./class"

### Stabilishing your metrics/threasholds

    Your metrics have to be added to the directory "./threasholds", following the format
    ```
    name,sign,value
    cbo,>,1
    cboModified,>,1
    ```
    Each line represents a limit, if you want a range between 0 and 1000 for LOC for exemple, it's necessary to add 2 lines:
    
    ```
        name,sign,value
        loc,>,0
        loc,<,1000
    ```
    Each file must have the name of the Code Smell to be analysed
