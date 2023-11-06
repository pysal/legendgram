import warnings

from matplotlib import colormaps as cm
from matplotlib.axes._axes import Axes
from matplotlib.collections import Collection
from matplotlib.colors import ListedColormap

loc_lut = {'best'         : 0,
            'upper right'  : 1,
            'upper left'   : 2,
            'lower left'   : 3,
            'lower right'  : 4,
            'right'        : 5, 
            'center left'  : 6,
            'center right' : 7,
            'lower center' : 8,
            'upper center' : 9,
            'center'       : 10}
inv_lut = {v:k for k,v in loc_lut.items()} #yes, it's not general, but it's ok.

def make_location(ax,loc, legend_size=(.27,.2)):
    """
    Construct the location bounds of a legendgram

    Arguments:
    ----------
    ax          :   matplotlib.AxesSubplot
                    axis on which to add a legendgram
    loc         :   string or int
                    valid legend location like that used in matplotlib.pyplot.legend
    legend_size :   tuple or float
                    tuple denoting the length/width of the legendgram in terms
                    of a fraction of the axis. If a float, the legend is assumed
                    square. 

    Returns
    -------
    a list [left_anchor, bottom_anchor, width, height] in terms of plot units
    that defines the location and extent of the legendgram.


    """
    if isinstance(loc, (list, tuple)):
        assert len(loc) == 4
        return loc
    position = ax.get_position()
    if isinstance(legend_size, float):
        legend_size = (legend_size, legend_size)
    lw, lh = legend_size
    legend_width = position.width * lw
    legend_height = position.height * lh
    right_offset = (position.width - legend_width)
    top_offset = (position.height - legend_height)
    if isinstance(loc, int):
        try:
            loc = inv_lut[loc]
        except KeyError:
            raise KeyError('Legend location {} not recognized. Please choose '
                           ' from the list of valid matplotlib legend locations.'
                           ''.format(loc))
    if loc.lower() == 'lower left' or loc.lower() == 'best':
        anchor_x, anchor_y = position.x0, position.y0
    elif loc.lower() == 'lower center':
        anchor_x, anchor_y = position.x0 + position.width*.5, position.y0
    elif loc.lower() == 'lower right':
        anchor_x, anchor_y = position.x0 + right_offset, position.y0
    elif loc.lower() == 'center left':
        anchor_x, anchor_y = position.x0, position.y0 + position.height * .5
    elif loc.lower() == 'center':
        anchor_x, anchor_y = position.x0 + position.width * .5, position.y0 + position.height*.5
    elif loc.lower() == 'center right' or loc.lower()=='right':
        anchor_x, anchor_y = position.x0 + right_offset, position.y0 + position.height*.5
    elif loc.lower() == 'upper left':
        anchor_x, anchor_y = position.x0, position.y0 + top_offset
    elif loc.lower() == 'upper center':
        anchor_x, anchor_y = position.x0 + position.width * .5, position.y0 + top_offset
    elif loc.lower() == 'upper right':
        anchor_x, anchor_y = position.x0 + right_offset, position.y0 + top_offset
    return [anchor_x, anchor_y, legend_width, legend_height]


def _get_cmap(_ax: Axes) -> ListedColormap:
    """Detect the most recent matplotlib colormap used, if previously rendered."""
    _child_cmaps = [
        (cc.cmap, cc.cmap.name) for cc
        in _ax.properties()["children"]
        if isinstance(cc, Collection)
    ]
    has_child_cmaps = len(_child_cmaps)
    n_unique_cmaps = len(set(cc[1] for cc in _child_cmaps))
    if has_child_cmaps:
        cmap, cmap_name = _child_cmaps[-1]
        if n_unique_cmaps > 1:
            warnings.warn(
                (
                    f"There are {n_unique_cmaps} unique colormaps associated with"
                    f"the axes. Defaulting to last colormap: '{cmap_name}'"
                ),
                UserWarning,
                stacklevel=2
            )
    else:
        warnings.warn(
            "There is no data associated with the `ax`.",
            UserWarning,
            stacklevel=2
        )
        cmap = cm.get_cmap("viridis")
    return cmap