# flask_app/core/services/planning_service.py

import datetime
from flask_app.core.utils.logger import log_info, log_error

class PlanningService:
    def __init__(self):
        # Store tasks as dict: {task_id: {goal, timeline, checkpoints, status}}
        self.tasks = {}

    def create_task(self, task_id, goal, timeline_days, checkpoints):
        """
        Initialize a new task with goal, timeline in days, and checkpoints list.

        Args:
            task_id (str): Unique identifier for the task.
            goal (str): High-level goal description.
            timeline_days (int): Deadline in days from now.
            checkpoints (list of dict): Each checkpoint {id, description, completed=False}.
        """
        deadline = datetime.datetime.now() + datetime.timedelta(days=timeline_days)
        self.tasks[task_id] = {
            "goal": goal,
            "deadline": deadline,
            "checkpoints": checkpoints,
            "status": "in-progress",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        }
        log_info(f"Task {task_id} created with deadline {deadline} and checkpoints {checkpoints}")

    def update_checkpoint(self, task_id, checkpoint_id, completed=True):
        """
        Update completion status of a checkpoint.

        Args:
            task_id (str)
            checkpoint_id (str)
            completed (bool): Mark checkpoint done or not.
        """
        try:
            checkpoints = self.tasks[task_id]["checkpoints"]
            for cp in checkpoints:
                if cp["id"] == checkpoint_id:
                    cp["completed"] = completed
                    self.tasks[task_id]["updated_at"] = datetime.datetime.now()
                    log_info(f"Checkpoint {checkpoint_id} for task {task_id} marked {'completed' if completed else 'incomplete'}.")
                    break
        except KeyError:
            log_error(f"Task or checkpoint not found for {task_id}, {checkpoint_id}")

    def check_progress(self, task_id):
        """
        Check how many checkpoints are completed vs total.

        Returns:
            dict: {completed: int, total: int, percentage: float}
        """
        try:
            checkpoints = self.tasks[task_id]["checkpoints"]
            completed = sum(1 for cp in checkpoints if cp.get("completed"))
            total = len(checkpoints)
            percentage = (completed / total * 100) if total > 0 else 0.0
            return {"completed": completed, "total": total, "percentage": percentage}
        except KeyError:
            log_error(f"Task {task_id} not found for progress check")
            return {"completed": 0, "total": 0, "percentage": 0.0}

    def is_task_complete(self, task_id, threshold=90):
        """
        Determine if task is complete based on checkpoint completion threshold (%).

        Args:
            threshold (int): Minimum percent completion for success.

        Returns:
            bool
        """
        progress = self.check_progress(task_id)
        if progress["percentage"] >= threshold:
            self.tasks[task_id]["status"] = "completed"
            log_info(f"Task {task_id} marked completed.")
            return True
        return False

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def remove_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            log_info(f"Task {task_id} removed.")

