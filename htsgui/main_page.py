""" The `main_page` module sets the `AppMain` class, its attributes and related secondary classes.
"""

__all__ = ['AppMain']

# Standard library imports
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font as tkFont
from functools import partial
from pathlib import Path

# 3rd party imports
from screeninfo import get_monitors

# Local imports
import htsgui.gui_globals as gg
import htsfuncts.institute_globals as ig
from htsgui.update_scopus_page import create_consolidate_scopus
from htsgui.useful_functs import font_size
from htsgui.useful_functs import general_properties
from htsgui.useful_functs import mm_to_px
from htsgui.useful_functs import place_after
from htsgui.useful_functs import str_size_mm


class AppMain(tk.Tk):
    """The class AppMain inherite the attributes and methods of "tk.Tk".

    sef stands for ScopusExtractions_Files.
    """
    # ======================== Class init - start =======================
    def __init__(self):
        # Setting the link with "tk.Tk"
        tk.Tk.__init__(self)

        # Internal functions - start
        def _display_path(inst_sef):
            """Shortening sef path for easy display""" 
            p = Path(inst_sef)
            p_disp = ('/'.join(p.parts[0:2])) / Path("...") / ('/'.join(p.parts[-3:]))
            return p_disp


        def _get_file(institute_select):
            # Getting new working directory
            dialog_title = "Choisir un nouveau dossier de travail"
            sef_str = filedialog.askdirectory(title=dialog_title)
            if sef_str=='':
                warning_title = "!!! Attention !!!"
                warning_text = "Chemin non renseigné."
                messagebox.showwarning(warning_title, warning_text)

            # Updating sef values using new working directory
            _set_sef_widget_param(institute_select, sef_str)
            _set_launch_button(institute_select, sef_str)


        def _set_sef_widget_param(institute_select, inst_sef):
            # Setting sef widgets parameters
            sef_font = tkFont.Font(family=gg.FONT_NAME,
                                   size=eff_sef_font_size,
                                   weight='bold')
            sef_label = tk.Label(self,
                                 text=gg.TEXT_SEF,
                                 font=sef_font,)
            sef_val = tk.StringVar(self)
            sef_val2 = tk.StringVar(self)
            sef_entree2 = tk.Entry(self, textvariable=sef_val2, width=eff_sef_width)
            sef_button_font = tkFont.Font(family=gg.FONT_NAME,
                                          size=eff_button_font_size)
            sef_button = tk.Button(self,
                                   text=gg.TEXT_SEF_CHANGE,
                                   font=sef_button_font,
                                   command=lambda: _get_file(institute_select))
            # Placing sef widgets
            sef_label.place(x=eff_sef_pos_x_px,
                            y=eff_sef_pos_y_px,)

            text_width_mm, _ = str_size_mm(gg.TEXT_SEF, sef_font, gg.PPI)
            eff_path_pos_x_px = mm_to_px(text_width_mm + add_space_mm, gg.PPI)
            sef_entree2.place(x=eff_path_pos_x_px,
                              y=eff_sef_pos_y_px,)

            sef_button.place(x=eff_path_pos_x_px,
                             y=eff_sef_pos_y_px + eff_button_dy_px,)
            sef_val.set(inst_sef)
            sef_val2.set((_display_path(inst_sef)))


        def _set_launch_button(institute, inst_sef):
            # Setting launch button
            launch_font = tkFont.Font(family=gg.FONT_NAME,
                                      size=eff_launch_font_size,
                                      weight='bold')
            launch_button = tk.Button(self,
                                      text=gg.TEXT_BOUTON_LANCEMENT,
                                      font=launch_font,
                                      command=lambda: self._generate_pages(institute, inst_sef))
            # Plqcing launch button
            launch_button.place(x=launch_but_pos_x_px,
                                y=launch_but_pos_y_px,
                                anchor="s")


        def _update_page(*args, widget=None):
            _ = args
            institute_select = widget.get()
            inst_default_sef = ig.WORKING_FOLDERS_DICT[institute_select]

            # Managing working folder (sef stands for "BiblioMeter_Files")
            _set_sef_widget_param(institute_select, inst_default_sef)

            # Managing analysis launch button
            _set_launch_button(institute_select, inst_default_sef)
        # ===================== Internal functions - end ====================

        # ============================== Main ===============================

        # Identifying tk window of init class
        _ = get_monitors() # OBLIGATOIRE
        #self.lift()
        self.attributes("-topmost", True)
        #self.after_idle(self.attributes,'-topmost',False)
        #self.REP = list()

        # Defining pages classes and pages list
        AppMain.pages = (UpdateScopusPage,)
        AppMain.pages_ordered_list = [x.__name__ for x in AppMain.pages][::-1]

        # Getting useful screen sizes and scale factors depending on displays properties
        self, sizes_tuple = general_properties(self)
        AppMain.win_width_px = sizes_tuple[0]
        AppMain.win_height_px = sizes_tuple[1]
        AppMain.width_sf_px = sizes_tuple[2]
        AppMain.height_sf_px = sizes_tuple[3] # unused here
        AppMain.width_sf_mm = sizes_tuple[4]
        AppMain.height_sf_mm = sizes_tuple[5]
        AppMain.width_sf_min = min(AppMain.width_sf_mm, AppMain.width_sf_px)

        # Setting common parameters for widgets
        add_space_mm = gg.ADD_SPACE_MM

        # ============== Title and copyright widgets parameters =============
        # Setting font size for page title and copyright
        eff_page_title_font_size = font_size(gg.REF_PAGE_TITLE_FONT_SIZE, AppMain.width_sf_min)

        # Setting reference Y position in mm and effective Y position in pixels for page label
        eff_page_title_pos_y_px = mm_to_px(gg.REF_PAGE_TITLE_POS_Y_MM * AppMain.height_sf_mm,
                                           gg.PPI)

        # Setting x position in pixels for page title
        mid_page_pos_x_px = AppMain.win_width_px  * 0.5

        # Setting font size for copyright
        eff_copyright_font_size = font_size(gg.REF_COPYRIGHT_FONT_SIZE, AppMain.width_sf_min)

        # Setting X and Y positions reference in mm for copyright
        eff_copyright_x_px = mm_to_px(gg.REF_COPYRIGHT_X_MM * AppMain.width_sf_mm, gg.PPI)
        eff_copyright_y_px = mm_to_px(gg.REF_COPYRIGHT_Y_MM * AppMain.height_sf_mm, gg.PPI)

        # Setting font size for version
        eff_version_font_size = font_size(gg.REF_VERSION_FONT_SIZE, AppMain.width_sf_min)

        # Setting X and Y positions reference in mm for version
        eff_version_x_px = mm_to_px(gg.REF_VERSION_X_MM * AppMain.width_sf_mm, gg.PPI)
        eff_version_y_px = mm_to_px(gg.REF_COPYRIGHT_Y_MM * AppMain.height_sf_mm, gg.PPI)

        # ============= Institute-selection widgets parameters ==============
        # Setting institut selection widgets parameters
        eff_buttons_font_size = font_size(gg.REF_BUTTON_FONT_SIZE, AppMain.width_sf_min)
        eff_select_font_size  = font_size(gg.REF_SUB_TITLE_FONT_SIZE, AppMain.width_sf_min)
        inst_button_x_pos = mm_to_px(gg.REF_INST_POS_X_MM * AppMain.width_sf_mm,  gg.PPI)
        inst_button_y_pos = mm_to_px(gg.REF_INST_POS_Y_MM * AppMain.height_sf_mm, gg.PPI)
        dy_inst = -10

        # =========== Working-folder selection widgets parameters ===========
        # Setting effective value for sef entry width
        eff_sef_width = int(gg.REF_ENTRY_NB_CHAR * AppMain.width_sf_min)

        # Setting font size for sef
        eff_sef_font_size = font_size(gg.REF_SUB_TITLE_FONT_SIZE, AppMain.width_sf_min)
        eff_button_font_size = font_size(gg.REF_BUTTON_FONT_SIZE, AppMain.width_sf_min)

        # Setting reference positions in mm and effective ones in pixels for sef
        eff_sef_pos_x_px = mm_to_px(gg.REF_SEF_POS_X_MM * AppMain.height_sf_mm, gg.PPI)
        eff_sef_pos_y_px = mm_to_px(gg.REF_SEF_POS_Y_MM * AppMain.height_sf_mm, gg.PPI)

        # Setting reference relative positions in mm and effective relative
        # X,Y positions in pixels for sef change button
        eff_button_dy_px = mm_to_px(gg.REF_BUTTON_DY_MM * AppMain.height_sf_mm, gg.PPI)

        # ===================== Launch button parameters ====================
        # Setting font size for launch button
        eff_launch_font_size = font_size(gg.REF_LAUNCH_FONT_SIZE, AppMain.width_sf_min)

        # Setting x and y position in pixels for launch button
        launch_but_pos_x_px = AppMain.win_width_px * 0.5
        launch_but_pos_y_px = AppMain.win_height_px * 0.65

        # Setting default values
        institutes_list = ig.INSTITUTES_LIST
        default_institute = "....."

        # ========================== Title - start ==========================
        page_title = tk.Label(self,
                              text=gg.TEXT_TITLE,
                              font=(gg.FONT_NAME, eff_page_title_font_size),
                              justify="center")
        page_title.place(x=mid_page_pos_x_px,
                         y=eff_page_title_pos_y_px,
                         anchor="center")
        # ========================= = Title - end  ==========================

        # ======================= Institute selection =======================
        institute_val = tk.StringVar(self)
        institute_val.set(default_institute)

        # Création de l'option button des instituts
        self.font_OptionButton_inst = tkFont.Font(family=gg.FONT_NAME,
                                                  size=eff_buttons_font_size)
        self.OptionButton_inst = tk.OptionMenu(self,
                                               institute_val,
                                               *institutes_list)
        self.OptionButton_inst.config(font=self.font_OptionButton_inst)

        # Création du label
        self.font_Label_inst = tkFont.Font(family=gg.FONT_NAME,
                                           size=eff_select_font_size,
                                           weight='bold')
        self.Label_inst = tk.Label(self,
                                   text=gg.TEXT_INSTITUTE,
                                   font=self.font_Label_inst)
        self.Label_inst.place(x=inst_button_x_pos, y=inst_button_y_pos)
        place_after(self.Label_inst, self.OptionButton_inst, dy=dy_inst)

        # Suivi de la sélection
        institute_val.trace('w', partial(_update_page, widget=institute_val))

        # ======================= Authors and version =======================
        authors_font_label = tkFont.Font(family=gg.FONT_NAME,
                                         size=eff_copyright_font_size,)
        authors_label = tk.Label(self,
                                 text=gg.TEXT_COPYRIGHT,
                                 font=authors_font_label,
                                 justify="left")
        authors_label.place(x=eff_copyright_x_px,
                            y=eff_copyright_y_px,
                            anchor="sw")

        version_font_label = tkFont.Font(family=gg.FONT_NAME,
                                         size=eff_version_font_size,
                                         weight='bold')
        version_label = tk.Label(self,
                                 text= gg.TEXT_VERSION,
                                 font=version_font_label,
                                 justify="right")
        version_label.place(x=eff_version_x_px,
                            y=eff_version_y_px,
                            anchor="sw")

    # ======================== Class init - end =========================

    # ================  Class internal functions - start ================
    def _generate_pages(self, institute, haltoscopus_path):
        """Permet la génération des pages après spécification du chemin 
        vers la zone de stockage.

        Vérifie qu'un chemin a été renseigné et continue le cas échéant, 
        sinon redemande de renseigner un chemin.
        """
        if haltoscopus_path=='':
            warning_title = "!!! Attention !!!"
            warning_text = ("Chemin non renseigné."
                            "\nL'application ne peut pas être lancée."
                            "\nVeuillez le définir.")
            messagebox.showwarning(warning_title, warning_text)

        else:
            # Creating two frames in the tk window
            container_button = tk.Frame(self,
                                        height=gg.CONTAINER_BUTTON_HEIGHT_PX,
                                        bg='red')
            container_button.pack(side="top",
                                  fill="both",
                                  expand=False)

            container_frame = tk.Frame(self)
            container_frame.pack(side="top",
                                 fill="both",
                                 expand=True)
            container_frame.grid_rowconfigure(0,
                                              weight=1)
            container_frame.grid_columnconfigure(0,
                                                 weight=1)

            self.frames = {}
            for page in AppMain.pages:
                page_name = page.__name__
                frame = page(parent=container_frame,
                             controller=self,
                             container_button=container_button,
                             institute=institute,
                             haltoscopus_path=haltoscopus_path)
                self.frames[page_name] = frame

                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                frame.grid(row=0,
                           column=0,
                           sticky="nsew")

    def _show_frame(self, page_name):
        """Show a frame for the given page name."""        
        frame = self.frames[page_name]
        frame.tkraise()


class UpdateScopusPage(tk.Frame):
    """Page 'Consolidation Scopus avec HAL'."""           
    def __init__(self, parent, controller, container_button, institute, haltoscopus_path):
        super().__init__(parent)
        self.controller = controller

        # Setting specific texts
        page_name = self.__class__.__name__
        page_num = AppMain.pages_ordered_list.index(page_name)
        label_text = gg.PAGES_LABELS[page_name]
        page_title = label_text + " du " + institute

        # Setting font size for page label and button
        eff_label_font_size = font_size(gg.REF_LABEL_FONT_SIZE, AppMain.width_sf_min)
        eff_button_font_size = font_size(gg.REF_BUTTON_FONT_SIZE, AppMain.width_sf_min)

        # Setting y_position in px for page label
        eff_label_pos_y_px = mm_to_px(gg.REF_LABEL_POS_Y_MM * AppMain.height_sf_mm, gg.PPI)

        # Setting x position in pixels for page label
        mid_page_pos_x_px = AppMain.win_width_px / 2

        # Creation of the class object Page 1
        create_consolidate_scopus(self, institute, haltoscopus_path, controller)

        label_font = tkFont.Font(family=gg.FONT_NAME,
                                 size=eff_label_font_size)
        label = tk.Label(self,
                         text=page_title,
                         font=label_font)
        label.place(x=mid_page_pos_x_px,
                    y=eff_label_pos_y_px,
                    anchor = "center")
        button_font = tkFont.Font(family=gg.FONT_NAME,
                                  size=eff_button_font_size)
        button = tk.Button(container_button,
                           text=label_text,
                           font=button_font,
                           command=lambda: controller._show_frame(page_name))
        button.grid(row=0, column=page_num)
