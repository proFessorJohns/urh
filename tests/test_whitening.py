from tests.QtTestCase import QtTestCase
from urh.signalprocessing.encoder import Encoder

class TestWhitening(QtTestCase):
    def test_whitening(self):
        e = Encoder()

        # Test 1
        e.data_whitening_sync = e.hex2bit("67686768")
        original_inpt = e.hex2bit("aaaaaaaa67686768f9ca03909567ba76a8") + [False] # Korrektes Signal, bitgenau
        inpt = original_inpt.copy()
        #print (e.bit2hex(inpt))
        output, err, _ = e.apply_data_whitening(True, inpt)
        #print (e.bit2hex(output), err)
        newinpt, err, _ = e.apply_data_whitening(False, output)
        #print (e.bit2hex(newinpt), newinpt, err)
        self.assertEqual(original_inpt, newinpt)
