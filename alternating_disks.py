"""
Algorithm 1: Sort Disks
Names: Ananya Karthi, Ricardo Pena, Steven Solorzano, Ngoc Chung Tran


"""

from typing import List, Tuple
import sys

#function to check user input
def ask_user_for_input(prompt: str = "Enter n (number of pairs): ") -> int:
    """
    Will ask the user for input until a valid integer n >= 1 is provided.
    Returns the integer n. 
    
    """
    while True:
        try:
            value = input(prompt)
        except (EOFError, KeyboardInterrupt): #interuption force closes the program
            print("\nInput interrupted. Exiting.")
            sys.exit(1)
        value = value.strip() #removes leading and trailing whitespace

        if not value or not value.isdigit(): #checks if input is empty or not a digit
            print("Invalid input. Please enter a positive integer.")
            continue
        
        number = int(value) #integer typecast
        if number < 1:
            print("Invalid input. Please enter an integer greater than or equal to 1.")
            continue
        return number

#added this function to generate an alternating list to place L in even and D in odd indices according to the prompt
def make_alternating(n: int) -> List[str]:
    return ['L' if i % 2 == 0 else 'D' for i in range(2 * n)] #place L in even slots else place d in odds.

def sort_disks(n: int, disks: List[str]) -> Tuple[List[str], int]:
    """
   Sort disks so that entries labled 'D' are all at the front of the list, followed by 'L'
   using only adjacent swaps.
   Returns (reordered-list, m) where m is the amount of swaps it took to reorder the list.
  
    Input:
        n   - number of disk pairs (total disks = 2n)
        disks- list of 2n disks that alternate and start with 'L'
    Output:
        (disks, m) - ordered list and amount of swaps performed
   """
    assert n >= 1 and len(disks) == 2 * n, "Input must contain exactly 2n disks and n must be greater than or equal to 1."

    m = 0 #swap count
    step = 0 #steps to show evolution
    sorted_flag = False #flag to check if sorted
    round_no = 0  #counts rounds of passes left to right and right to left is 1 round

    print(f"Start: {' '.join(disks)}")

    while not sorted_flag:
        round_no += 1 #round starts at 1
        sorted_flag = True

        # Pass from left to right
        print(f"\nRound {round_no}: Left → Right pass")
        for i in range(0,2*n-1):  #from index 0 all the way to 2n-2 index
            if disks[i] == 'L' and disks[i + 1] == 'D': #check left and right
                disks[i], disks[i + 1] = disks[i + 1], disks[i] #swap
                m += 1 #increment swap count
                step += 1 #increment step count
                sorted_flag = False #if a swap occurs then not sorted yet
                print(f"[{step}] swap at index({i},{i+1})  →  {' '.join(disks)}") #prints the current step, where changes occured, and current list

        # Pass from right to left
        print(f"Round {round_no}: Right ← Left pass")
        for i in range(2*n-1,0,-1):  #from index 2n-1 down to index 1
            if disks[i - 1] == 'L' and disks[i] == 'D': #check left and right
                disks[i - 1], disks[i] = disks[i], disks[i - 1] #swap
                m += 1
                step += 1
                sorted_flag = False
                print(f"[{step}] swap at index ({i-1},{i})  →  {' '.join(disks)}")

        if sorted_flag: #if no swaps occurred in both passes, then the list is finally sorted
            print(f"\nNo swaps in Round {round_no}. List is properly partitioned.")

    print(f"\nDone:  {' '.join(disks)}") #prints final state
    print(f"Total swaps: {m}") #prints total swaps
    return disks, m #return the sorted array and amount of swaps


if __name__ == "__main__":
    #Ask only for n; auto-generate alternating L D input as required by assignment prompt
    n = ask_user_for_input("Enter n (number of pairs): ")
    disks = make_alternating(n)
    sort_disks(n, disks)

    """ 
        Added print statements to track every transformation and removed 
        the user input of alternating disks since we assume the disks will be alternating
        starting with L as per the prompt. Also added input checking incase user does not input
        a proper value to easily cycle until a valid input is given.
        
    """
