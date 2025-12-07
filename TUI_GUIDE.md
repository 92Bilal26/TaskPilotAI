# TaskPilotAI Interactive TUI Guide

**Terminal User Interface (TUI)** - Beautiful interactive menu-driven system for managing tasks

---

## 🚀 Quick Start (30 seconds)

### Run the Interactive UI

```bash
cd /home/bilal/TaskPilotAI
/home/bilal/.local/bin/uv run python -m src.tui
```

That's it! You'll see a beautiful menu with all options.

---

## 📋 Menu Options Explained

### Main Menu Structure

```
🎯 TASKPILOTAI - Interactive Task Manager

📋 MAIN MENU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1️⃣  Add New Task
  2️⃣  View All Tasks (Table)
  3️⃣  View All Tasks (JSON)
  4️⃣  View Pending Tasks
  5️⃣  View Completed Tasks
  6️⃣  Update Task
  7️⃣  Mark Task Complete/Pending
  8️⃣  Delete Task
  9️⃣  View Statistics
  0️⃣  Exit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ✨ Feature Walkthrough

### Feature 1️⃣: Add New Task

**Menu**: Press `1`

**What it does**: Create a new task with title and optional description

**Steps**:
1. Enter task title (required, 1-200 characters)
2. Enter description (optional, press Enter to skip)
3. See confirmation with task ID and details

**Example**:
```
➕ ADD NEW TASK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Enter task title (1-200 characters): Buy groceries
📄 Enter task description (optional, max 1000 chars, press Enter to skip): Milk, eggs, bread

======================================================================
✅ SUCCESS! Task 1 added
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: ⏳ Pending
  Created: 2025-12-07T10:30:45.123456Z
======================================================================
```

---

### Feature 2️⃣: View All Tasks (Table)

**Menu**: Press `2`

**What it does**: Display all tasks in a nice table format

**Display**:
```
📋 ALL TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID    | Title                 | Status      | Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1     | Buy groceries         | ⏳ Pending   | 2025-12-07
2     | Call dentist          | ✅ Completed| 2025-12-07
3     | Fix authentication    | ⏳ Pending   | 2025-12-06
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Features**:
- ✅ Easy to read table format
- ✅ Shows ID, Title, Status, Created date
- ✅ Status icons: ⏳ (Pending) or ✅ (Completed)

---

### Feature 3️⃣: View All Tasks (JSON)

**Menu**: Press `3`

**What it does**: Display tasks in JSON format (for programmatic use)

**Display**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-07T10:30:45.123456Z",
    "updated_at": "2025-12-07T10:30:45.123456Z"
  },
  {
    "id": 2,
    "title": "Call dentist",
    "description": "",
    "completed": true,
    "created_at": "2025-12-07T14:00:00.000000Z",
    "updated_at": "2025-12-07T15:30:00.000000Z"
  }
]
```

**Why useful**: Export data, integrate with other apps, backup tasks

---

### Feature 4️⃣: View Pending Tasks

**Menu**: Press `4`

**What it does**: Show only tasks that are NOT completed

**Display**:
```
⏳ PENDING TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID    | Title                 | Status      | Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1     | Buy groceries         | ⏳ Pending   | 2025-12-07
3     | Fix authentication    | ⏳ Pending   | 2025-12-06
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Feature 5️⃣: View Completed Tasks

**Menu**: Press `5`

**What it does**: Show only tasks that ARE completed

**Display**:
```
✅ COMPLETED TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID    | Title                 | Status        | Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2     | Call dentist          | ✅ Completed  | 2025-12-07
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Feature 6️⃣: Update Task

**Menu**: Press `6`

**What it does**: Modify task title and/or description

**Steps**:
1. View current tasks (displayed automatically)
2. Enter task ID to update
3. Enter new title (press Enter to keep current)
4. Enter new description (press Enter to keep current)
5. See confirmation

**Example**:
```
✏️  UPDATE TASK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Current Tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID    | Title           | Status      | Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1     | Buy groceries   | ⏳ Pending   | 2025-12-07
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔢 Enter task ID to update: 1
📝 Enter new title (press Enter to keep current): Buy groceries and fruits
📄 Enter new description (press Enter to keep current): Fresh organic produce

======================================================================
✅ SUCCESS! Task 1 updated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ID: 1
  Title: Buy groceries and fruits
  Description: Fresh organic produce
  Updated: 2025-12-07T11:45:30.654321Z
======================================================================
```

---

### Feature 7️⃣: Mark Task Complete/Pending

**Menu**: Press `7`

**What it does**: Toggle task status (pending ↔ completed)

**Steps**:
1. View current tasks
2. Enter task ID to toggle
3. See status change confirmation

**Example**:
```
🎯 TOGGLE TASK STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Current Tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID    | Title           | Status      | Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1     | Buy groceries   | ⏳ Pending   | 2025-12-07
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔢 Enter task ID to toggle: 1

======================================================================
✅ SUCCESS! Task 1 status changed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ID: 1
  Title: Buy groceries and fruits
  New Status: ✅ Completed
  Updated: 2025-12-07T12:00:15.789012Z
======================================================================
```

---

### Feature 8️⃣: Delete Task

**Menu**: Press `8`

**What it does**: Permanently remove a task (with confirmation)

**Steps**:
1. View current tasks
2. Enter task ID to delete
3. Confirm deletion (type "yes")
4. Task is deleted

**Example**:
```
🗑️  DELETE TASK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Current Tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID    | Title           | Status      | Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1     | Buy groceries   | ✅ Completed| 2025-12-07
2     | Call dentist    | ⏳ Pending   | 2025-12-07
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔢 Enter task ID to delete: 2
⚠️  Are you sure you want to delete task 2? (yes/no): yes

======================================================================
✅ SUCCESS! Task 2 deleted
======================================================================
```

---

### Feature 9️⃣: View Statistics

**Menu**: Press `9`

**What it does**: Show task summary with completion progress

**Display**:
```
📊 TASK STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Task Summary:
  Total Tasks:      5
  ⏳ Pending:       2
  ✅ Completed:     3
  Progress:         60.0% complete
  [██████░░░░] 60%

⏳ Pending Tasks:
  • Task 1: Buy groceries
  • Task 3: Fix authentication

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Shows**:
- 📊 Total tasks
- ⏳ Pending count
- ✅ Completed count
- 📈 Completion percentage
- 📊 Progress bar
- 📋 List of pending tasks

---

## 🎮 Complete Demo Sequence

Follow this to see all features in action:

```bash
cd /home/bilal/TaskPilotAI
/home/bilal/.local/bin/uv run python -m src.tui
```

**Then do this in the menu**:

1. **Press 1** → Add task "Buy groceries" with description "Milk, eggs, bread"
2. **Press 1** → Add task "Call dentist"
3. **Press 1** → Add task "Fix authentication"
4. **Press 2** → View all tasks (see 3 tasks in table)
5. **Press 9** → View statistics (shows 0% complete)
6. **Press 7** → Mark task 1 complete
7. **Press 9** → View statistics again (shows 33% complete)
8. **Press 4** → View pending tasks (only 2 left)
9. **Press 5** → View completed tasks (shows task 1)
10. **Press 6** → Update task 2 title to "Call dentist and check teeth"
11. **Press 3** → View all tasks as JSON
12. **Press 8** → Delete task 3
13. **Press 2** → Final view of remaining tasks
14. **Press 0** → Exit

---

## 🎨 UI Features

### Beautiful Design Elements

- 🎯 **Header**: Shows app title with emojis
- 📋 **Menu**: Numbered options with emoji indicators
- 📌 **Tables**: Clean table format with separators
- ✅ **Icons**: Visual indicators for status
- 📊 **Progress**: Progress bar for statistics
- ⚠️ **Warnings**: Confirmation for destructive actions
- ❌ **Errors**: Clear error messages
- ✅ **Success**: Confirmation messages with details

### Screen Clearing

- Screen automatically clears between actions
- Clean, distraction-free interface
- "Press Enter to continue" for review

---

## 💡 Tips & Tricks

### Faster Navigation
- Numbers are single digit (0-9)
- No need to press Enter after some inputs
- Just type and press Enter

### Data Safety
- Deletion requires confirmation (type "yes")
- Updates show before/after comparison
- No data lost between operations

### Task Management
- Use statistics to track progress
- Filter by status to focus on pending work
- Update titles to clarify task goals
- IDs never change (unique identifiers)

---

## ⚡ Keyboard Shortcuts

While in menu:
- Press `1-9` for features
- Press `0` to exit
- Press `Enter` at prompts to skip optional fields
- Type `yes` to confirm deletions

---

## 🐛 Error Handling

If you see errors:

| Error | Reason | Solution |
|-------|--------|----------|
| "Invalid choice" | Pressed invalid key | Press 0-9 only |
| "Title cannot be empty" | No title provided | Enter at least 1 character |
| "Task ID not found" | Wrong task ID | View tasks first, use correct ID |
| "Invalid task ID" | Non-numeric ID | Enter numbers only |

---

## 📱 Terminal Requirements

- **Terminal**: Any terminal (bash, zsh, cmd)
- **Size**: Works best at 80+ characters wide
- **Colors**: Uses emojis (requires UTF-8 support)
- **Features**: No special requirements

---

## 🚀 Run TUI with One Command

Just copy and paste this:

```bash
cd /home/bilal/TaskPilotAI && /home/bilal/.local/bin/uv run python -m src.tui
```

---

## 📹 Recording Demo Video

To record your demo:

1. Run the TUI
2. Perform 2-3 operations showing all 5 features
3. Record <90 seconds
4. Upload to YouTube
5. Link in hackathon form

---

**Enjoy using TaskPilotAI! 🎯**
