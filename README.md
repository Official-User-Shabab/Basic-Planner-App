# Basic-Planner-App

A simple desktop planner application built with **Python** and **Tkinter**. This app allows you to manage your tasks and events with due dates, save them to a file, and mark them as complete, intended for organisation.

## Features

  - **Add Tasks**: Easily add new tasks or events with a title and a due date.
  - **Due Date Picker**: A simple calendar pop-up makes it easy to select due dates.
  - **Mark as Complete**: Toggle a task's status between done and not done, with completed tasks visually marked.
  - **Delete Tasks**: Remove tasks you no longer need.
  - **Persistent Storage**: All your tasks are automatically saved to a local file (`planner.txt`), so they're there the next time you open the app.
  - **Automatic Sorting**: Tasks are sorted by their due date, with completed tasks moved to the bottom of the list.
  - **Dark Mode**: A clean, dark interface.

---

## How to Use

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/Official-User-Shabab/Basic-Planner-App
    ```

2.  **Run the Application**:
    Ensure you have Python installed then run the script from your terminal:

    ```bash
    python planner.py
    ```

3.  **Add a New Task**:

      - Enter the task's **title** in the "Task/Event Title" field.
      - Use the "Due Date" entry to type in a date in **DD-MM-YYYY** format, or click the "📅" button to select a date from the calendar.
      - Click **"Add to Planner"** to save your task.

4.  **Manage Tasks**:

      - Select a task from the list.
      - Click **"Mark as Done / Restore"** to toggle its completion status. Completed tasks will have a strikethrough effect.
      - Click **"Delete"** to permanently remove the selected task.

---

## Requirements

The application uses standard Python libraries, so no additional installation is needed. You just need **Python 3.13.5** installed on your system.

```bash
python --version
```

---

## Code Structure

  - `planner.py`: The main Python script containing the `PlannerApp` class and the `DatePopup` class.
      - `PlannerApp`: A class handling the main GUI, task management, and file operations.
      - `DatePopup`: A class for top-level window for the date-picking functionality.
  - `planner.txt`: The text file where your tasks are saved. It's automatically created when you add your first task.

---

## Customising

You can easily customise the app's appearance by modifying the constants at the top of the `planner.py` file:

  - `STOREFILE`: Change the name of the file where data is stored.
  - `FONT_FAMILY`: Choose a different font.
  - `BG_COLOR`, `FRAME_COLOR`, `BUTTON_COLOR`, etc : Adjust the color scheme to your liking.
