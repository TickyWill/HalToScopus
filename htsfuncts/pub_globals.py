"""Module for setting publicatoons globals."""

__all__ = ['UNKNOWN',
           'FILES_BASE',
          ]


UNKNOWN = "unknown"

FILES_BASE = {"scopus_base"      : "-final scopus",
              "new_scopus_base"  : "-final scopus_hal",
              "added_doi_base"   : " hal_added_dois",
              "failed_doi_base"  : " scopus_failed_dois",
              "hal_base"         : " hal",
              "new_doi_base"     : " hal_new_dois",
             }
