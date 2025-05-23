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
       help_text = "Available commands (try natural language!):\n"
       help_text += "- plan_travel / view_travel_plans\n"
       help_text += "- set_reminder / view_reminders\n"
       help_text += "- create_mind_map / add_mind_map_node / view_mind_map\n"
       help_text += "- help\n"
       help_text += "- exit"
       return help_text

    def plan_travel(self, args=None): # args can now be a dict from NLP
        # print("Let's plan your travel!") # Web: No direct print
        try:
            destination = args.get("destination") if args else None
            start_date = args.get("start_date") if args else None
            end_date = args.get("end_date") if args else None

            if not destination:
                destination = input("Enter destination: ") # Still need input if not web
            if not start_date:
                start_date = input("Enter start date (YYYY-MM-DD): ")
            if not end_date:
                end_date = input("Enter end date (YYYY-MM-DD): ")
            
            if not destination or not start_date or not end_date:
                return "All fields are required. Travel plan not saved."

            new_plan = {
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "status": "planned"
            }
            self.travel_plans.append(new_plan)
            return f"Travel to {destination} from {start_date} to {end_date} planned successfully!"
        except Exception as e:
            return f"Error planning travel: {e}"

    def view_travel_plans(self, args=None):
        if not self.travel_plans:
            return "No travel plans yet. Use 'plan_travel' to add one."
        response = "\n--- Your Travel Plans ---\n"
        for i, plan in enumerate(self.travel_plans):
            response += f"Plan {i+1}:\n"
            response += f"  Destination: {plan['destination']}\n"
            response += f"  Start Date: {plan['start_date']}\n"
            response += f"  End Date: {plan['end_date']}\n"
            response += f"  Status: {plan['status']}\n"
            response += "-" * 20 + "\n"
        return response

    def set_reminder(self, args=None): # args can now be a dict from NLP
        # print("Let's set a reminder!") # Web: No direct print
        try:
            message = args.get("message") if args else None
            time_str = args.get("time_str") if args else None

            if not message:
                message = input("Enter reminder message: ") # Still need input if not web
            if not time_str:
                time_str = input("Enter reminder time (e.g., 'tomorrow 10am' or '2024-12-31 23:59'): ")
            
            if not message or not time_str:
                return "Message and time are required. Reminder not set."

            new_reminder = {
                "message": message,
                "time_str": time_str, 
                "status": "pending" 
            }
            self.reminders.append(new_reminder)
            return f"Reminder '{message}' set for '{time_str}' successfully!"
        except Exception as e:
            return f"Error setting reminder: {e}"

    def view_reminders(self, args=None):
        if not self.reminders:
            return "No reminders set yet. Use 'set_reminder' to add one."
        response = "\n--- Your Reminders ---\n"
        for i, reminder in enumerate(self.reminders):
            response += f"Reminder {i+1}:\n"
            response += f"  Message: {reminder['message']}\n"
            response += f"  Time: {reminder['time_str']}\n"
            response += f"  Status: {reminder['status']}\n"
            response += "-" * 20 + "\n"
        return response

    def create_mind_map(self, args=None):
        map_name = ""
        if args:
            map_name = " ".join(args)
        else:
            map_name = input("Enter the name/central topic for your new mind map: ") # CLI fallback

        if not map_name:
            return "Mind map name cannot be empty. Creation failed."
        if map_name in self.mind_maps:
            return f"A mind map named '{map_name}' already exists."
       
        self.mind_maps[map_name] = {"root": {"text": map_name, "children": []}}
        return f"Mind map '{map_name}' created successfully."

    def _find_node_in_map(self, current_node, target_text):
        if current_node["text"] == target_text:
            return current_node
        for child in current_node["children"]:
            found = self._find_node_in_map(child, target_text)
            if found:
                return found
        return None

    def add_mind_map_node(self, args=None): # args not used by current NLP, relies on input
        map_name = input("Enter the name of the mind map to add a node to: ") # CLI
        if map_name not in self.mind_maps:
            return f"Mind map '{map_name}' not found."

        parent_node_text = input("Enter the text of the parent node (or root to add to central topic): ") # CLI
        new_node_text = input("Enter the text for the new node/idea: ") # CLI

        if not new_node_text:
            return "New node text cannot be empty. Node not added."
        
        mind_map_data = self.mind_maps[map_name]
        
        parent_node = None
        if parent_node_text.lower() == "root" or parent_node_text == mind_map_data["root"]["text"]:
            parent_node = mind_map_data["root"]
        else:
            parent_node = self._find_node_in_map(mind_map_data["root"], parent_node_text)

        if not parent_node:
            return f"Parent node '{parent_node_text}' not found in mind map '{map_name}'."

        parent_node["children"].append({"text": new_node_text, "children": []})
        return f"Node '{new_node_text}' added to '{parent_node['text']}' in mind map '{map_name}'."

    def _display_map_node(self, node, indent_level=0, current_map_str=""):
        indent = "  " * indent_level
        current_map_str += f"{indent}- {node['text']}\n"
        for child in node["children"]:
            current_map_str = self._display_map_node(child, indent_level + 1, current_map_str)
        return current_map_str

    def view_mind_map(self, args=None):
        map_name = ""
        if args:
            map_name = " ".join(args)
        else:
            map_name = input("Enter the name of the mind map to view: ") # CLI fallback

        if not map_name:
            return "Mind map name cannot be empty."
        if map_name not in self.mind_maps:
            return f"Mind map '{map_name}' not found."

        header = f"\n--- Mind Map: {map_name} ---\n"
        return header + self._display_map_node(self.mind_maps[map_name]["root"])

    def handle_command(self, user_input_text):
        doc = nlp(user_input_text.lower())
        intent = None
        args_dict = {} # Renamed from 'args' to avoid conflict

        # Help intent
        if any(token.lemma_ in ["help", "assist", "guide"] for token in doc):
            intent = "help"
        
        # Travel planning intents
        elif any(token.lemma_ in ["travel", "trip", "journey", "vacation"] for token in doc) and \
             any(token.lemma_ in ["plan", "book", "organize", "new"] for token in doc):
            intent = "plan_travel"
            for ent in doc.ents:
                if ent.label_ == "GPE": 
                    args_dict["destination"] = ent.text
                elif ent.label_ == "DATE":
                    if "start_date" not in args_dict:
                        args_dict["start_date"] = ent.text
                    else:
                        args_dict["end_date"] = ent.text
        elif any(token.lemma_ in ["travel", "trip", "journey", "vacation"] for token in doc) and \
             any(token.lemma_ in ["show", "view", "list", "see", "find"] for token in doc):
            intent = "view_travel_plans"

        # Reminder intents
        elif any(token.lemma_ in ["remind", "reminder", "alert"] for token in doc) and \
             any(token.lemma_ in ["set", "add", "new", "create"] for token in doc):
            intent = "set_reminder"
            message_parts = []
            time_entity = None
            # Iterate through tokens to reconstruct message and find time
            message_token_indices = []
            time_token_indices = []

            for i, token in enumerate(doc):
                # Try to identify core action verbs/prepositions for reminder text
                if token.lemma_ in ["remind", "me", "to", "set", "alert", "for", "on", "at"]:
                    continue # Skip these keywords from the message itself
                
                # Check for time entities or time-related keywords
                is_time_related = False
                if token.ent_type_ == "TIME":
                    is_time_related = True
                else: # Check subtree for common time words if not a formal TIME entity
                    for sub_token in token.subtree:
                        if sub_token.lemma_ in ["today", "tomorrow", "yesterday", "now"] or \
                           any(num_char.isdigit() for num_char in sub_token.text): # Basic check for time like "10am"
                            is_time_related = True
                            break
                
                if is_time_related:
                    # Collect all tokens of a potential time phrase
                    current_time_phrase = " ".join(t.text for t in token.subtree)
                    if not time_entity or len(current_time_phrase) > len(time_entity): # Prefer longer (more complete) time phrases
                        time_entity = current_time_phrase
                else:
                    message_parts.append(token.text)

            if message_parts:
                args_dict["message"] = " ".join(message_parts).strip().replace(time_entity if time_entity else "", "").strip() # Attempt to remove time from message
            if time_entity:
                args_dict["time_str"] = time_entity.strip()


        elif any(token.lemma_ in ["reminder", "remind"] for token in doc) and \
             any(token.lemma_ in ["show", "view", "list", "see", "find"] for token in doc):
            intent = "view_reminders"

        # Mind map intents
        elif any(token.lemma_ in ["mindmap", "mind map", "map"] for token in doc) and \
             any(token.lemma_ in ["create", "new", "start", "make"] for token in doc):
            intent = "create_mind_map"
            name_parts = []
            for token in doc: # Basic name extraction, can be improved
                if token.lemma_ not in ["mindmap", "mind", "map", "create", "new", "start", "make", "a", "an", "the", "for", "of", "called"]:
                     name_parts.append(token.text)
            if name_parts:
                args_dict["map_name"] = " ".join(name_parts).strip()

        elif any(token.lemma_ in ["mindmap", "mind map", "map"] for token in doc) and \
             any(token.lemma_ in ["add", "node", "idea"] for token in doc):
            intent = "add_mind_map_node"

        elif any(token.lemma_ in ["mindmap", "mind map", "map"] for token in doc) and \
             any(token.lemma_ in ["show", "view", "display", "open"] for token in doc):
            intent = "view_mind_map"
            name_parts = []
            for token in doc: # Basic name extraction
                if token.lemma_ not in ["mindmap", "mind", "map", "show", "view", "display", "open", "a", "an", "the", "for", "of"]:
                     name_parts.append(token.text)
            if name_parts:
                args_dict["map_name"] = " ".join(name_parts).strip()

        if intent and intent in self.commands:
            # print(f"DEBUG: Intent: {intent}, Args: {args_dict}") # Optional: for logging
            
            if intent == "plan_travel":
                return self.commands[intent](args_dict) 
            elif intent == "set_reminder":
                 return self.commands[intent](args_dict)
            elif intent == "create_mind_map":
                name_list = args_dict.get("map_name", "").split() if args_dict.get("map_name") else None
                return self.commands[intent](name_list)
            elif intent == "view_mind_map":
                name_list = args_dict.get("map_name", "").split() if args_dict.get("map_name") else None
                return self.commands[intent](name_list)
            elif intent == "add_mind_map_node": 
                return self.commands[intent]() # Still relies on input() for details
            else: # For commands like help, view_travel_plans, view_reminders
                return self.commands[intent](args_dict if args_dict else None)
        else:
            return f"Sorry, I didn't understand that. Try 'help' for available commands."

if __name__ == "__main__":
    assistant = Assistant()
    # The show_help() call here will print the returned string.
    print(assistant.show_help()) # Modified to print the returned string
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            # The result from handle_command is now printed here.
            response = assistant.handle_command(user_input)
            print(response)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
