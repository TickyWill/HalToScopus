"""Module of functions for building updated publications list extracted 
from Scopus database for the Institute selected in the GUI."""

__all__ = ['consolidate_scopus',
          ]


# Standard library imports
from pathlib import Path

# 3rd party imports
import pandas as pd
import HalApyJson as haj
import ScopusApyJson as saj

# Local imports
import htsfuncts.pub_globals as hts_pg


def _replace_na(init_df):
    """Replaces NAN and "NA" values."""
    init_df.fillna(0, inplace=True)
    new_df = init_df.astype(str)
    new_df = new_df.replace(to_replace={'0': hts_pg.UNKNOWN,
                                        'NA': hts_pg.UNKNOWN})
    return new_df


def _get_scopus_dois(init_scopus_file, working_folder_path):
    """Sets already extracted DOIs list from scopus database."""
    init_scopus_file_path = working_folder_path / Path(init_scopus_file + ".csv")
    scopus_init_df = pd.read_csv(init_scopus_file_path, sep = ",")
    scopus_init_df = _replace_na(scopus_init_df)
    scopus_dois_list_raw = scopus_init_df['DOI'].tolist()
    scopus_dois_list_lower = [str(doi).lower() for doi in scopus_dois_list_raw]
    scopus_dois_set = set(scopus_dois_list_lower)
    return scopus_dois_set, scopus_init_df


def _extract_hal_dois(institute, corpus_year, working_folder_path,
                      hal_files_tup, scopus_dois_set):
    """Sets DOIs list from HAL not in DOIs list extracted 
    from scopus database."""
    # Getting HAL extraction using HAL api
    hal_df = haj.build_hal_df_from_api(corpus_year, institute.lower())
    hal_df = _replace_na(hal_df)

    # Saving HAL extraction
    hal_file_alias = hal_files_tup[0]
    hal_file_path = working_folder_path / Path(hal_file_alias + ".xlsx")
    hal_df.to_excel(hal_file_path, index = False)
    message = (f"\n\nHAL extraction file saved as '{hal_file_alias}.xlsx' "
               "in: \n{working_folder_path}")

    # Setting DOIs list from HAL extraction
    hal_doi_list_raw = list(set(hal_df["DOI"].tolist()) - set([hts_pg.UNKNOWN]))
    hal_doi_list_lower = [doi.lower() for doi in hal_doi_list_raw]
    hal_doi_set = set(hal_doi_list_lower)

    # Buiding DOIs list from HAL not in DOIs list extracted from scopus database
    hal_not_scopus_doi_list = list(hal_doi_set - hal_doi_set.intersection(scopus_dois_set))
    hal_not_scopus_doi_list = ["doi/" + doi for doi in hal_not_scopus_doi_list]

    # Saving DOIs list from HAL not in DOIs list extracted from scopus database
    dois_file_alias = hal_files_tup[1]
    dois_file_path = working_folder_path / Path(dois_file_alias + ".xlsx")
    dois_df = pd.DataFrame(hal_not_scopus_doi_list, columns=["DOI"])
    dois_df.to_excel(dois_file_path, index=False)
    message += ("\n\nDOIs list from HAL not in DOIs list extracted from scopus database "
                f"saved as '{dois_file_alias}.xlsx' in: \n{working_folder_path}")
    return message, hal_not_scopus_doi_list


def consolidate_scopus(institute, haltoscopus_path, corpus_year, files_tup):
    """Complements the scopus extraction with information on publications 
    of which DOIs are found in HAL extraction.
    
    Args:
        institute (str): Institute name.
        corpus_year (str): 4 digits year of the corpus.
        haltoscopus_path (path): Full path to working folder.
        files_tup (tup): (name of the initial Scopus extraction file, \
        name of the updated Scopus file, name for the HAL extraction file, \
        name for the file where DOIs list not present in the initial Scopus \
        extraction is saved, name of the file where publications information \
        of DOIs not found in the Scopus database is saved, name of the file \
        where publications information added to the initial Scopus extraction \
        is saved).
    Returns:
        (tup): (message for exe log (str), authentication status \
        on Scopus database (bool), Scopus extraction update status (bool)).
    """
    # Initialize status
    update_status = False
    authy_status = False

    # Setting results file name
    new_scopus_file_alias = files_tup[1]

    # Setting already extracted DOIs list from scopus database
    init_scopus_file = files_tup[0]
    year_haltoscopus_path = haltoscopus_path / Path(corpus_year)
    scopus_dois_set, scopus_init_df = _get_scopus_dois(init_scopus_file, year_haltoscopus_path)

    # Building DOIs list from HAL not in DOIs list extracted from scopus database
    hal_files_tup = (files_tup[2], files_tup[3])
    message, hal_not_scopus_doi_list = _extract_hal_dois(institute, corpus_year,
                                                         year_haltoscopus_path,
                                                         hal_files_tup, scopus_dois_set)

    if hal_not_scopus_doi_list:

        # Build the dataframe with the results of the parsing
        # of the api request response for each DOI of the hal_not_scopus_doi_list list
        scopus_tup = saj.build_scopus_df_from_api(hal_not_scopus_doi_list,
                                                  timeout=30, verbose=False)
        authy_status = scopus_tup[2]
        if authy_status:
            scopus_df = scopus_tup[0]
            scopus_df = _replace_na(scopus_df)
            if not scopus_df.empty:
                new_scopus_df = pd.concat([scopus_init_df, scopus_df])
                message += (f"\n\nScopus csv file updated with complementary HAL DOIs "
                            f"saved as '{new_scopus_file_alias}.csv' in: \n{year_haltoscopus_path}")
                update_status = True
            else:
                new_scopus_df = scopus_init_df.copy()
                message += (f"\nScopus csv file unchanged but "
                            f"saved as '{new_scopus_file_alias}.csv' in: \n{year_haltoscopus_path}")
                update_status = False

            # Saving the new scopus dataframe as csv file in the working folder
            file_csv_path = year_haltoscopus_path / Path(new_scopus_file_alias + ".csv")
            new_scopus_df.to_csv(file_csv_path,
                                 header = True,
                                 index = False,
                                 sep = ',')

            # Saving the dataframe of added DOIs as xlsx file in the working folder
            added_file_alias = files_tup[4]
            added_file_xlsx_path = year_haltoscopus_path / Path(added_file_alias + ".xlsx")
            scopus_df.to_excel(added_file_xlsx_path, index = False)
            message += (f"\n\nComplementary HAL DOIs added to the Scopus csv file "
                        f"saved as '{added_file_alias}.xlsx' in: \n{year_haltoscopus_path}")

            # Saving the dataframe of DOIs that failed to be extracted
            # as xlsx file in the working folder
            failed_doi_df = scopus_tup[1]
            failed_file_alias = files_tup[3]
            failed_file_xlsx_path = year_haltoscopus_path / Path(failed_file_alias + ".xlsx")
            failed_doi_df.to_excel(failed_file_xlsx_path, index = False)
            message += (f"\n\nComplementary HAL DOIs not found in scopus database "
                        f"saved as '{failed_file_alias}.xlsx' in: \n{year_haltoscopus_path}")
        else:
            message = "Scopus authentication failed"
    else:
        new_scopus_df = scopus_init_df.copy()
        message += (f"\n\nAll HAL DOIs are in initial Scopus csv file."
                    f"\nScopus csv file unchanged but "
                    f"saved as '{new_scopus_file_alias}.csv' "
                    f"in: \n{year_haltoscopus_path}")
        update_status = False
        authy_status = True

        # Saving the new scopus dataframe as csv file in the working folder
        file_csv_path = year_haltoscopus_path / Path(new_scopus_file_alias + ".csv")
        new_scopus_df.to_csv(file_csv_path,
                             header=True,
                             index=False,
                             sep=',')
    return message, authy_status, update_status
