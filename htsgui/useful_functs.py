"""Tool box for GUI management."""

__all__ = ['font_size',
           'general_properties',
           'last_available_years',
           'mm_to_px',
           'place_after', 
           'place_bellow', 
           'label_entry_place_bellow',
           'str_size_mm',
           'set_frame_rl',
           'set_frame_ud',
          ]


# Standard library imports
import math
import os
from tkinter import messagebox

# Local imports
import htsgui.gui_globals as gg


def last_available_years(bibliometer_path, year_number):
    """Returns a list of the available five last available years where corpuses are stored."""
    try:
        list_dir = os.listdir(bibliometer_path)
        years_full_list = []
        for year in list_dir:
            if len(year) == 4:
                years_full_list.append(year)
        years_list = years_full_list[-year_number:]
    except FileNotFoundError:
        warning_title = "!!! ATTENTION : Dossier de travail inaccessible !!!"
        warning_text = (f"L'accès au dossier {bibliometer_path} est impossible."
                        f"\nChoisissez un autre dossier de travail.")
        messagebox.showwarning(warning_title, warning_text)
        years_list = []
    return years_list


def place_after(gauche, droite, dx = 5, dy = 0):
    """Places 'droite' widget horizontally after 'gauche' widget."""
    gauche_info = gauche.place_info()
    x = int(gauche_info['x']) + gauche.winfo_reqwidth() + dx
    y = int(gauche_info['y']) + dy
    droite.place(x=x, y=y)


def place_bellow(haut, bas, dx = 0, dy = 5):
    """Places 'bas' widget bellow 'haut' widget."""
    haut_info = haut.place_info()
    x = int(haut_info['x']) + dx
    y = int(haut_info['y']) + haut.winfo_reqheight() + dy
    bas.place(x=x, y=y)


def set_frame_rl(fond, gauche, droite, color="red", dn=10, de=10, ds=10, dw=10):
    """Places rectangular frame widget relatively to 'gauche' and 'droite' widgets."""
    gauche_info = gauche.place_info()
    droite_info = droite.place_info()

    x1 = int(gauche_info['x']) - dw
    y1 = int(gauche_info['y']) - dn

    x2 = int(gauche_info['x']) + gauche.winfo_reqwidth() + droite.winfo_reqwidth() + de
    y2 = int(droite_info['y']) + max(gauche.winfo_reqheight(), droite.winfo_reqheight()) + ds

    fond.create_rectangle(x1, y1, x2, y2, outline=color, width=2)
    fond.place(x=0, y=0)


def set_frame_ud(fond, haut, bas, color="red", dn=10, de=10, ds=10, dw=10):
    """Places rectangular frame widget relatively to 'haut' and 'bas' widgets."""
    haut_info = haut.place_info()
    bas_info = bas.place_info()

    x1 = int(haut_info['x']) - dw
    y1 = int(haut_info['y']) - dn

    x2 = int(bas_info['x']) + max(haut.winfo_reqwidth(), bas.winfo_reqwidth()) + de
    y2 = int(bas_info['y']) + haut.winfo_reqheight() + bas.winfo_reqheight() + ds

    fond.create_rectangle(x1, y1, x2, y2, outline=color, width=2)
    fond.place(x=0, y=0)


def label_entry_place_bellow(haut, label_entry, dx=0, dy=5):
    """Places label_entry widget bellow haut widget."""
    haut_info = haut.place_info()
    x = int(haut_info['x']) + dx
    y = int(haut_info['y']) + haut.winfo_reqheight() + dy
    label_entry.place(x=x, y=y)


def font_size(size, scale_factor):
    """Set the fontsize based on scale_factor.
    If the fontsize is less than minimum_size,
    it is set to the minimum size."""
    fontsize = int(size * scale_factor)
    fontsize = max(fontsize, 8)
    return fontsize


def str_size_mm(text, font, ppi):
    """The function `_str_size_mm` computes the sizes in mm of a string.

    Args:
        text (str): the text of which we compute the size in mm.
        font (tk.font): the font of the text.
        ppi (int): pixels per inch of the display.
    Returns:
        (tuple): width in mm (float), height in mm (float).
    Note:
        The use of this function requires a tkinter window availability \
        since it is based on a tkinter font definition.
    """
    (w_px,h_px) = (font.measure(text),font.metrics("linespace"))
    w_mm = w_px * gg.IN_TO_MM / ppi
    h_mm = h_px * gg.IN_TO_MM / ppi
    return (w_mm,h_mm )


def mm_to_px(size_mm, ppi, fact = 1.0):
    """The `mm_to_px' function converts a value in mm to a value in pixels 
    using the ppi of the used display and a factor fact.

    Args:
        size_mm (float): value in mm to be converted.
        ppi ( float): pixels per inch of the display.
        fact (float): factor (default= 1).
    Returns:
        (int): upper integer value of the conversion to pixels.
    """
    size_px = math.ceil((size_mm * fact / gg.IN_TO_MM) * ppi)
    return size_px


def _window_properties(screen_width_px, screen_height_px):
    # Getting number of pixels per inch screen resolution from imported global DISPLAYS
    ppi = gg.DISPLAYS[gg.BM_GUI_DISP]["ppi"]

    # Setting screen effective sizes in mm from imported global DISPLAYS
    screen_width_mm = gg.DISPLAYS[gg.BM_GUI_DISP]["width_mm"]
    screen_height_mm = gg.DISPLAYS[gg.BM_GUI_DISP]["height_mm"]

    # Setting screen reference sizes in pixels and mm
    # from globals internal to module "Coordinates.py"
    ref_width_px = gg.REF_SCREEN_WIDTH_PX
    ref_height_px = gg.REF_SCREEN_HEIGHT_PX
    ref_width_mm = gg.REF_SCREEN_WIDTH_MM
    ref_height_mm = gg.REF_SCREEN_HEIGHT_MM

    # Setting secondary window reference sizes in mm
    # from globals internal to module "Coordinates.py"
    ref_window_width_mm = gg.REF_WINDOW_WIDTH_MM
    ref_window_height_mm = gg.REF_WINDOW_HEIGHT_MM

    # Computing ratii of effective screen sizes
    # to screen reference sizes in pixels
    scale_factor_width_px = screen_width_px / ref_width_px
    scale_factor_height_px = screen_height_px / ref_height_px

    # Computing ratii of effective screen sizes
    # to screen reference sizes in mm
    scale_factor_width_mm = screen_width_mm / ref_width_mm
    scale_factor_height_mm = screen_height_mm / ref_height_mm

    # Computing secondary window sizes in pixels depending on scale factors
    win_width_px = mm_to_px(ref_window_width_mm * scale_factor_width_mm, ppi)
    win_height_px = mm_to_px(ref_window_height_mm * scale_factor_height_mm, ppi)

    sizes_tuple = (win_width_px, win_height_px,
                   scale_factor_width_px, scale_factor_height_px,
                   scale_factor_width_mm, scale_factor_height_mm)

    return sizes_tuple

def general_properties(self):
    """The function `general_properties` calculate the window sizes 
    and useful scale factors for the application launch window.
    
    For that, it uses reference values for the display sizes in pixels
    and mm through the globals:
    - "REF_SCREEN_WIDTH_PX" and "REF_SCREEN_HEIGHT_PX";
    - "REF_SCREEN_WIDTH_MM" and "REF_SCREEN_HEIGHT_MM".
    The secondary window sizes in mm are set through the globals: 
    - "REF_WINDOW_WIDTH_MM" and "REF_WINDOW_HEIGHT_MM".
    The window title is set through the global "APPLICATION_TITLE".

    Returns:
        (tuple): (self, 2 window sizes in pixels, 2 scale factors for sizes in mm \
                 and 2 scale factors for sizes in pixels).
    """
    # Getting screen effective sizes in pixels for window "root"
    # (not working for Darwin platform)
    screen_width_px = self.winfo_screenwidth()
    screen_height_px = self.winfo_screenheight()

    sizes_tuple = _window_properties(screen_width_px, screen_height_px)

    win_width_px = sizes_tuple[0]
    win_height_px = sizes_tuple[1]

    # Setting window size depending on scale factor
    self.geometry(f"{win_width_px}x{win_height_px}")
    self.resizable(False, False)

    # Setting title window
    self.title(gg.APPLICATION_WINDOW_TITLE)

    return self, sizes_tuple
