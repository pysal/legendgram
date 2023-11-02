from .util import make_location as _make_location
from .util import _get_cmap
import numpy as np
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
from palettable.palette import Palette


def legendgram(y, breaks=None, pal=None, bins=50, clip=None,
               loc = 'lower left', legend_size=(.27,.2),
               frameon=False, tick_params = None, f=None, ax=None):
    '''
    Add a histogram in a choropleth with colors aligned with map
    ...

    Arguments
    ---------
    y           : ndarray/Series
                  Values to map
    breaks      : list or int
                  [Optional. Default=ten evenly-spaced percentiles from the 1st to the 99th]
                  Sequence with breaks for each class (i.e. boundary values
                  for colors). If an integer is supplied, this is used as the number of
                  evenly-spaced percentiles to use in the discretization 
    pal         : palettable colormap, matplotlib colormap, or str
                  palette to use to construct the legendgram. (default: None)
    clip        : tuple
                  [Optional. Default=None] If a tuple, clips the X
                  axis of the histogram to the bounds provided.
    loc         : str or int
                  valid legend location like that used in matplotlib.pyplot.legend
    legend_size : tuple
                  tuple of floats between 0 and 1 describing the (width,height)
                  of the legend relative to the original frame.
    frameon     : bool (default: False)
                  whether to add a frame to the legendgram
    tick_params : keyword dictionary
                  options to control how the histogram axis gets ticked/labelled.
    f           : Figure
    ax          : AxesSubplot

    Returns
    -------
    axis containing the legendgram.
    '''
    if f is None:
        f = plt.gcf()
    if ax is None:
        ax = plt.gca()
    if pal is None:
        pal = _get_cmap(ax)
    if breaks is None:
        breaks = 10
    if isinstance(breaks, int):
        breaks = np.percentile(y, q=np.linspace(1,99,num=breaks))
    k = len(breaks)
    histpos = _make_location(ax, loc, legend_size=legend_size)
    histax = f.add_axes(histpos)
    N, bins, patches = histax.hist(y, bins=bins, color='0.1')
    #---
    if isinstance(pal, str):
        pl = plt.get_cmap(pal)
    if isinstance(pal, Palette):
        assert k == pal.number, "provided number of classes does not match number of colors in palette."
        pl = pal.get_mpl_colormap()
    elif isinstance(pal, Colormap):
        pl = pal
    else:
        raise ValueError("pal needs to be either palettable colormap or matplotlib colormap, got {}".format(type(pal)))
    bucket_breaks = [0]+[np.searchsorted(bins, i) for i in breaks]
    for c in range(k):
        for b in range(bucket_breaks[c], bucket_breaks[c+1]):
            patches[b].set_facecolor(pl(c/k))
    #---
    if clip is not None:
        histax.set_xlim(*clip)
    histax.set_frame_on(frameon)
    histax.get_yaxis().set_visible(False)
    if tick_params is None:
        tick_params = dict()
    tick_params['labelsize'] = tick_params.get('labelsize', 12)
    histax.tick_params(**tick_params)
    return histax
