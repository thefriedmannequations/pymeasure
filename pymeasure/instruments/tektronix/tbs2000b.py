#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.instruments import Instrument, Channel

class MeasurementChannel(Channel):
    """Represents a measurement channel on the oscilloscope."""



class TBS2XXX(Instrument):
    """Represents the Tektronix TBS 2000B series oscilloscope and provides
    a high-level interface for interacting with the instrument.
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initializer and important communication methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, adapter, name="TBS-2XXX", **kwargs):
        super().__init__(
            adapter, name, **kwargs
        )
        self.reset
        channels = Instrument.MultiChannelCreator(MeasurementChannel,
            list(range(1, self.__find_n_channels())))


    def reset(self):
        """Resets the instrument"""
        self.write("*RST")


    def __find_n_channels(self):
        """Private method. Uses the instrument's VISA ID number to determine 
        the number of channels required. Tektronix' naming convention is 
        TBS2XXNB where N is the number of channels."""

        id_list = self.id.split(',')
        n_channels = id_list[1][-1]

        return int(n_channels)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Measurements
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    id = Instrument.measurement(
        "*IDN?",
        "Get the instrument VISA ID number."
    )

    status = Instrument.measurement(
        "*ESR?",
        "Fetches the contents of the event status register."
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def auto_setup(self):
        """Automatically configures the instrument."""
        self.write("AUTOS EXEC;")
