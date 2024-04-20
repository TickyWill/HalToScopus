__all__ = ['create_consolidate_scopus']

def _launch_update_scopus(institute,
                          haltoscopus_path,
                          corpus_year,
                          files_tup,
                          ):
    """
    """
    
    # Standard library imports    
    from tkinter import messagebox
    from pathlib import Path
    
    # Local imports     
    from HalToScopus_Utils.HTS_MainFunctions import consolidate_scopus 
    
    # Lancement de la fonction de consolidation de scopus
    ask_title = "- Confirmation de la consolidation de Scopus -"
    ask_text  = f"L'extraction de Scopus va être complétée "
    ask_text += f"avec les données disponibles sur HAL "
    ask_text += f"pour l'année {corpus_year}."
    ask_text += f"\n\nCette opération peut prendre une ou deux minutes."
    ask_text += f"\nDans l'attente, ne pas fermer 'HalToScopus'."        
    ask_text += f" \n\nEffectuer la consolidation ?"            
    answer    = messagebox.askokcancel(ask_title, ask_text)
    if answer:
        # Mise à jour de consolidation de scopus
        _, authy_status, update_status = consolidate_scopus(institute, haltoscopus_path, 
                                                                    corpus_year, files_tup)
        if authy_status:
            info_title = "- Information -"
            if update_status :                
                info_text  = f"L'extraction de Scopus a été complétée pour l'année {corpus_year} "
                info_text += f"et sauvegardée dans le fichier '{files_tup[1]}.csv'." 
                info_text += f"\n\nLes DOIs présents dans HAL ajoutés à Scopus "
                info_text += f"ont été stockés dans le fichier '{files_tup[4]}.xlsx'." 
                info_text += f"\n\nDe plus les DOIs présents dans HAL mais inconnus de Scopus "
                info_text += f"ont été stockés dans le fichier '{files_tup[3]}.xlsx'."
                info_text += f"\n\nL'extraction de HAL a été sauvegardée dans le fichier '{files_tup[2]}.xlsx'."
                info_text += f"\n\nLes fichiers sont dans le dossier {haltoscopus_path / Path(corpus_year)}."
            else:
                info_text  = f"L'extraction de Scopus n'a pas été modifiée pour l'année {corpus_year} "
                info_text += f"mais elle est sauvegardée dans le fichier '{files_tup[1]}.csv'."  
                info_text += f"\n\nAucun des DOIs présents dans HAL n'a été ajouté à Scopus "
                info_text += f"et le fichier '{files_tup[4]}.xlsx' est vide."  
                info_text += f"\n\nLes DOIs présents dans HAL mais inconnus de Scopus "
                info_text += f"ont été stockés dans le fichier '{files_tup[3]}.xlsx'."    
                info_text += f"\n\nL'extraction de HAL a été sauvegardée dans le fichier '{files_tup[2]}.xlsx'."
                info_text += f"\n\nLes fichiers sont dans le dossier {haltoscopus_path / Path(corpus_year)}."
            messagebox.showinfo(info_title, info_text)
        else:
            info_title = "- ATTENTION -"
            info_text  = f"!! L'autentification par Scopus a échoué !!"
    else:
        # Arrêt de la procédure
        info_title = "- Information -"
        info_text  = f"La consolidation de Scopus à été abandonnée."            
        messagebox.showwarning(info_title, info_text)
    return

def create_consolidate_scopus(self, institute, haltoscopus_path, parent):
    
    """
    Description : function working as a bridge between the HalToScopus 
    App and the functionalities needed for the use of the app
    
    Args : takes only self and haltoscopus_path as arguments. 
    self is the intense in which PageThree will be created
    haltoscopus_path is a type Path, and is the path to where the folders
    organised in a very specific way are stored
    
    Returns: nothing, it create the page in self
    """
    
    # Standard library imports
    import os
    from pathlib import Path
    
    # 3rd party imports
    import tkinter as tk
    from tkinter import font as tkFont
    from tkinter import messagebox
    
    # Local imports
    import HalToScopus_GUI.GUI_Globals as gg
    import HalToScopus_Utils.HTS_PubGlobals as hts_pg
    from HalToScopus_GUI.Page_Main import app_main
    from HalToScopus_GUI.Useful_Functions import encadre_RL 
    from HalToScopus_GUI.Useful_Functions import font_size
    from HalToScopus_GUI.Useful_Functions import last_available_years
    from HalToScopus_GUI.Useful_Functions import mm_to_px
    from HalToScopus_GUI.Useful_Functions import place_after
    from HalToScopus_GUI.Useful_Functions import place_bellow
    
    # Internal functions    
    def _launch_update_scopus_try():
        # Getting year selection
        year_select =  variable_years.get()
       
        # Setting useful aliases
        init_scopus_file_alias = year_select + hts_pg.FILES_BASE["scopus_base"]
        new_scopus_file_alias  = year_select + hts_pg.FILES_BASE["new_scopus_base"]
        hal_file_alias         = year_select + hts_pg.FILES_BASE["hal_base"]
        failed_file_alias      = year_select + hts_pg.FILES_BASE["failed_doi_base"]
        added_file_alias       = year_select + hts_pg.FILES_BASE["added_doi_base"]
        files_tup = (init_scopus_file_alias, new_scopus_file_alias, 
                     hal_file_alias, failed_file_alias, added_file_alias)
        
        # Setting working folder path
        working_folder_path = haltoscopus_path / Path(year_select)     
        
        # Cheking availability of Scopus file
        init_scopus_file_path = working_folder_path / Path(init_scopus_file_alias + ".csv")
        scopus_file_status = os.path.exists(init_scopus_file_path)    
        if scopus_file_status:
            _launch_update_scopus(institute,
                                  haltoscopus_path,
                                  year_select,
                                  files_tup,
                                  )
        else:
            warning_title = "!!! ATTENTION : fichier non disponible !!!"
            warning_text  = f"Le fichier {files_tup[0]}.csv' d'extraction de Scopus "
            warning_text += f"\nn'est pas disponible à l'emplacement attendu."
            warning_text += f"\n1- Mettez le fichier dans le dossier : "
            warning_text += f"\n {working_folder_path} ;"
            warning_text += f"\n2- Puis relancez consolidation de Scopus."
            messagebox.showwarning(warning_title, warning_text) 
        return

    def _launch_exit():
        message =  "Vous allez fermer HalToScopus. "
        message += "\nRien ne sera perdu et vous pourrez reprendre le traitement plus tard."
        message += "\n\nSouhaitez-vous faire une pause dans le traitement ?"
        answer_1 = messagebox.askokcancel('Information', message)
        if answer_1:
            parent.destroy()
    
    # Setting effective font sizes and positions (numbers are reference values in mm)
    eff_buttons_font_size    = font_size(gg.REF_ETAPE_FONT_SIZE-3, app_main.width_sf_min)
    eff_select_font_size     = font_size(gg.REF_ETAPE_FONT_SIZE-2, app_main.width_sf_min)
    eff_etape_font_size      = font_size(gg.REF_ETAPE_FONT_SIZE, app_main.width_sf_min)           #14
    eff_help_font_size       = font_size(gg.REF_ETAPE_FONT_SIZE-2, app_main.width_sf_min)
    eff_launch_font_size     = font_size(gg.REF_ETAPE_FONT_SIZE-1, app_main.width_sf_min)    
    etape_label_format = 'left'
    etape_underline    = -1    
    year_button_x_pos        = mm_to_px(gg.REF_YEAR_BUT_POS_X_MM * app_main.width_sf_mm,  gg.PPI)    #10  
    year_button_y_pos        = mm_to_px(gg.REF_YEAR_BUT_POS_Y_MM * app_main.height_sf_mm, gg.PPI)    #26     
    dy_year                  = -6
    ds_year                  = 5
    scopus_update_x_pos_px   = mm_to_px(10 * app_main.width_sf_mm,  gg.PPI)
    scopus_update_y_pos_px   = mm_to_px(50 * app_main.height_sf_mm, gg.PPI)     
    launch_dx_px             = mm_to_px( 0 * app_main.width_sf_mm,  gg.PPI)    
    launch_dy_px             = mm_to_px( 5 * app_main.height_sf_mm, gg.PPI)   
    exit_button_x_pos_px     = mm_to_px(gg.REF_EXIT_BUT_POS_X_MM * app_main.width_sf_mm,  gg.PPI)    #193 
    exit_button_y_pos_px     = mm_to_px(gg.REF_EXIT_BUT_POS_Y_MM * app_main.height_sf_mm, gg.PPI)    #145 

    ### Décoration de la page
    # - Canvas
    fond = tk.Canvas(self, 
                     width  = app_main.win_width_px, 
                     height = app_main.win_height_px)
    fond.place(x = 0, y = 0)
    
    ### Choix de l'année
    years_list = last_available_years(haltoscopus_path, gg.CORPUSES_NUMBER)
    default_year = years_list[-1]  
    variable_years = tk.StringVar(self)
    variable_years.set(default_year)
    
    # Création de l'option button des années    
    self.font_OptionButton_years = tkFont.Font(family = gg.FONT_NAME, 
                                               size = eff_buttons_font_size)
    self.OptionButton_years = tk.OptionMenu(self, 
                                            variable_years, 
                                            *years_list)
    self.OptionButton_years.config(font = self.font_OptionButton_years)
    
    # Création du label
    self.font_Label_years = tkFont.Font(family = gg.FONT_NAME, 
                                        size = eff_select_font_size)
    self.Label_years = tk.Label(self, 
                                text = gg.TEXT_YEAR, 
                                font = self.font_Label_years)
    self.Label_years.place(x = year_button_x_pos, y = year_button_y_pos)
    
    place_after(self.Label_years, self.OptionButton_years, dy = dy_year)
    encadre_RL(fond, self.Label_years, self.OptionButton_years, ds = ds_year)
    
    ################## Consolidation de scopus

    ### Titre
    scopus_update_font = tkFont.Font(family = gg.FONT_NAME, 
                                     size = eff_etape_font_size,
                                     weight = 'bold')
    scopus_update_label = tk.Label(self,
                                   text = gg.TEXT_ETAPE_1,
                                   justify = etape_label_format,
                                   font = scopus_update_font,
                                   underline = etape_underline)
    
    scopus_update_label.place(x = scopus_update_x_pos_px, 
                              y = scopus_update_y_pos_px)   
    
    ### Explication
    help_label_font = tkFont.Font(family = gg.FONT_NAME, 
                                  size = eff_help_font_size)
    help_label = tk.Label(self, 
                          text = gg.HELP_ETAPE_1, 
                          justify = "left", 
                          font = help_label_font)
    place_bellow(scopus_update_label, 
                 help_label)     
                                         
    ### Bouton pour lancer l'étape
    scopus_update_launch_font = tkFont.Font(family = gg.FONT_NAME, 
                                        size = eff_launch_font_size)
    scopus_update_launch_button = tk.Button(self,
                                        text = gg.TEXT_MAJ_SCOPUS,
                                        font = scopus_update_launch_font,
                                        command = lambda: _launch_update_scopus_try())
    place_bellow(help_label, 
                 scopus_update_launch_button, 
                 dx = launch_dx_px, 
                 dy = launch_dy_px)

    ################## Bouton pour sortir de la page
    font_button_quit = tkFont.Font(family =gg.FONT_NAME, 
                                   size   = eff_buttons_font_size)
    button_quit = tk.Button(self, 
                            text = gg.TEXT_PAUSE, 
                            font = font_button_quit, 
                            command = lambda: _launch_exit()).place(x = exit_button_x_pos_px, 
                                                                    y = exit_button_y_pos_px, 
                                                                    anchor = 'n')