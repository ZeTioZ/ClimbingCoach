import os
import sys
import unittest
from unittest.mock import MagicMock

from gui.app_state import AppState

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))


class TestRunPage(unittest.TestCase):
	def setUp(self):
		self.app = MagicMock()
		self.parent = MagicMock()
		self.state = AppState()

	def test_get_camera_name(self):
		self.assertEqual(self.state.get_camera_name(), None)

	def test_get_index_camera(self):
		self.assertEqual(self.state.get_index_camera(), "0")

	def test_set_camera_name(self):
		self.state.set_camera_name("test")
		self.assertEqual(self.state.get_camera_name(), "test")
