"""Sets globals for GUI."""

__all__ = ['ADD_SPACE_MM',
           'BM_GUI_DISP',
           'CONTAINER_BUTTON_HEIGHT_PX',
           'CORPUSES_NUMBER',
           'FONT_NAME',
           'IN_TO_MM',
           'PAGES_LABELS',
           'PPI',
           'REF_SEF_FONT_SIZE',
           'REF_SEF_POS_X_MM',
           'REF_SEF_POS_Y_MM',
           'REF_BUTTON_DX_MM',
           'REF_BUTTON_DY_MM',
           'REF_BUTTON_FONT_SIZE',
           'REF_COPYRIGHT_FONT_SIZE',
           'REF_COPYRIGHT_X_MM',
           'REF_COPYRIGHT_Y_MM',
           'REF_ENTRY_NB_CHAR',
           'REF_EXIT_BUT_POS_X_MM',
           'REF_EXIT_BUT_POS_Y_MM',
           'REF_INST_POS_X_MM',
           'REF_INST_POS_Y_MM',
           'REF_LABEL_FONT_SIZE',
           'REF_LABEL_POS_Y_MM',
           'REF_LAUNCH_FONT_SIZE',
           'REF_PAGE_TITLE_FONT_SIZE',
           'REF_PAGE_TITLE_POS_Y_MM',
           'REF_SCREEN_WIDTH_PX',
           'REF_SCREEN_HEIGHT_PX',
           'REF_SCREEN_WIDTH_MM',
           'REF_SCREEN_HEIGHT_MM',
           'REF_SUB_TITLE_FONT_SIZE',
           'REF_WINDOW_WIDTH_MM',
           'REF_WINDOW_HEIGHT_MM',
           'REF_VERSION_FONT_SIZE',
           'REF_VERSION_X_MM',
           'REF_YEAR_BUT_POS_X_MM',
           'REF_YEAR_BUT_POS_Y_MM',
           'TEXT_SEF',
           'TEXT_SEF_CHANGE',
           'TEXT_BOUTON_LANCEMENT',
           'TEXT_COPYRIGHT',
           'TEXT_INSTITUTE',
           'TEXT_PAUSE',
           'TEXT_TITLE',
           'TEXT_VERSION',
           'TEXT_YEAR',
           'TEXT_ETAPE_1',
           'HELP_ETAPE_1',
           'TEXT_MAJ_SCOPUS',
           ]


# Standard library imports
import math

# 3rd party imports
from screeninfo import get_monitors

# ========================= General globals =========================

# Setting BiblioMeter version value (internal)
VERSION ='1.0.0'

# Setting the number of corpuses to analyse
CORPUSES_NUMBER = 10

# Setting the title of the application main window (internal)
APPLICATION_WINDOW_TITLE = ("HalToScopus - Consolidation des extractions "
                            "Scopus et HAL d'un institut")

# ================== Definition of display globals ==================

def _get_displays(in_to_mm):
    """The function `get_displays` allows to identify the set of displays
    available within the user hardware and to get their parameters.

    If the width or the height of a display are not available in mm 
    through the `get_monitors` method (as for Darwin platforms), 
    the user is asked to specify the displays diagonal size to compute them.

    Args:
        in_to_mm (float): Factor of conversion from inches to millimeters.
    Returns:
        (list): List of dicts with one dict per detected display, \
        each dict is keyed by 8 display parameters.   
    """
    # To Do: convert prints and inputs to gui displays and inputs

    displays = [{'x':m.x,'y':m.y,'width':m.width,
                 'height':m.height,'width_mm':m.width_mm,
                 'height_mm':m.height_mm,'name':m.name,
                 'is_primary':m.is_primary} for m in get_monitors()]

    for disp, _ in enumerate(displays):
        width_px = displays[disp]['width']
        height_px = displays[disp]['height']
        diag_px = math.sqrt(int(width_px)**2 + int(height_px)**2)
        width_mm = displays[disp]['width_mm']
        height_mm = displays[disp]['height_mm']
        if width_mm is None or height_mm is None:
            diag_in = float(input('Enter the diagonal size of the screen n°' \
                                  + str(disp) + ' (inches)'))
            width_mm = round(int(width_px) * (diag_in/diag_px) * in_to_mm,1)
            height_mm = round(int(height_px) * (diag_in/diag_px) * in_to_mm,1)
            displays[disp]['width_mm'] = str(width_mm)
            displays[disp]['height_mm'] = str(height_mm)
        else:
            diag_in = math.sqrt(float(width_mm) ** 2 + float(height_mm) ** 2) / in_to_mm
        displays[disp]['ppi'] = round(diag_px/diag_in,2)

    return displays

# Conversion factor for inch to millimeter
IN_TO_MM = 25.4

DISPLAYS = _get_displays(IN_TO_MM)

# Setting primary display
BM_GUI_DISP = 0

# Getting display resolution in pixels per inch
PPI = DISPLAYS[BM_GUI_DISP]['ppi']

# Setting display reference sizes in pixels and mm (internal)
REF_SCREEN_WIDTH_PX = 1920
REF_SCREEN_HEIGHT_PX = 1080
REF_SCREEN_WIDTH_MM = 467
REF_SCREEN_HEIGHT_MM = 267

# Application window reference sizes in mm for the display
# reference sizes (internal)
REF_WINDOW_WIDTH_MM = 219
REF_WINDOW_HEIGHT_MM = 173


# ===================================================================
# ========================== Pages globals ==========================
# ===================================================================


# Setting general globals for text edition
FONT_NAME = "Helvetica"

# ================= Reference coordinates for pages =================

# Number of characters reference for editing the entered files-folder path
REF_ENTRY_NB_CHAR = 100

# Font size references for page label and button
REF_SUB_TITLE_FONT_SIZE = 15
REF_PAGE_TITLE_FONT_SIZE = 30
REF_LAUNCH_FONT_SIZE = 25
REF_SEF_FONT_SIZE = 15
REF_BUTTON_FONT_SIZE = 12
REF_COPYRIGHT_FONT_SIZE = 12
REF_VERSION_FONT_SIZE = 12

# Y position reference in mm for page label
REF_PAGE_TITLE_POS_Y_MM = 20

# Positions reference in mm for institute selection button
REF_INST_POS_X_MM = 5
REF_INST_POS_Y_MM = 40

# Positions reference in mm for bmf label and button
REF_SEF_POS_X_MM = 5
REF_SEF_POS_Y_MM = 55
REF_BUTTON_DX_MM = -147
REF_BUTTON_DY_MM = 10

# Space between label and value
ADD_SPACE_MM = 10

# Setting X and Y positions reference in mm for copyright
REF_COPYRIGHT_X_MM = 5
REF_COPYRIGHT_Y_MM = 170
REF_VERSION_X_MM = 185

# Container button height in pixels
CONTAINER_BUTTON_HEIGHT_PX = 50

# Font size references for page label and button
REF_LABEL_FONT_SIZE = 25
REF_ETAPE_FONT_SIZE = 14
REF_BUTTON_FONT_SIZE = 10

# Positions reference in mm for pages widgets
REF_LABEL_POS_Y_MM = 15
REF_ETAPE_POS_X_MM = 10
REF_ETAPE_POS_Y_MM_LIST = [40, 74, 101, 129]
REF_ETAPE_BUT_DX_MM = 10
REF_ETAPE_BUT_DY_MM = 5
REF_ETAPE_CHECK_DY_MM = -8
REF_EXIT_BUT_POS_X_MM = 193
REF_EXIT_BUT_POS_Y_MM = 145
REF_YEAR_BUT_POS_X_MM = 10
REF_YEAR_BUT_POS_Y_MM = 30

# Separation space in mm for check boxes
REF_CHECK_BOXES_SEP_SPACE = 25

# Setting label for each gui page
PAGES_LABELS = {'UpdateScopusPage' : "Consolidation Scopus avec HAL",
               }

# =================== Cover Page (launching Page) ===================

# Titre de la page
TEXT_TITLE = "- HalToScopus -\nInitialisation de la consolidation"

# Choix de l'année de l'Institut
TEXT_INSTITUTE = "Sélection de l'Institut"

# Titre LabelEntry of BiblioMeter_Files folder
TEXT_SEF = "Dossier de travail "

# Titre bouton changement de dossier de travail
TEXT_SEF_CHANGE = "Changer de dossier de travail"

# Titre bouton de lancement
TEXT_BOUTON_LANCEMENT = "Lancer la consolidation"

# Copyright and contacts
TEXT_COPYRIGHT  =   "Contributeurs et contacts :"
TEXT_COPYRIGHT +=  "\n- Amal Chabli : amal.chabli@orange.fr"
TEXT_COPYRIGHT +=  "\n- François Bertin : francois.bertin7@wanadoo.fr"
TEXT_COPYRIGHT +=  "\n- Ludovic Desmeuzes"
TEXT_VERSION = f"\nVersion {VERSION}"

# ========================= Secondary pages =========================

# Common to secondary pages
TEXT_PAUSE = "Mettre en pause"
TEXT_YEAR = "Sélection de l'année "

# ======================== Update Scopus page ========================

TEXT_ETAPE_1  = "Consolidation de l'extraction de Scopus"
HELP_ETAPE_1  = "Un fichier au format standard de l'extraction de Scopus "
HELP_ETAPE_1 += "\nva être construit à partir du fichier initial de l'extraction "
HELP_ETAPE_1 += "\net de l'extraction par DOI pour les DOIs complémentaires issus de HAL."
TEXT_MAJ_SCOPUS = "Lancer la consolidation de l'extraction de Scopus"
