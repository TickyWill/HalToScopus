#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Local imports
from htsgui.main_page import AppMain

def run_hts():
    """Main function used for starting the HalToScopus application.
    """
    try:
        app = AppMain()
        app.mainloop()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    run_hts()


# In[ ]:




