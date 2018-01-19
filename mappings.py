__doc__ = '''Mappings for the different tokens'''

import pdb


class Mappings(object):
    """Encodes a dictionary of visemes and phonemes, performs the different lookup"""

    def __init__(self, pdictfname='../HW3/beep-1.0', vmapfname='../HW3/woodward_d.vmap', vdictfname='../HW3/woodward_d.vdict'):
        """TODO: Docstring for __init__.

        :returns: TODO

        """
# myDict.loadVisToPhon('../HW3/woodward_d.vmap')
# myDict.loadWordToPhon('../HW3/beep-1.0')
# myDict.loadWordToVis('../HW3/woodward_d.vdict')
        self._vdict = dict() # for a given word, will encode the set of vismems that corresponds
        self._phontovis = dict() # for a given phonem, the set of visemes that corresponds
        self._vmap = dict() # for a given visem, the set of phonems that corresponds
        self._pdict = dict()
        self._pmap = dict() # the phoneme -> viseme mapping
        self.load_vmap(vmapfname)
        self.load_vdict(vdictfname)
        self.load_pdict(pdictfname)
        self.compute_pmap() # computes the mapping between phoneme and visemes
        return


    def visemeToPhonemes(self, vis):
        """The viseme to phonemes mapping"""
        return self._vmap.get(vis, ['/sil/'])

    def phonemeToViseme(self, phn):
        '''Return the viseme associated with the phoneme'''

        # we assume there is only one viseme for each phoneme

        return self._pmap.get(phn, 'gar') # the default viseme is gar when no phoneme is found




    def wordToPhonemes(self, word):
        """The viseme to phonemes mapping"""
        return self._pdict.get(word, ['/sil/'])


    def wordToVisemes(self, word):
        """The viseme to phonemes mapping"""
        return self._vdict.get(word, ['/sil/'])



    def load_vmap(self, vmapfname):
        """Loads the different visemes from a file"""
        with open(vmapfname, 'r') as file:
            for line in file:
                spline = line.strip().split(' ') # we split the line with the blank character
                self._vmap[spline[0]] = spline[1:]
        return


    def load_pdict(self, pdictfname):
        """Loads the different phonems from a file"""
        with open(pdictfname, 'r') as file:
            for line in file:
                spline = line.strip().split(' ') # we split the line with the blank character
                self._pdict[spline[0]] = spline[1:]
        return


    def load_vdict(self, vdictfname):
        """Loads the different phonems from a file"""
        with open(vdictfname, 'r') as file:
            for line in file:
                spline = line.strip().split(' ') # we split the line with the blank character
                self._vdict[spline[0]] = spline[1:]
        return

    def compute_pmap(self):
        '''Compute the (inverse) mapping phoneme -> viseme'''
        # the keys are the phonemes
        for key, value in self._vmap.items(): # key is the viseme, value is the phoneme
            for phn in value:
                self._pmap[phn] = key




