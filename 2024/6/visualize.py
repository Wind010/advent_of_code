import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from constants import OBSTACLE

def visualize_paths(grid, all_paths) -> None:
    rows, cols = len(grid), len(grid[0])
    grid_array = np.full((rows, cols), 0)  # 0 for empty spaces
    

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == OBSTACLE:
                grid_array[r, c] = 1  # Mark obstacles with 1


    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid_array, cmap="Blues", origin='upper')

    current_positions = []

    def update(frame):
        ax.clear()
        ax.imshow(grid_array, cmap="Blues", origin='upper')
        # Plot the paths up to the current frame
        for path in all_paths:
            # TODO:  Paths are not ordered in traversal manner because a set is used for all_paths.
            for pos in list(path)[:frame + 1]:
                row, col = pos
                ax.plot(col, row, marker='o', color='red', markersize=3)

        guard_row, guard_col = list(all_paths[0])[0]  # TODO:  Update for actual starting.
        ax.plot(guard_col, guard_row, marker='*', color='yellow', markersize=8, label="Guard Start")

        ax.set_xticks(np.arange(cols))
        ax.set_yticks(np.arange(rows))
        ax.set_xticklabels(np.arange(cols))
        ax.set_yticklabels(np.arange(rows))
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        ax.legend()

    num_frames = max(len(path) for path in all_paths)
    ani = FuncAnimation(fig, update, frames=num_frames, interval=500, repeat=False)


    plt.title("Guard Path Animation")
    plt.show()