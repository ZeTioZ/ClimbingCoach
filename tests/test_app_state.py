import unittest
from unittest.mock import MagicMock
# move dir to src
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from gui.app_state import AppState

class TestRunPage(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.parent = MagicMock()
        self.state = AppState(self.parent, self.app)

    def test_get_camera_name(self):
        self.assertEqual(self.state.get_camera_name(), None)
    
    def test_get_index_camera(self):
        self.assertEqual(self.state.get_index_camera(), "0")
    
    def test_set_camera_name(self):
        self.state.set_camera_name("test")
        self.assertEqual(self.state.get_camera_name(), "test")