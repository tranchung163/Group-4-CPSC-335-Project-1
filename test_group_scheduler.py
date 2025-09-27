"""
Simple Test file for Group Schedule Matching Problem
Names: Ananya Karthi, Ricardo Pena, Steven Solorzano, Ngoc Chung Tran
"""

import unittest
from group_scheduler import (
    to_minute, to_regular_time, merge_closed_intervals,
    meeting_coordinator_dict
)


class TestBasicFunctions(unittest.TestCase):
    """Test basic helper functions"""
    
    def test_to_minute(self):
        """Test time to minute conversion"""
        self.assertEqual(to_minute("00:00"), 0)
        self.assertEqual(to_minute("09:30"), 570)
        self.assertEqual(to_minute("12:00"), 720)
        self.assertEqual(to_minute("23:59"), 1439)
    
    def test_to_regular_time(self):
        """Test minute to time conversion"""
        self.assertEqual(to_regular_time(0), "00:00")
        self.assertEqual(to_regular_time(570), "09:30")
        self.assertEqual(to_regular_time(720), "12:00")
        self.assertEqual(to_regular_time(1439), "23:59")
    
    def test_merge_intervals(self):
        """Test interval merging"""
        # No overlap
        intervals = [(100, 150), (200, 250)]
        result = merge_closed_intervals(intervals)
        self.assertEqual(result, [(100, 150), (200, 250)])
        
        # Overlapping
        intervals = [(100, 150), (140, 200)]
        result = merge_closed_intervals(intervals)
        self.assertEqual(result, [(100, 200)])


class TestMeetingCoordinator(unittest.TestCase):
    """Test the main meeting coordinator function"""
    
    def test_basic_example(self):
        """Test with the basic example from assignment"""
        schedules = {
            "person1": [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']],
            "person2": [['9:00', '10:30'], ['12:20', '14:00'], ['14:30', '15:00'], ['16:00', '17:00']]
        }
        active = {
            "person1": ['9:00', '19:00'],
            "person2": ['9:00', '18:30']
        }
        
        result = meeting_coordinator_dict(schedules, active, 30)
        
        # Check expected output (adjusted for closed intervals)
        expected = [['10:31', '11:59'], ['15:01', '15:59'], ['18:01', '18:30']]
        self.assertEqual(result["common_meeting_windows"], expected)
        
        # Check structure
        self.assertIn("members", result)
        self.assertIn("free_by_member", result)
        self.assertIn("common_meeting_windows", result)
    
    def test_single_person(self):
        """Test with one person"""
        schedules = {
            "alice": [['12:00', '13:00']]
        }
        active = {
            "alice": ['9:00', '18:00']
        }
        
        result = meeting_coordinator_dict(schedules, active, 60)
        
        # Should have free time before and after lunch
        self.assertGreater(len(result["common_meeting_windows"]), 0)
        self.assertEqual(len(result["members"]), 1)
    
    def test_no_common_time(self):
        """Test when no common time exists"""
        schedules = {
            "person1": [['9:00', '18:00']],  # Busy all day
            "person2": [['8:00', '19:00']]   # Busy longer
        }
        active = {
            "person1": ['9:00', '18:00'],
            "person2": ['9:00', '18:00']
        }
        
        result = meeting_coordinator_dict(schedules, active, 30)
        self.assertEqual(result["common_meeting_windows"], [])
    
    def test_three_people(self):
        """Test with three people"""
        schedules = {
            "alice": [['10:00', '11:00']],
            "bob": [['11:30', '12:30']],
            "charlie": [['14:00', '15:00']]
        }
        active = {
            "alice": ['9:00', '18:00'],
            "bob": ['9:00', '18:00'],
            "charlie": ['9:00', '18:00']
        }
        
        result = meeting_coordinator_dict(schedules, active, 30)
        
        # Should find some common times
        self.assertEqual(len(result["members"]), 3)
        self.assertGreater(len(result["common_meeting_windows"]), 0)
    
    def test_different_durations(self):
        """Test with different meeting durations"""
        schedules = {
            "person1": [['10:00', '10:15']],
            "person2": [['10:30', '11:00']]
        }
        active = {
            "person1": ['9:00', '12:00'],
            "person2": ['9:00', '12:00']
        }
        
        # Short meeting should find more slots
        result_15 = meeting_coordinator_dict(schedules, active, 15)
        
        # Long meeting should find fewer slots
        result_60 = meeting_coordinator_dict(schedules, active, 60)
        
        self.assertGreaterEqual(len(result_15["common_meeting_windows"]), 
                              len(result_60["common_meeting_windows"]))
    
    def test_error_handling(self):
        """Test error when members don't match"""
        schedules = {
            "person1": [['12:00', '13:00']],
            "person2": [['14:00', '15:00']]
        }
        active = {
            "person1": ['9:00', '18:00']
            # Missing person2
        }
        
        with self.assertRaises(ValueError):
            meeting_coordinator_dict(schedules, active, 30)


if __name__ == '__main__':
    unittest.main()