# Group-4-CPSC-335-Project-1
# CPSC 335 - Project 1: Algorithm Design and Analysis

**Group 4 Members:**
- Ananya Karthi (akarthi@csu.fullerton.edu)
- Ricardo Pena (pena_ricky@csu.fullerton.edu)
- Steven Solorzano
- Ngoc Chung Tran (ntran562@csu.fullerton.edu)

## Project Overview

This project implements and analyzes two fundamental algorithms: the Alternating Disk Problem and the Group Schedule Matching Problem. Both algorithms demonstrate different approaches to solving optimization and coordination problems with detailed complexity analysis.

## Algorithms Implemented

### Algorithm 1: Alternating Disk Problem

**Problem Statement:**
Given a list of 2n disks alternating between light and dark (starting with light), rearrange them so all dark disks come first, followed by all light disks, using the minimum number of adjacent swaps.

**Approach:**
- Bidirectional bubble sort implementation
- Left-to-right pass followed by right-to-left pass
- Continues until no more swaps are needed

**Time Complexity:** O(n²)
**Space Complexity:** O(1)

**Key Features:**
- Tracks the number of swaps performed
- Uses bidirectional sorting for efficiency
- Handles edge cases for small inputs

### Algorithm 2: Group Schedule Matching

**Problem Statement:**
Find common available time slots for multiple group members given their busy schedules and daily availability windows.

**Approach:**
- Convert time formats to minutes for easier computation
- Merge overlapping busy intervals for each member
- Compute free time intervals within daily availability
- Find intersection of all members' free time
- Filter results by minimum meeting duration

**Time Complexity:** O(k log k) where k is the number of busy intervals
**Space Complexity:** O(k)

**Key Features:**
- Handles multiple group members
- Supports flexible time formats (HH:MM)
- Efficiently computes interval intersections
- Filters results by minimum duration requirements

## File Structure

```
project1/
├── README.md
├── alternating_disks.py
├── group_scheduler.py
├── test_alternating_disks.py
├── test_group_scheduler.py
└── report.pdf
```

## Usage Instructions

### Alternating Disk Problem

```python
from alternating_disks import AlternatingDisks

# Example usage
n = 4  # Number of disk pairs
disks = ['L', 'D', 'L', 'D', 'L', 'D', 'L', 'D']  # Initial alternating pattern

result_disks, num_swaps = AlternatingDisks(n, disks)
print(f"Final arrangement: {result_disks}")
print(f"Number of swaps: {num_swaps}")
```

### Group Schedule Matching

```python
from group_scheduler import meetingCoordinator

# Example usage
schedules = {
    'person1': [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']],
    'person2': [['9:00', '10:30'], ['12:20', '14:00'], ['14:30', '15:00'], ['16:00', '17:00']]
}

active_times = {
    'person1': ['9:00', '19:00'],
    'person2': ['9:00', '18:30']
}

duration = 30  # minutes

available_slots = meetingCoordinator(schedules, active_times, duration)
print(f"Available meeting times: {available_slots}")
```

## Testing

Run the test files to verify algorithm correctness:

```bash
python test_alternating_disks.py
python test_group_scheduler.py
```

## Complexity Analysis Summary

| Algorithm | Time Complexity | Space Complexity | Best Case | Worst Case |
|-----------|----------------|------------------|-----------|------------|
| Alternating Disks | O(n²) | O(1) | O(n) | O(n²) |
| Group Scheduler | O(k log k) | O(k) | O(k) | O(k log k) |

*Where n = number of disk pairs, k = number of busy intervals*

## Implementation Details

### Alternating Disk Algorithm
- Uses bidirectional bubble sort for optimal swapping
- Each round consists of left-to-right and right-to-left passes
- Terminates when no swaps occur in a complete round
- Theoretical minimum swaps: n² for worst-case input

### Group Schedule Algorithm
- Converts time strings to minutes for efficient computation
- Merges overlapping intervals to reduce complexity
- Uses two-pointer technique for interval intersections
- Supports variable number of group members
- Returns results in sorted order

## Performance Characteristics

### Alternating Disks
- **Best Case:** Already sorted or nearly sorted - O(n)
- **Average Case:** Random arrangement - O(n²)
- **Worst Case:** Reverse sorted - O(n²)

### Group Scheduler
- **Best Case:** Few intervals, minimal overlaps - O(k)
- **Average Case:** Typical scheduling scenario - O(k log k)
- **Worst Case:** Many overlapping intervals - O(k log k)

## Known Limitations

1. **Alternating Disks:** Algorithm assumes input follows the specified alternating pattern
2. **Group Scheduler:** Assumes valid time format (HH:MM) and logical time ranges
3. Both algorithms prioritize correctness over micro-optimizations

## Future Enhancements

- Add input validation for edge cases
- Implement GUI for schedule visualization
- Add support for recurring meetings
- Optimize memory usage for large inputs

## References

- Algorithm design principles from CPSC 335 coursework
- Interval scheduling algorithms from computational geometry
- Bidirectional bubble sort optimization techniques
