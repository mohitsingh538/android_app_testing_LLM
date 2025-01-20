import os
from typing import Any, Dict, Tuple
from openai import OpenAI
from llm.function_calling import action_handlers
from dotenv import load_dotenv

load_dotenv()


class LLMAutomation:

    base_url = os.environ.get("OPENAI_BASE_URL")
    api_key = os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("OPENAI_MODEL")

    @classmethod
    def call_llm(cls, query: str) -> Dict[str, Any] | None:
        """Call the LLM to interpret the instruction and return action name + arguments."""
        # Create a list of available actions for the prompt
        available_actions = "\n".join([f"- {act.name}: {act.description}" for act in action_handlers.values()])

        prompt = f"""
                    Interpret the following instruction and generate the corresponding action and parameters.
                        Available actions:
                        {available_actions}

                        Instruction: {query}

                        Respond in the exact format:
                        Action: <action_name>
                        Parameters: <param1>=<value1>, <param2>=<value2>
                """

        openai_init = OpenAI(
            base_url=cls.base_url,
            api_key=cls.api_key
        )

        response = openai_init.completions.create(
            model=cls.model,
            prompt=prompt,
            max_tokens=150,
            temperature=0.0,
        )

        action_response = response.choices[0].text.strip()
        try:
            action_name, args = cls._parse_action_response(action_response)

            if action_name.lower() not in {k.lower() for k in action_handlers.keys()}:
                raise ValueError(f"Invalid action '{action_name}'. Available actions are: {list(action_handlers.keys())}")

            return {"name": action_name.lower(), "arguments": args}

        except Exception as e:
            print(f"Error parsing LLM response: {action_response}\nError details: {str(e)}")
            return None

    @staticmethod
    def _parse_action_response(action_response: str) -> Tuple[str, Dict[str, Any]]:
        """Parse the LLM response into action name and arguments."""
        try:
            # Split into lines and clean up
            lines = [line.strip() for line in action_response.split('\n') if line.strip()]

            # Extract action name
            action_line = next(line for line in lines if line.lower().startswith('action:'))
            action_name = action_line.split(':', 1)[1].strip()

            # Extract parameters
            params_line = next((line for line in lines if line.lower().startswith('parameters:')), None)
            parameters = {}

            if params_line:
                params_str = params_line.split(':', 1)[1].strip()
                if params_str:
                    # Split parameters by comma and handle potential spaces
                    param_pairs = [p.strip() for p in params_str.split(',')]
                    for pair in param_pairs:
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            parameters[key.strip()] = value.strip()

            return action_name, parameters

        except Exception as e:
            raise ValueError(f"Failed to parse action response: {action_response}") from e