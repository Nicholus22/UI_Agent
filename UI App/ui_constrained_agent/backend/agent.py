class TaskAgent:
    def __init__(self):
        self.state = {
            "step": "start",
            "date": None,
            "participants": [],
            "confidence": 1.0,
            "error": None
        }

    def validate_date(self, date_str):
        from datetime import datetime
        try:
            selected = datetime.strptime(date_str, "%Y-%m-%d")
            return selected >= datetime.now()
        except:
            return False

    def validate_participants(self, participants):
        return len(participants) > 0

    def next_step(self, user_input):
        step = self.state["step"]
        self.state["error"] = None  # reset previous errors

        if step == "start":
            self.state["step"] = "select_date"
            self.state["confidence"] = 0.9
            return "Select a meeting date.", self.state["confidence"]

        elif step == "select_date":
            if self.validate_date(user_input):
                self.state["date"] = user_input
                self.state["step"] = "select_participants"
                self.state["confidence"] = 0.85
                return "Add participants from the list.", self.state["confidence"]
            else:
                self.state["error"] = "Invalid date"
                self.state["confidence"] = 0.5
                return "Invalid date! Pick a future date.", self.state["confidence"]

        elif step == "select_participants":
            if self.validate_participants(user_input):
                self.state["participants"] = user_input
                self.state["step"] = "confirm"
                self.state["confidence"] = 0.95
                return "Confirm all details before booking.", self.state["confidence"]
            else:
                self.state["error"] = "No participants selected"
                self.state["confidence"] = 0.6
                return "Select at least one participant.", self.state["confidence"]

        elif step == "confirm":
            self.state["step"] = "completed"
            self.state["confidence"] = 1.0
            return "Task completed!", self.state["confidence"]

        else:
            return "Task already completed.", self.state["confidence"]
