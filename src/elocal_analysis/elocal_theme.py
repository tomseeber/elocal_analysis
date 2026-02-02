import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Define eLocal brand colors (hex codes) – inspired by eLocal's logo/branding
ELOCAL_BLUE   = "#003366"  # deep navy blue (primary brand color)
ELOCAL_ORANGE = "#F05A28"  # bright orange (accent color, used for calls-to-action)
ELOCAL_GREEN  = "#4CAF50"  # green accent (used in branding for "local" theme)

# Create a categorical palette of brand colors for qualitative data
ELOCAL_PALETTE = [ELOCAL_BLUE, ELOCAL_ORANGE, ELOCAL_GREEN]
# (Optional) If more colors are needed for multiple categories, you could extend this list 
# with tints or analogous colors that complement the brand palette.

# Create a sequential colormap for continuous data (light to brand blue)
ELOCAL_SEQ_CMAP = sns.light_palette(ELOCAL_BLUE, as_cmap=True)
# Register the colormap with matplotlib for global use
plt.register_cmap(name="elocal_seq", cmap=ELOCAL_SEQ_CMAP)

# Define custom rc (runtime configuration) parameters for the theme
ELOCAL_RC = {
    # Figure and layout
    "figure.figsize": (16, 9),        # 16:9 aspect ratio, in inches
    # "figure.dpi": 100,              # Optional: DPI for higher resolution (uncomment to set)
    
    # Font settings
    "font.family": "sans-serif",      
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Sans-serif"],
    "axes.titlesize": 18,            # large title font for presentations
    "axes.titleweight": "bold",      # bold titles for emphasis
    "axes.labelsize": 14,            # x/y label font size
    "axes.labelweight": "semibold",  # semi-bold axis labels
    "xtick.labelsize": 12,           # tick label font sizes
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "legend.title_fontsize": 14,
    
    # Axes and grid styling
    "axes.edgecolor": "#333333",     # dark gray for axis spines (matches text better than black)
    "axes.linewidth": 1.0,           # spine line width
    "axes.spines.top": False,        # remove top spine
    "axes.spines.right": False,      # remove right spine
    "axes.grid": True,               # enable grid
    "axes.grid.axis": "y",           # horizontal grid lines only
    "axes.grid.which": "major",      # major grid lines only
    "grid.color": "#e5e5e5",         # light gray grid lines
    "grid.linestyle": "-",           # solid grid lines (could use '--' for dashed)
    "grid.linewidth": 0.5,           # thin grid lines
    "xtick.major.size": 5,           # tick length (for visibility)
    "xtick.major.width": 1,
    "ytick.major.size": 5,
    "ytick.major.width": 1,
    
    # Color map for heatmaps/contours
    "image.cmap": "elocal_seq"       # default colormap for imshow/heatmap (uses our registered cmap)
}

def set_elocal_theme():
    """
    Apply the eLocal-themed seaborn style to the current environment.
    This sets the theme with eLocal branding – including color palette, font, 
    and axis styles – for all subsequent Seaborn/Matplotlib plots.
    """
    # Set Seaborn theme with our parameters. We base it on 'whitegrid' style for a clean look.
    sns.set_theme(context="talk", style="whitegrid", palette=ELOCAL_PALETTE, rc=ELOCAL_RC)
    # Note: context="talk" scales up the fonts for better readability (suitable for presentations).
    # The rc parameters defined in ELOCAL_RC will override parts of the style and context as needed.
