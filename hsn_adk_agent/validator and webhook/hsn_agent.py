from hsn_validator_api import HSNValidator

class HSNCodeAgent:
    def __init__(self, data_path):
        self.validator = HSNValidator(data_path)

    def handle_input(self, user_input):
        codes = self.extract_hsn_codes(user_input)
        if not codes:
            return " I couldn't find any HSN codes in your input. Please try again."

        responses = []
        for code in codes:
            result = self.validator.validate_code(code, hierarchical=True)
            if result["valid"]:
                msg = f" HSN Code `{code}` is valid.\n Description: *{result['description']}*"
                if "hierarchy" in result:
                    parents = result["hierarchy"]
                    if parents:
                        hierarchy_msg = "\n Hierarchy:\n" + "\n".join(
                            [f"- `{p['code']}`: {p['description']}" for p in parents]
                        )
                        msg += hierarchy_msg
            else:
                msg = f" HSN Code `{code}` is invalid. Reason: {result['reason']}"

            responses.append(msg)
        return "\n\n".join(responses)

    def extract_hsn_codes(self, text):
        import re
        return re.findall(r'\b\d{2,8}\b', text)


# --- Simulated Chatbot Interface ---
if __name__ == "__main__":
    agent = HSNCodeAgent(r"C:\Users\BHUMIKA\Desktop\Settyl\HSN_SAC.xlsx")
    print(" HSN Validation Agent is online. Type your HSN query or 'exit' to quit.")
    while True:
        user_input = input(" You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        reply = agent.handle_input(user_input)
        print(" Agent:", reply)
