"""
Sudoku Solver as a CSP Game
A Constraint Satisfaction Problem approach to solving Sudoku puzzles.
"""

class SudokuCSP:
    def __init__(self, grid):
        """Initialize the Sudoku CSP with a 9x9 grid (0 represents empty cells)."""
        self.grid = [row[:] for row in grid]  # Copy grid
        self.size = 9
        self.box_size = 3
        
    def is_valid(self, row, col, num):
        """Check if placing num at (row, col) violates constraints."""
        # Row constraint
        if num in self.grid[row]:
            return False
        
        # Column constraint
        if num in [self.grid[r][col] for r in range(self.size)]:
            return False
        
        # Box constraint (3x3 subgrid)
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] == num:
                    return False
        return True
    
    def get_domain(self, row, col):
        """Get valid domain (possible values) for a cell using constraint propagation."""
        if self.grid[row][col] != 0:
            return []
        return [num for num in range(1, 10) if self.is_valid(row, col, num)]
    
    def find_mrv_cell(self):
        """Find empty cell with Minimum Remaining Values (MRV heuristic)."""
        min_domain_size = 10
        best_cell = None
        
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    domain = self.get_domain(row, col)
                    if len(domain) < min_domain_size:
                        min_domain_size = len(domain)
                        best_cell = (row, col, domain)
        return best_cell
    
    def solve(self):
        """Solve Sudoku using backtracking with MRV and constraint propagation."""
        # Find empty cell with minimum remaining values
        result = self.find_mrv_cell()
        
        if result is None:
            return True  # All cells filled, puzzle solved
        
        row, col, domain = result
        
        if not domain:
            return False  # No valid values, backtrack
        
        # Try each value in the domain
        for num in domain:
            self.grid[row][col] = num
            
            if self.solve():
                return True
            
            # Backtrack
            self.grid[row][col] = 0
        
        return False

def display_grid(grid):
    """Display the Sudoku grid in a neat format."""
    print("\n" + "─" * 25)
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("├" + "─" * 7 + "┼" + "─" * 7 + "┼" + "─" * 7 + "┤")
        
        row_str = "│ "
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "│ "
            row_str += str(num if num != 0 else ".") + " "
        row_str += "│"
        print(row_str)
    print("─" * 25 + "\n")

def get_user_input():
    """Get user's choice for game interaction."""
    print("Options:")
    print("1. Fill/modify a cell")
    print("2. Solve automatically")
    print("3. Exit")
    return input("Choose an option (1-3): ").strip()

def main():
    """Main game loop."""
    # Sample Sudoku puzzle (0 represents empty cells)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print("=" * 25)
    print("  SUDOKU SOLVER (CSP)")
    print("=" * 25)
    print("\nInitial Puzzle:")
    display_grid(puzzle)
    
    while True:
        choice = get_user_input()
        
        if choice == "1":
            try:
                row = int(input("Enter row (1-9): ")) - 1
                col = int(input("Enter column (1-9): ")) - 1
                num = int(input("Enter number (0-9, 0 for empty): "))
                
                if 0 <= row < 9 and 0 <= col < 9 and 0 <= num <= 9:
                    puzzle[row][col] = num
                    print("\nUpdated Grid:")
                    display_grid(puzzle)
                else:
                    print("Invalid input! Use values 1-9 for position and 0-9 for number.")
            except ValueError:
                print("Invalid input! Please enter numbers only.")
        
        elif choice == "2":
            print("\nSolving using CSP with Backtracking + MRV...\n")
            solver = SudokuCSP(puzzle)
            
            if solver.solve():
                print("✓ Solved using CSP!")
                display_grid(solver.grid)
            else:
                print("✗ No solution exists for this puzzle.")
            break
        
        elif choice == "3":
            print("Thanks for playing!")
            break
        
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()