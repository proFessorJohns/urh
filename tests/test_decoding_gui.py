from PyQt5.QtCore import QPoint

from tests.QtTestCase import QtTestCase
from urh import constants
from urh.controller.DecoderWidgetController import DecoderWidgetController
from urh.signalprocessing.encoder import Encoder

class TestDecodingGUI(QtTestCase):
    def setUp(self):
        super().setUp()
        self.add_signal_to_form("esaver.complex")
        signal = self.form.signal_tab_controller.signal_frames[0].signal
        self.dialog = DecoderWidgetController(decodings=self.form.compare_frame_controller.decodings,
                                              signals=[signal], parent=self.form,
                                              project_manager=self.form.project_manager)

        if self.SHOW:
            self.dialog.show()

    def test_edit_decoding(self):
        self.dialog.ui.combobox_decodings.setCurrentIndex(1)  # NRZI
        self.assertEqual(self.dialog.ui.decoderchain.count(), 1)  # One Invert
        self.dialog.save_to_file()

    def test_build_decoding(self):
        self.dialog.ui.combobox_decodings.setCurrentIndex(4)
        chain = [constants.DECODING_INVERT, constants.DECODING_ENOCEAN, constants.DECODING_DIFFERENTIAL,
                 constants.DECODING_REDUNDANCY,
                 constants.DECODING_CARRIER, constants.DECODING_BITORDER, constants.DECODING_EDGE,
                 constants.DECODING_DATAWHITENING,
                 constants.DECODING_SUBSTITUTION, constants.DECODING_EXTERNAL, constants.DECODING_CUT]

        decoding = Encoder(chain=chain)
        self.dialog.decodings[4] = decoding
        self.dialog.set_e()

        self.assertEqual(len(chain), self.dialog.ui.decoderchain.count())

        for i in range(0, self.dialog.ui.decoderchain.count()):
            self.dialog.ui.decoderchain.setCurrentRow(i)
            self.dialog.set_information(2)
            self.assertIn(chain[i], self.dialog.ui.info.text())

    def test_set_signal(self):
        self.dialog.ui.combobox_signals.currentIndexChanged.emit(0)
        self.assertEqual(self.dialog.ui.inpt.text(), "10010110")

    def test_select_items(self):
        for i in range(0, self.dialog.ui.basefunctions.count()):
            self.dialog.ui.basefunctions.setCurrentRow(i)
            self.assertIn(self.dialog.ui.basefunctions.currentItem().text(), self.dialog.ui.info.text())

        for i in range(0, self.dialog.ui.additionalfunctions.count()):
            self.dialog.ui.additionalfunctions.setCurrentRow(i)
            self.assertIn(self.dialog.ui.additionalfunctions.currentItem().text(), self.dialog.ui.info.text())

    def test_context_menu(self):
        self.dialog.ui.combobox_decodings.setCurrentIndex(4)
        decoding = Encoder(chain=[constants.DECODING_INVERT])
        self.dialog.decodings[4] = decoding
        self.dialog.set_e()

        self.assertEqual(1, self.dialog.ui.decoderchain.count())

        self.dialog.ui.decoderchain.context_menu_pos = QPoint(0, 0)
        menu = self.dialog.ui.decoderchain.create_context_menu()
        menu_actions = [action.text() for action in menu.actions() if action.text()]
        self.assertEqual(3, len(menu_actions))
