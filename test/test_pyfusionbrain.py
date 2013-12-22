import random
import unittest
import time
from pyfusionbrain.pyfusionbrain import FusionBrainV3


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.fb = FusionBrainV3()

    def test_sequence(self):
        states = [True]*12
        self.fb.set_outputs(states)
        time.sleep(1)
        self.fb.set_outputs([False]*12)
        time.sleep(1)
        for i in range(0,12):
            self.fb.set_output(i, True)
            time.sleep(1)
        time.sleep(10)

if __name__ == '__main__':
    unittest.main()