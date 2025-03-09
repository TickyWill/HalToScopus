"""The `update_scopus_page` GUI module allows to built updated publications 
list extracted from Scopus database for the Institute selected.
"""

__all__ = ['create_consolidate_scopus']

# Standard library imports
import os
from pathlib import Path

# 3rd party imports
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

# Local imports
import htsgui.gui_globals as gg
import htsfuncts.pub_globals as hts_pg
from htsfuncts.main_functs import consolidate_scopus
from htsgui.useful_functs import set_frame_rl
from htsgui.useful_functs import font_size
from htsgui.useful_functs import last_available_years
from htsgui.useful_functs import mm_to_px
from htsgui.useful_functs import place_after
from htsgui.useful_functs import place_bellow


def _launch_update_scopus(institute,
                          haltoscopus_path,
                          corpus_year,
                          files_tup,
                          ):
    # Lancement de la fonction de consolidation de scopus
    ask_title = "- Confirmation de la consolidation de Scopus -"
    ask_text = (f"L'extraction de Scopus va être complétée "
                f"avec les données disponibles sur HAL "
                f"pour l'année {corpus_year}."
                f"\n\nCette opération peut prendre une ou deux minutes."
                f"\nDans l'attente, ne pas fermer 'HalToScopus'."
                f" \n\nEffectuer la consolidation ?")
    answer = messagebox.askokcancel(ask_title, ask_text)
    if answer:
        # Mise à jour de consolidation de scopus
        _, authy_status, update_status = consolidate_scopus(institute, haltoscopus_path,
                                                            corpus_year, files_tup)
        if authy_status:
            info_title = "- Information -"
            if update_status:
                info_text = (f"L'extraction de Scopus a été complétée pour l'année {corpus_year} "
                             f"et sauvegardée dans le fichier '{files_tup[1]}.csv'."
                             f"\n\nLes DOIs présents dans HAL ajoutés à Scopus "
                             f"ont été stockés dans le fichier '{files_tup[4]}.xlsx'."
                             f"\n\nDe plus les DOIs présents dans HAL mais inconnus de Scopus "
                             f"ont été stockés dans le fichier '{files_tup[3]}.xlsx'."
                             "\n\nL'extraction de HAL a été sauvegardée dans le fichier "
                             f"'{files_tup[2]}.xlsx'."
                             "\n\nLes fichiers sont dans le dossier "
                             f"{haltoscopus_path / Path(corpus_year)}.")
                messagebox.showinfo(info_title, info_text)
            else:
                info_text = ("L'extraction de Scopus n'a pas été modifiée "
                             f"pour l'année {corpus_year} "
                             f"mais elle est sauvegardée dans le fichier '{files_tup[1]}.csv'."
                             f"\n\nAucun des DOIs présents dans HAL n'a été ajouté à Scopus "
                             f"et le fichier '{files_tup[4]}.xlsx' est vide."
                             f"\n\nLes DOIs présents dans HAL mais inconnus de Scopus "
                             f"ont été stockés dans le fichier '{files_tup[3]}.xlsx'."
                             "\n\nL'extraction de HAL a été sauvegardée "
                             f"dans le fichier '{files_tup[2]}.xlsx'."
                             "\n\nLes fichiers sont dans le dossier "
                             f"{haltoscopus_path / Path(corpus_year)}.")
                messagebox.showinfo(info_title, info_text)
        else:
            info_title = "- ATTENTION -"
            info_text  = "!! L'autentification par Scopus a échoué !!"
            messagebox.showwarning(info_title, info_text)
    else:
        # Arrêt de la procédure
        info_title = "- Information -"
        info_text = "La consolidation de Scopus à été abandonnée."
        messagebox.showwarning(info_title, info_text)


def create_consolidate_scopus(self, institute, haltoscopus_path, parent):
    """
    Description : function working as a bridge between the HalToScopus 
    App and the functionalities needed for the use of the app
    
    Args : takes only self and haltoscopus_path as arguments. 
    self is the intense in which PageThree will be created
    haltoscopus_path is a type Path, and is the path to where the folders
    organised in a very specific way are stored.
    """

    # Internal functions
    def _launch_update_scopus_try():
        # Getting year selection
        year_select = variable_years.get()

        # Setting useful aliases
        init_scopus_file_alias = year_select + hts_pg.FILES_BASE["scopus_base"]
        new_scopus_file_alias = year_select + hts_pg.FILES_BASE["new_scopus_base"]
        hal_file_alias = year_select + hts_pg.FILES_BASE["hal_base"]
        failed_file_alias = year_select + hts_pg.FILES_BASE["failed_doi_base"]
        added_file_alias = year_select + hts_pg.FILES_BASE["added_doi_base"]
        files_tup = (init_scopus_file_alias, new_scopus_file_alias,
                     hal_file_alias, failed_file_alias, added_file_alias)

        # Setting working folder path
        year_haltoscopus_path = haltoscopus_path / Path(year_select)

        # Cheking availability of Scopus file
        init_scopus_file_path = year_haltoscopus_path / Path(init_scopus_file_alias + ".csv")
        scopus_file_status = os.path.exists(init_scopus_file_path)
        if scopus_file_status:
            _launch_update_scopus(institute,
                                  haltoscopus_path,
                                  year_select,
                                  files_tup,)
        else:
            warning_title = "!!! ATTENTION : fichier non disponible !!!"
            warning_text  = (f"Le fichier {files_tup[0]}.csv' d'extraction de Scopus "
                             f"\nn'est pas disponible à l'emplacement attendu."
                             f"\n1- Mettez le fichier dans le dossier : "
                             f"\n {year_haltoscopus_path} ;"
                             f"\n2- Puis relancez consolidation de Scopus.")
            messagebox.showwarning(warning_title, warning_text)


    def _launch_exit():
        message =  ("Vous allez fermer HalToScopus. "
                    "\nRien ne sera perdu et vous pourrez reprendre le traitement plus tard."
                    "\n\nSouhaitez-vous faire une pause dans le traitement ?")
        answer_1 = messagebox.askokcancel('Information', message)
        if answer_1:
            parent.destroy()

    # Setting effective font sizes and positions (numbers are reference values in mm)
    eff_buttons_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-3, parent.width_sf_min)
    eff_select_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-2, parent.width_sf_min)
    eff_etape_font_size = font_size(gg.REF_ETAPE_FONT_SIZE, parent.width_sf_min)
    eff_help_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-2, parent.width_sf_min)
    eff_launch_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-1, parent.width_sf_min)
    etape_label_format = 'left'
    etape_underline = -1
    year_button_x_pos = mm_to_px(gg.REF_YEAR_BUT_POS_X_MM * parent.width_sf_mm, gg.PPI)
    year_button_y_pos = mm_to_px(gg.REF_YEAR_BUT_POS_Y_MM * parent.height_sf_mm, gg.PPI)
    dy_year = -6
    ds_year = 5
    scopus_update_x_pos_px = mm_to_px(10 * parent.width_sf_mm, gg.PPI)
    scopus_update_y_pos_px = mm_to_px(50 * parent.height_sf_mm, gg.PPI)
    launch_dx_px = mm_to_px(0 * parent.width_sf_mm, gg.PPI)
    launch_dy_px = mm_to_px(5 * parent.height_sf_mm, gg.PPI)
    exit_button_x_pos_px = mm_to_px(gg.REF_EXIT_BUT_POS_X_MM * parent.width_sf_mm, gg.PPI)
    exit_button_y_pos_px = mm_to_px(gg.REF_EXIT_BUT_POS_Y_MM * parent.height_sf_mm, gg.PPI)

    # == Décoration de la page
    # - Canvas
    fond = tk.Canvas(self,
                     width=parent.win_width_px,
                     height=parent.win_height_px)
    fond.place(x = 0, y = 0)

    ### Choix de l'année
    years_list = last_available_years(haltoscopus_path, gg.CORPUSES_NUMBER)
    default_year = years_list[-1]
    variable_years = tk.StringVar(self)
    variable_years.set(default_year)

    # Création de l'option button des années
    self.font_OptionButton_years = tkFont.Font(family=gg.FONT_NAME,
                                               size=eff_buttons_font_size)
    self.OptionButton_years = tk.OptionMenu(self,
                                            variable_years,
                                            *years_list)
    self.OptionButton_years.config(font=self.font_OptionButton_years)

    # Création du label
    self.font_Label_years = tkFont.Font(family=gg.FONT_NAME,
                                        size=eff_select_font_size)
    self.Label_years = tk.Label(self,
                                text=gg.TEXT_YEAR,
                                font=self.font_Label_years)
    self.Label_years.place(x=year_button_x_pos, y=year_button_y_pos)

    place_after(self.Label_years, self.OptionButton_years, dy=dy_year)
    set_frame_rl(fond, self.Label_years, self.OptionButton_years, ds=ds_year)

    # ==================== Consolidation de scopus

    # == Titre
    scopus_update_font = tkFont.Font(family=gg.FONT_NAME,
                                     size=eff_etape_font_size,
                                     weight='bold')
    scopus_update_label = tk.Label(self,
                                   text=gg.TEXT_ETAPE_1,
                                   justify=etape_label_format,
                                   font=scopus_update_font,
                                   underline=etape_underline)

    scopus_update_label.place(x=scopus_update_x_pos_px,
                              y=scopus_update_y_pos_px)

    # == Explication
    help_label_font = tkFont.Font(family=gg.FONT_NAME,
                                  size=eff_help_font_size)
    help_label = tk.Label(self,
                          text=gg.HELP_ETAPE_1,
                          justify="left",
                          font=help_label_font)
    place_bellow(scopus_update_label,
                 help_label)

    # == Bouton pour lancer l'étape
    scopus_update_launch_font = tkFont.Font(family=gg.FONT_NAME,
                                        size=eff_launch_font_size)
    scopus_update_launch_button = tk.Button(self,
                                        text=gg.TEXT_MAJ_SCOPUS,
                                        font=scopus_update_launch_font,
                                        command=lambda: _launch_update_scopus_try())
    place_bellow(help_label,
                 scopus_update_launch_button,
                 dx=launch_dx_px,
                 dy=launch_dy_px)

    # ======================= Bouton pour sortir de la page
    font_button_quit = tkFont.Font(family=gg.FONT_NAME,
                                   size=eff_buttons_font_size)
    tk.Button(self,
              text=gg.TEXT_PAUSE,
              font=font_button_quit,
              command=lambda: _launch_exit()).place(x=exit_button_x_pos_px,
                                            y=exit_button_y_pos_px,
                                            anchor='n')
