"""KM3Pipe Modules for Fluxes."""
from km3pipe import Module
from km3flux import Honda2015, HondaSarcevic


class Honda2015Mod(Module):
    """Get the Honda 2015 fluxes.

    """
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.key = self.require('key')
        self.average = self.get('average') or True
        self.honda = Honda2015()

    def process(self, blob):
        if self.key not in blob:
            return blob
        flav = blob[self.key]['flavor']
        ene = blob[self.key]['energy']
        if self.average:
            zen = None
        else:
            zen = blob[self.key]['zenith']
        blob['Honda2015'] = self.honda.get(flav, ene, zen)
        return blob


class HondaSarcevicMod(Module):
    """Get the Honda Sarcevic fluxes.
    """
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.key = self.require('key')
        self.honda = HondaSarcevic()

    def process(self, blob):
        if self.key not in blob:
            return blob
        flav = blob[self.key]['flavor']
        ene = blob[self.key]['energy']
        zen = blob[self.key]['zenith']
        blob['Honda2015'] = self.honda.get(flav, ene, zen)
        return blob
