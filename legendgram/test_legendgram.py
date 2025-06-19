import pytest

import matplotlib as mpl
mpl.use("pdf")
import matplotlib.pyplot as plt

import geopandas
import libpysal.examples as examples
from mapclassify import Quantiles
import numpy as np
from palettable import matplotlib as mplpal

from .legendgram import legendgram
from .util import inv_lut


class Test_Legendgram:
    def setup_method(self):
        self.data = geopandas.read_file(examples.get_path('south.shp'))
        self.test_attribute = 'HR70'
        self.k = 10
        self.breaks = Quantiles(self.data[self.test_attribute].values, k=self.k).bins
        self.pal = mplpal.Inferno_10
        self.cmap = mplpal.Inferno_10.get_mpl_colormap()

    def genframe(self, f=None, ax=None, cmap="inferno"):
        if not f:
            f, ax = plt.subplots()
        self.data.plot(self.test_attribute, scheme='Quantiles',
                        k=self.k, cmap=cmap, ax=ax)
        return f,ax

    def test_call(self):
        f, ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          breaks=self.breaks, pal=self.pal, f=f, ax=ax)
        plt.close(f)

    def test_positioning(self):
        """
        Check that changing the locstring changes the location of the plot.
        Also, check that all strings & ints are able to be used.
        """

        bboxes = []
        for i in range(1,11):
            f,ax = self.genframe()
            aout = legendgram(self.data[self.test_attribute].values,
                              breaks=self.breaks, pal=self.pal, loc=i, f=f, ax=ax)
            f2,ax2 = self.genframe()
            aout2 = legendgram(self.data[self.test_attribute].values, loc=inv_lut[i],
                               breaks=self.breaks, pal=self.pal, f=f2, ax=ax2)
            print(i,inv_lut[i])
            bbox = aout.get_position()
            bbox2 = aout2.get_position()
            print(bbox, bbox2)
            np.testing.assert_allclose(bbox.bounds, bbox2.bounds)
            bboxes.append(bbox)
            plt.close(f)
            plt.close(f2)
        for i in range(len(bboxes)-1):
            assert bboxes[i].bounds != bboxes[i+1].bounds
        f,ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          breaks=self.breaks, pal=self.pal, loc=0, f=f, ax=ax)
        bestbbox = aout.get_position()
        print(bestbbox.bounds, bboxes[2].bounds)
        np.testing.assert_allclose(bestbbox.bounds, bboxes[2].bounds) #best == bottom left

    def test_tickparams(self):
        f,ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values, breaks=self.breaks,
                          pal=self.pal, tick_params=dict(labelsize=20), f=f, ax=ax)
        ticks = aout.get_xticklabels()
        for tick in ticks:
            assert tick.get_fontsize() == 20
        plt.close(f)

    def test_frameon(self):
        f,ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          breaks=self.breaks, pal=self.pal, frameon=True, f=f, ax=ax)
        assert aout.get_frame_on()
        plt.close(f)

        f,ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          breaks=self.breaks, pal=self.pal, frameon=False, f=f, ax=ax)
        assert not aout.get_frame_on()
        plt.close(f)

    @pytest.mark.skip('Not sure how to test this')
    def test_sizing(self):
        raise NotImplementedError('Not sure how to test this yet...')

    @pytest.mark.skip('this should test that loc=[*subax_corner, *subax_dimension] passes through make_location unphased.')
    def test_passthrough_sizing(self):
        raise NotImplementedError('this should test that loc=[*subax_corner, *subax_dimension] passes through make_location unphased.')

    def test_clip(self):
        f,ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          breaks=self.breaks, pal=self.pal, clip=(10,20), f=f, ax=ax)
        assert aout.get_xlim() == (10,20)

    def test_palettebreak_mismatch(self):
        f,ax = self.genframe()
        with pytest.raises(AssertionError):
            legendgram(self.data[self.test_attribute].values,
                       breaks=self.breaks, pal=mplpal.Inferno_12, f=f, ax=ax)

    def test_matplotlib_cmap(self):
        f,ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          self.breaks, pal=self.cmap, f=f, ax=ax)
        plt.close(f)

    def test_pal_typeerror(self):
        f,ax = self.genframe()
        with pytest.raises(ValueError):
            legendgram(self.data[self.test_attribute].values,
                       breaks=self.breaks, pal='pal', f=f, ax=ax)

    def test_no_previous_cmap_from_ax(self):
        f, ax = plt.subplots()

        with pytest.warns(
            UserWarning, match="There is no data associated with the `ax`",
        ):
            aout = legendgram(self.data[self.test_attribute].values,
                            self.breaks, pal=None, f=f, ax=ax)
        plt.close(f)

    def test_one_previous_cmap_from_ax(self):
        f, ax = self.genframe()
        aout = legendgram(self.data[self.test_attribute].values,
                          self.breaks, pal=None, f=f, ax=ax)
        plt.close(f)

    def test_two_previous_cmaps_from_ax(self):
        f, ax = self.genframe()
        f, ax = self.genframe(f=f, ax=ax, cmap="twilight")

        with pytest.warns(
            UserWarning,
            match=(
                "There are 2 unique colormaps associated with"
                "the axes. Defaulting to last colormap: 'twilight'"
            ),
        ):
            aout = legendgram(self.data[self.test_attribute].values,
                            self.breaks, pal=None, f=f, ax=ax)
        plt.close(f)
