"""
Algorithm 2: Matching Group Schedules
Names: Ananya Karthi, Ricardo Pena, Steven Solorzano, Ngoc Chung Tran


"""
from typing import Dict, List, Tuple, Any 
import sys
###CONVERSION FUNCTIONS###
def to_minute(t: str) -> int: #t means time
    """
    Convert time string "HH:MM" to integer minutes since midnight

    """
    t = t.replace(" ", "") #remove white spaces in input
    hours_str, minutes_str = t.split(":") #split into hours text and minutes text
    hours, minutes = int(hours_str), int(minutes_str) #typecast to integers
    return hours * 60 + minutes #convert to minutes

def to_regular_time(m: int) -> str: #m means minutes
    """
    Convert minutes since midnight to "HH:MM" format with leading zero if needed
    """
    h = m // 60 #to get hours ex: 540 minutes is 9 hours
    mm = m % 60 #to get minutes ex: 1439 minutes = 23:59 is 59 minutes
    return f"{h:02d}:{mm:02d}" #pad with leading zeros if needed. Ex 9 becomes 09

def minutes_in_closed_interval(start_minute: int, end_minute: int) -> int:
    """
    Inclusive count of minutes in closed interval [start, end] in minutes.
    If start is greater than end return 0 because its invalid. Cant have negative time.
    """
    """ 
    Examples:   [540, 569] = 569 - 540 + 1 = 30 minutes
                [0, 1439] = 1439 - 0 + 1 = 1440 minutes
                [100, 50] = 0 because start is greater than end
                  
    """
    return max(0, end_minute - start_minute + 1) #+1 because it is inclusive

###INTERVAL OPERATIONS###
Interval = Tuple[int, int] #type alias for the interval [start, end] in int minutes

def merge_closed_intervals(intervals: List[Interval]) -> List[Interval]:
    """
    Merge a list of closed intervals [s, e] where the endpoints count.
    Touching intervals (next.start == current.end) also merge.
    Returns a sorted, disjoint intervals.
    """
    if not intervals: #if nothing to merge
        return []
    intervals = sorted(intervals) #sort intervals by start time
    out: List[Interval] = [] #initializes output list that will contain merged, non-overlapping intervals
    current_start, current_end = intervals[0] #initialize a current interval with the first interval to compare with others
    for start, end in intervals[1:]: #iteration through the rest of the intervals (from second to last)
        if start <= current_end + 1: #if the next interval starts before or exactly when the current one ends, they overlap or touch
            current_end = max(current_end, end)
            #Example: current = [10, 20], next = [15, 30] 15 <= 20 + 1 is True, so they merge and become [10, 30]
        else:
            out.append((current_start, current_end))
            current_start, current_end = start, end #If the next interval starts after current one ends, thats a gap so they dont merge
            #example current = [10, 12], next  = [14, 18] then 14 <= 12 + 1 is False, so push current [10, 12] to output and make current = [14, 18]
    out.append((current_start, current_end)) #append the last interval after the loop ends
    return out #return the merged intervals

def compute_free_intervals_within_active(active_window: Interval, busy_intervals: List[Interval]) -> List[Interval]:
    """
    Given ACTIVE WINDOW [A, B] and a list of CLOSED busy intervals, 
    return the closed free intervals inside [A, B].
    """

    A, B = active_window #unpack the active window tuple into A and B
    if A > B: #if active window is invalid/empty, there is no free time so return empty list
        return []
    
    clipped: List[Interval] = [] #list to hold busy intervals clipped to active window
    for s, e in busy_intervals: #iterate through each busy interval
        s2, e2 = max(s, A), min(e, B) #clip the busy interval to [A, B]
        # start will become s2 and end will become e2
        if s2 <= e2: #only add if the clipped interval is valid or non-empty
            clipped.append((s2, e2)) #add the clipped busy interval to the list

    merged = merge_closed_intervals(clipped) #merge the overlapping busy intervals

    free: List[Interval] = [] #initialize list to hold free intervals
    cursor = A #tracking the start of the next free gap
    for s, e in merged: #iterate through each merged busy block
        if cursor <= s - 1: #because intervals are closed, check  if there is a gap before the busy block
            free.append((cursor, s - 1)) #add the free interval to the list
            #ex: if cursor = 540 and next busy is [600,660] then set free gap to [540,599]
        cursor = max(cursor, e + 1) #advance the cursor past this busy block.
        #The first free minute after this busy block is e + 1
        #ex: if busy is [600,660] then next free minute is 661
    if cursor <= B: #after processing all the busy blocks if there is still a gap between the cursor and B (end of active window)
        free.append((cursor, B)) #append the last free interval from cursor to B
        #ex: if cursor is 1400 and B is 1439 then add [1400, 1439] to free intervals
    return free #return the list of free intervals

def intersect_closed_intervals(free_list1: List[Interval], free_list2: List[Interval]) -> List[Interval]:
    """
    Intersect two lists of closed intervals (sorted and disjoint).
    Returns CLOSED intersections; touching at one minute yields a single-minute interval.
    """
    i1 = i2 = 0 #initialize two pointers for each list
    intersections: List[Interval] = [] #initialize list to hold intersections/overlaps

    while i1 < len(free_list1) and i2 < len(free_list2): #while neither pointer has reached the end of its list
        start1, end1 = free_list1[i1] #read the current interval from the first list
        start2, end2 = free_list2[i2] #read the current interval from the second list
        
        start = max(start1, start2) #find the start of the intersection or the later start time
        end = min(end1, end2) #find the end of the intersection or the earlier end time
        if start <= end: #if they overlap or touch, equality means touching at one minute
            intersections.append((start, end)) #add the intersection to the list

        if end1 < end2: #advance the pointer of the interval that ends first
            i1 += 1 #move pointer in first list forward
        else:
            i2 += 1 #move pointer in second list forward
    return intersections

def build_free_schedule(schedule_hhmm: List[List[str]], active_window_hhmm: List[str]) -> List[Interval]:
    """
    schedule_hhmm = includes a list of busy intervals in [["HH:MM", "HH:MM"], ...] format. (closed)
    active_window_hhmm = includes the days active window in ["HH:MM", "HH:MM"] (closed)
    return: a list of free intervals located in their schedules in minutes (closed). Sorted and disjoint
    
    """

    busy_minutes = [(to_minute(start), to_minute(end)) for (start, end) in schedule_hhmm] #convert busy intervals to a list of tuples in minutes
    merged_busy = merge_closed_intervals(busy_minutes) #sorts by start and merges any overlapping or touching intervals

    A = to_minute(active_window_hhmm[0]) #convert active window to minutes using A representing start
    B = to_minute(active_window_hhmm[1]) #convert active window to minutes using B representing end
    
    free_minutes = compute_free_intervals_within_active((A, B), merged_busy) #compute free intervals using free interval function to get free time within active window
    return free_minutes #return the free intervals in minutes

def meeting_coordinator_dict(schedules_by_member: Dict[str, List[List[str]]],active_by_member: Dict[str, List[str]],meeting_duration: int) -> Dict[str, Any]:
    """
    schedules_by_member = {
        "person1": [['7:00','8:30'], ...],
        "person2": [['9:00','10:30'], ...],
        ...
    }
    active_by_member = {
        "person1": ['9:00','19:00'],
        "person2": ['9:00','18:30'],
        ...
    }
    Returns:
    {
      "members": ["person1","person2",...],
      "free_by_member": { name: [['HH:MM','HH:MM'], ...] },
      "common_meeting_windows": [['HH:MM','HH:MM'], ...]
    }
    """

    
    if set(schedules_by_member.keys()) != set(active_by_member.keys()): #check if both dictionaries have the same member keys
        missing_in_active = set(schedules_by_member) - set(active_by_member) #find keys in schedules but not in active if missing in active
        missing_in_sched  = set(active_by_member) - set(schedules_by_member) #find keys in active but not in schedules if missing in schedules
        raise ValueError(
            f"Member key mismatch. Missing in active: {sorted(missing_in_active)}; "
            f"Missing in schedules: {sorted(missing_in_sched)}"
        )

    # 1) Fix an iteration order (dicts preserve insertion order in Py3.7+)
    member_names = list(schedules_by_member.keys())

    # 2) Build FREE intervals per member (in minutes), and also keep HH:MM for reporting
    free_by_member_min: Dict[str, List[Interval]] = {}
    free_by_member_hhmm: Dict[str, List[List[str]]] = {}
    for name in member_names:
        sched  = schedules_by_member[name]
        active = active_by_member[name]
        free_min = build_free_schedule(sched, active)  # -> List[Interval] in minutes
        free_by_member_min[name] = free_min
        free_by_member_hhmm[name] = [[to_regular_time(s), to_regular_time(e)] for s, e in free_min]

    # 3) Intersect all members’ free lists (minutes)
    if not member_names:
        common_min: List[Interval] = []
    else:
        common_min = free_by_member_min[member_names[0]]
        for name in member_names[1:]:
            common_min = intersect_closed_intervals(common_min, free_by_member_min[name])
            if not common_min:
                break

    # 4) Filter by duration and convert to HH:MM
    common_hhmm: List[List[str]] = []
    for s, e in common_min:
        if minutes_in_closed_interval(s, e) >= meeting_duration:
            common_hhmm.append([to_regular_time(s), to_regular_time(e)])

    # 5) Return a HashMap result (includes optional per-member free for clarity)
    return {
        "members": member_names,
        "free_by_member": free_by_member_hhmm,           # optional but nice to show work
        "common_meeting_windows": common_hhmm,
    }

if __name__ == "__main__":
    schedules_by_member = {
        "person1": [['7:00','8:30'], ['12:00','13:00'], ['16:00','18:00']],
        "person2": [['9:00','10:30'], ['12:20','14:00'], ['14:30','15:00'], ['16:00','17:00']],
    }
    active_by_member = {
        "person1": ['9:00','19:00'],
        "person2": ['9:00','18:30'],
    }
    out = meeting_coordinator_dict(schedules_by_member, active_by_member, meeting_duration=30)
    print(out["members"])
    print(out["common_meeting_windows"])
