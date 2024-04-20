__all__ = ['consolidate_scopus',
          ]


def consolidate_scopus(institute, haltoscopus_path, corpus_year, files_tup):

    # Standard library imports
    from pathlib import Path

    # 3rd party imports
    import HalApyJson as haj
    import pandas as pd
    import ScopusApyJson as saj
    
    # Local imports
    from HalToScopus_Utils.HTS_PubGlobals import UNKNOWN
    
    # internal functions
    
    def _replace_na(init_df):
        init_df.fillna(0, inplace = True)
        new_df = init_df.astype(str)
        new_df.replace('0', UNKNOWN, inplace=True)
        return new_df
       
    # Setting working folder path
    working_folder_path = haltoscopus_path / Path(corpus_year)    

    # Setting already extracted DOIs list from scopus database
    init_scopus_file_alias = files_tup[0]
    init_scopus_file_path = working_folder_path / Path(init_scopus_file_alias + ".csv")
    scopus_init_df = pd.read_csv(init_scopus_file_path, sep = ",")
    scopus_init_df = _replace_na(scopus_init_df)
    scopus_doi_list_raw = scopus_init_df['DOI'].tolist()
    scopus_doi_list_lower = [str(doi).lower() for doi in scopus_doi_list_raw]
    scopus_doi_set = set(scopus_doi_list_lower)

    # Getting DOIs list using HAL api
    hal_df = haj.build_hal_df_from_api(corpus_year, institute.lower())
    hal_df = _replace_na(hal_df)
    hal_df.fillna(UNKNOWN, inplace = True)
    hal_doi_list_raw = list(set(hal_df["DOI"].tolist()) - set([UNKNOWN]))
    hal_doi_list_lower = [doi.lower() for doi in hal_doi_list_raw]
    hal_doi_set = set(hal_doi_list_lower)

    # Buiding DOIs list from HAL not in DOIs list extracted from scopus database
    hal_not_scopus_doi_list = list(hal_doi_set - hal_doi_set.intersection(scopus_doi_set))
    hal_not_scopus_doi_list = ["doi/" + doi for doi in hal_not_scopus_doi_list]

    # Build the dataframe with the results of the parsing 
    # of the api request response for each DOI of the hal_not_scopus_doi_list list
    scopus_tup = saj.build_scopus_df_from_api(hal_not_scopus_doi_list, timeout = 30, verbose = False)
    authy_status = scopus_tup[2]
    if authy_status: 
        scopus_df = scopus_tup[0]
        scopus_df = _replace_na(scopus_df)
        new_scopus_file_alias = files_tup[1]
        if not scopus_df.empty:
            new_scopus_df = pd.concat([scopus_init_df, scopus_df])
            message  = f"\n\nScopus csv file updated with complementary HAL DOIs "
            message += f"saved as '{new_scopus_file_alias}.csv' in: \n{working_folder_path}"
            update_status = True
        else:
            new_scopus_df = scopus_init_df.copy()
            message  = f"\nScopus csv file unchanged but " 
            message += f"saved as '{new_scopus_file_alias}.csv' in: \n{working_folder_path}"
            update_status = False

        # Saving the new scopus dataframe as csv file in the working folder  
        file_csv_path = working_folder_path / Path(new_scopus_file_alias + ".csv")
        new_scopus_df.to_csv(file_csv_path,
                             header = True,
                             index = False,
                             sep = ',') 
        
        # Saving the dataframe of added DOIs as xlsx file in the working folder 
        added_file_alias = files_tup[4]
        added_file_xlsx_path = working_folder_path / Path(added_file_alias + ".xlsx") 
        scopus_df.to_excel(added_file_xlsx_path, index = False)
        message += f"\n\nComplementary HAL DOIs added to the Scopus csv file " 
        message += f"saved as '{added_file_alias}.xlsx' in: \n{working_folder_path}"
        
        # Saving the dataframe of DOIs that failed to be extracted as xlsx file in the working folder 
        failed_doi_df = scopus_tup[1]
        failed_file_alias = files_tup[3]
        failed_file_xlsx_path = working_folder_path / Path(failed_file_alias + ".xlsx") 
        failed_doi_df.to_excel(failed_file_xlsx_path, index = False)
        message += f"\n\nComplementary HAL DOIs not found in scopus database " 
        message += f"saved as '{failed_file_alias}.xlsx' in: \n{working_folder_path}"          

        # Saving HAL extraction
        hal_file_alias = files_tup[2]
        hal_file_path = working_folder_path / Path(hal_file_alias + ".xlsx")
        hal_df.to_excel(hal_file_path, index = False)
        message += f"\n\nHAL extraction file saved as '{hal_file_alias}.xlsx' in: \n{working_folder_path}"
        
    else:
        message = "Scopus authentication failed"
    return (message, authy_status, update_status) 