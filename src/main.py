import spacy
nlp = spacy.load("en_core_web_sm")

class Assistant:
    def __init__(self):
        self.travel_plans = []
        self.reminders = []
        self.mind_maps = {} # Stores mind maps by name
        self.commands = {
            "plan_travel": self.plan_travel,
            "view_travel_plans": self.view_travel_plans,
            "set_reminder": self.set_reminder,
            "view_reminders": self.view_reminders,
            "create_mind_map": self.create_mind_map, # Was placeholder, now to be implemented
            "add_mind_map_node": self.add_mind_map_node, # New command
            "view_mind_map": self.view_mind_map, # New command
            "help": self.show_help,
        }

    def show_help(self, args=None):
        print("Available commands:")
        for command in self.commands:
            print(f"- {command}")

    def plan_travel(self, args=None):
        print("Let's plan your travel!")
        try:
            destination = input("Enter destination: ")
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            
            # Basic validation (can be improved)
            if not destination or not start_date or not end_date:
                print("All fields are required. Travel plan not saved.")
                return

            new_plan = {
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "status": "planned" # Default status
            }
            self.travel_plans.append(new_plan)
            print(f"Travel to {destination} from {start_date} to {end_date} planned successfully!")
        except Exception as e:
            print(f"Error planning travel: {e}")

    def plan_travel(self, args=None): # args can now be a dict from NLP
        print("Let's plan your travel!")
        try:
            destination = args.get("destination") if args else None
            start_date = args.get("start_date") if args else None
            end_date = args.get("end_date") if args else None

            if not destination:
                destination = input("Enter destination: ")
            if not start_date:
                start_date = input("Enter start date (YYYY-MM-DD): ")
            if not end_date:
                end_date = input("Enter end date (YYYY-MM-DD): ")
            
            if not destination or not start_date or not end_date:
                print("All fields are required. Travel plan not saved.")
                return

            new_plan = {
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "status": "planned"
            }
            self.travel_plans.append(new_plan)
            print(f"Travel to {destination} from {start_date} to {end_date} planned successfully!")
        except Exception as e:
            print(f"Error planning travel: {e}")

    def view_travel_plans(self, args=None):
        print("\n--- Your Travel Plans ---")
        if not self.travel_plans:
            print("No travel plans yet. Use 'plan_travel' to add one.")
        else:
            for i, plan in enumerate(self.travel_plans):
                print(f"Plan {i+1}:")
                print(f"  Destination: {plan['destination']}")
                print(f"  Start Date: {plan['start_date']}")
                print(f"  End Date: {plan['end_date']}")
                print(f"  Status: {plan['status']}")
                print("-" * 20)
        print("\n")

    def set_reminder(self, args=None):
        print("Let's set a reminder!")
        try:
            message = input("Enter reminder message: ")
            time_str = input("Enter reminder time (e.g., 'tomorrow 10am' or '2024-12-31 23:59'): ")
            
            if not message or not time_str:
                print("Message and time are required. Reminder not set.")
                return

            new_reminder = {
                "message": message,
                "time_str": time_str, # Storing time as a string for now
                "status": "pending" 
            }
            self.reminders.append(new_reminder)
            print(f"Reminder '{message}' set for '{time_str}' successfully!")
        except Exception as e:
            print(f"Error setting reminder: {e}")

    def set_reminder(self, args=None): # args can now be a dict from NLP
        print("Let's set a reminder!")
        try:
            message = args.get("message") if args else None
            time_str = args.get("time_str") if args else None

            if not message:
                message = input("Enter reminder message: ")
            if not time_str:
                time_str = input("Enter reminder time (e.g., 'tomorrow 10am' or '2024-12-31 23:59'): ")
            
            if not message or not time_str:
                print("Message and time are required. Reminder not set.")
                return

            new_reminder = {
                "message": message,
                "time_str": time_str, 
                "status": "pending" 
            }
            self.reminders.append(new_reminder)
            print(f"Reminder '{message}' set for '{time_str}' successfully!")
        except Exception as e:
            print(f"Error setting reminder: {e}")

    def view_reminders(self, args=None):
        print("\n--- Your Reminders ---")
        if not self.reminders:
            print("No reminders set yet. Use 'set_reminder' to add one.")
        else:
            for i, reminder in enumerate(self.reminders):
                print(f"Reminder {i+1}:")
                print(f"  Message: {reminder['message']}")
                print(f"  Time: {reminder['time_str']}")
                print(f"  Status: {reminder['status']}")
                print("-" * 20)
        print("\n")

    def create_mind_map(self, args=None):
        map_name = ""
        if args:
            map_name = " ".join(args)
        else:
            map_name = input("Enter the name/central topic for your new mind map: ")

        if not map_name:
            print("Mind map name cannot be empty. Creation failed.")
            return

        if map_name in self.mind_maps:
            print(f"A mind map named '{map_name}' already exists.")
            return

        self.mind_maps[map_name] = {"root": {"text": map_name, "children": []}}
        print(f"Mind map '{map_name}' created successfully.")

    def _find_node_in_map(self, current_node, target_text):
        if current_node["text"] == target_text:
            return current_node
        for child in current_node["children"]:
            found = self._find_node_in_map(child, target_text)
            if found:
                return found
        return None

    def add_mind_map_node(self, args=None):
        map_name = input("Enter the name of the mind map to add a node to: ")
        if map_name not in self.mind_maps:
            print(f"Mind map '{map_name}' not found.")
            return

        parent_node_text = input("Enter the text of the parent node (or root to add to central topic): ")
        new_node_text = input("Enter the text for the new node/idea: ")

        if not new_node_text:
            print("New node text cannot be empty. Node not added.")
            return
        
        mind_map_data = self.mind_maps[map_name]
        
        parent_node = None
        if parent_node_text.lower() == "root" or parent_node_text == mind_map_data["root"]["text"]:
            parent_node = mind_map_data["root"]
        else:
            parent_node = self._find_node_in_map(mind_map_data["root"], parent_node_text)

        if not parent_node:
            print(f"Parent node '{parent_node_text}' not found in mind map '{map_name}'.")
            return

        parent_node["children"].append({"text": new_node_text, "children": []})
        print(f"Node '{new_node_text}' added to '{parent_node['text']}' in mind map '{map_name}'.")

    def _display_map_node(self, node, indent_level=0):
        indent = "  " * indent_level
        print(f"{indent}- {node['text']}")
        for child in node["children"]:
            self._display_map_node(child, indent_level + 1)

    def view_mind_map(self, args=None):
        map_name = ""
        if args:
            map_name = " ".join(args)
        else:
            map_name = input("Enter the name of the mind map to view: ")

        if not map_name:
            print("Mind map name cannot be empty.")
            return
            
        if map_name not in self.mind_maps:
            print(f"Mind map '{map_name}' not found.")
            return

        print(f"\n--- Mind Map: {map_name} ---")
        self._display_map_node(self.mind_maps[map_name]["root"])
        print("\n")

    def handle_command(self, user_input_text):
        doc = nlp(user_input_text.lower())
        
        intent = None
        args = {} # To store extracted entities like dates, destinations

        # Help intent
        if any(token.lemma_ in ["help", "assist", "guide"] for token in doc):
            intent = "help"
        
        # Travel planning intents
        elif any(token.lemma_ in ["travel", "trip", "journey", "vacation"] for token in doc) and \
             any(token.lemma_ in ["plan", "book", "organize", "new"] for token in doc):
            intent = "plan_travel"
            for ent in doc.ents:
                if ent.label_ == "GPE": 
                    args["destination"] = ent.text
                elif ent.label_ == "DATE":
                    if "start_date" not in args:
                        args["start_date"] = ent.text
                    else:
                        args["end_date"] = ent.text
        elif any(token.lemma_ in ["travel", "trip", "journey", "vacation"] for token in doc) and \
             any(token.lemma_ in ["show", "view", "list", "see", "find"] for token in doc):
            intent = "view_travel_plans"

        # Reminder intents
        elif any(token.lemma_ in ["remind", "reminder", "alert"] for token in doc) and \
             any(token.lemma_ in ["set", "add", "new", "create"] for token in doc):
            intent = "set_reminder"
            message_parts = []
            time_entity = None
            for token in doc:
                if token.lemma_ in ["remind", "me", "to"]: continue
                if token.ent_type_ == "TIME" or any(t.lemma_ in ["today", "tomorrow", "yesterday"] for t in token.subtree):
                    if not time_entity: 
                         time_entity = " ".join(t.text for t in token.subtree)
                    continue 
                message_parts.append(token.text)
            if message_parts:
                args["message"] = " ".join(message_parts).strip()
            if time_entity:
                args["time_str"] = time_entity

        elif any(token.lemma_ in ["reminder", "remind"] for token in doc) and \
             any(token.lemma_ in ["show", "view", "list", "see", "find"] for token in doc):
            intent = "view_reminders"

        # Mind map intents
        elif any(token.lemma_ in ["mindmap", "mind map", "map"] for token in doc) and \
             any(token.lemma_ in ["create", "new", "start", "make"] for token in doc):
            intent = "create_mind_map"
            name_parts = []
            for token in doc:
                if token.lemma_ not in ["mindmap", "mind", "map", "create", "new", "start", "make", "a", "an", "the"]:
                     name_parts.append(token.text)
            if name_parts:
                args["map_name"] = " ".join(name_parts).strip()

        elif any(token.lemma_ in ["mindmap", "mind map", "map"] for token in doc) and \
             any(token.lemma_ in ["add", "node", "idea"] for token in doc):
            intent = "add_mind_map_node"

        elif any(token.lemma_ in ["mindmap", "mind map", "map"] for token in doc) and \
             any(token.lemma_ in ["show", "view", "display", "open"] for token in doc):
            intent = "view_mind_map"
            name_parts = []
            for token in doc:
                if token.lemma_ not in ["mindmap", "mind", "map", "show", "view", "display", "open", "a", "an", "the"]:
                     name_parts.append(token.text)
            if name_parts:
                args["map_name"] = " ".join(name_parts).strip()


        if intent and intent in self.commands:
            print(f"... Detected intent: {intent} with args: {args}")
            if intent == "plan_travel": 
                self.commands[intent](args) # Pass NLP args
            elif intent == "set_reminder": 
                 self.commands[intent](args) # Pass NLP args
            elif intent == "create_mind_map":
                self.commands[intent](args.get("map_name", "").split() if args.get("map_name") else None)
            elif intent == "view_mind_map":
                self.commands[intent](args.get("map_name", "").split() if args.get("map_name") else None)
            elif intent == "add_mind_map_node": 
                self.commands[intent]() # No NLP args for now
            else: 
                self.commands[intent](args if args else None)
        else:
            print(f"Sorry, I didn't understand that. Try 'help' for available commands.")

if __name__ == "__main__":
    assistant = Assistant()
    print("Welcome to your AI Assistant!")
    assistant.show_help()
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            assistant.handle_command(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
