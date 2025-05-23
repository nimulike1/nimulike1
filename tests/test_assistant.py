import unittest
from unittest.mock import patch
import io # For capturing print output
import sys # For restoring stdout
from contextlib import redirect_stdout

# Add src directory to sys.path to allow importing main
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import Assistant # Assuming your Assistant class is in main.py

class TestAssistant(unittest.TestCase):

    def setUp(self):
        self.assistant = Assistant()
        # Suppress print statements during most tests for cleaner output
        # unless specifically testing print output
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def test_initialization(self):
        self.assertIsNotNone(self.assistant)
        self.assertTrue("plan_travel" in self.assistant.commands)
        self.assertTrue("set_reminder" in self.assistant.commands)
        self.assertTrue("create_mind_map" in self.assistant.commands)

    @patch('builtins.input', side_effect=['Test Destination', '2024-01-01', '2024-01-05'])
    def test_plan_travel_and_view(self, mock_input):
        # Test adding a travel plan
        # Since plan_travel now can take args, and NLP might pass them, 
        # we call it without args to test the input() path.
        self.assistant.plan_travel({}) 
        self.assertEqual(len(self.assistant.travel_plans), 1)
        self.assertEqual(self.assistant.travel_plans[0]['destination'], 'Test Destination')

        # Test viewing travel plans
        f = io.StringIO()
        with redirect_stdout(f):
            self.assistant.view_travel_plans()
        output = f.getvalue()
        self.assertIn("Test Destination", output)
        self.assertIn("2024-01-01", output)

    @patch('builtins.input', side_effect=['Test Reminder', 'Tomorrow 10am'])
    def test_set_reminder_and_view(self, mock_input):
        # Test setting a reminder
        # Similar to plan_travel, call with empty dict to test input()
        self.assistant.set_reminder({})
        self.assertEqual(len(self.assistant.reminders), 1)
        self.assertEqual(self.assistant.reminders[0]['message'], 'Test Reminder')

        # Test viewing reminders
        f = io.StringIO()
        with redirect_stdout(f):
            self.assistant.view_reminders()
        output = f.getvalue()
        self.assertIn("Test Reminder", output)
        self.assertIn("Tomorrow 10am", output)

    @patch('builtins.input', side_effect=['My Test Map'])
    def test_create_mind_map_and_view(self, mock_input):
        # Test creating a mind map
        self.assistant.create_mind_map() # Uses mock_input for map name via input()
        self.assertTrue("My Test Map" in self.assistant.mind_maps)
        self.assertEqual(self.assistant.mind_maps["My Test Map"]["root"]["text"], "My Test Map")

        # Test viewing the mind map
        f = io.StringIO()
        with redirect_stdout(f):
             # view_mind_map can take args from NLP, or use input()
             # Here, we test it by providing args directly
             self.assistant.view_mind_map(args=["My", "Test", "Map"])
        output = f.getvalue()
        self.assertIn("Mind Map: My Test Map", output)
        self.assertIn("- My Test Map", output)
        
    @patch('builtins.input', side_effect=['My Test Map', 'My Test Map', 'New Node'])
    def test_add_mind_map_node(self, mock_input):
        # First, create a map. Use direct arg passing for simplicity here.
        self.assistant.create_mind_map(args=["My", "Test", "Map"])
        
        # Now, add a node. Input sequence for input() calls within add_mind_map_node:
        # 1. Map name ('My Test Map')
        # 2. Parent node text ('My Test Map' - for root)
        # 3. New node text ('New Node')
        self.assistant.add_mind_map_node()
        
        map_data = self.assistant.mind_maps.get("My Test Map")
        self.assertIsNotNone(map_data)
        self.assertEqual(len(map_data["root"]["children"]), 1)
        self.assertEqual(map_data["root"]["children"][0]["text"], "New Node")

    # Test NLP intent recognition
    
    @patch.object(Assistant, 'plan_travel')
    def test_handle_command_plan_travel_intent(self, mock_plan_travel):
        sys.stdout = self.held_stdout 
        self.assistant.handle_command("plan a new trip to Paris for next week")
        # Check that it's called, and with a dictionary (even if empty or with partial data)
        mock_plan_travel.assert_called_once()
        call_args = mock_plan_travel.call_args[0][0]
        self.assertIsInstance(call_args, dict)
        self.assertIn("paris", call_args.get("destination","").lower())


    @patch.object(Assistant, 'set_reminder')
    def test_handle_command_set_reminder_intent(self, mock_set_reminder):
        sys.stdout = self.held_stdout
        self.assistant.handle_command("remind me to buy milk tomorrow")
        mock_set_reminder.assert_called_once()
        call_args = mock_set_reminder.call_args[0][0]
        self.assertIsInstance(call_args, dict)
        self.assertIn("buy milk", call_args.get("message","").lower())
        self.assertIn("tomorrow", call_args.get("time_str","").lower())


    @patch.object(Assistant, 'create_mind_map')
    def test_handle_command_create_mind_map_intent(self, mock_create_mind_map):
        sys.stdout = self.held_stdout
        self.assistant.handle_command("create a mind map for my project")
        # The argument passed to create_mind_map should be a list of strings (words of the name)
        # or None if no name is extracted.
        mock_create_mind_map.assert_called_once()
        call_args = mock_create_mind_map.call_args[0][0] # First positional argument
        self.assertIsInstance(call_args, list) 
        self.assertEqual(call_args, ["my", "project"])
        
    @patch.object(Assistant, 'show_help')
    def test_handle_command_help_intent(self, mock_show_help):
        sys.stdout = self.held_stdout
        self.assistant.handle_command("help me with this app")
        mock_show_help.assert_called_once()

if __name__ == '__main__':
    unittest.main()
