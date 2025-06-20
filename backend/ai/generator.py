from typing import Dict, Any
import openai
from flask import current_app


class AIGeneratorError(Exception):
    """Custom exception for AI generation errors."""

    pass


class AIGenerator:
    """Handles AI-powered SRS document generation."""

    def __init__(self):
        try:
            self.client = openai.OpenAI(
                api_key=current_app.config["OPENROUTER_API_KEY"]
            )
        except Exception as e:
            raise AIGeneratorError(f"Failed to initialize OpenAI client: {str(e)}")

    def generate_section(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a specific section of the SRS document."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            current_app.logger.error(f"Error generating section: {str(e)}")
            raise AIGeneratorError(f"Failed to generate section: {str(e)}")

    def generate_srs(self, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate a complete SRS document."""
        try:
            sections = {
                "introduction": self._generate_introduction(project_data),
                "functional_requirements": self._generate_functional_requirements(
                    project_data
                ),
                "non_functional_requirements": self._generate_non_functional_requirements(
                    project_data
                ),
                "constraints": self._generate_constraints(project_data),
            }
            return sections
        except Exception as e:
            raise AIGeneratorError(f"Failed to generate SRS: {str(e)}")

    def _generate_introduction(self, project_data: Dict[str, Any]) -> str:
        system_prompt = "You are an expert in writing software documentation. Create a professional introduction section for a Software Requirements Specification document."
        user_prompt = f"""Create an introduction section for the following project:
        Project Name: {project_data["projectName"]}
        Target Users: {project_data["targetUsers"]}
        Project Goals: {project_data["projectGoals"]}
        Project Scope: {project_data["projectScope"]}
        """
        return self.generate_section(system_prompt, user_prompt)

    def _generate_functional_requirements(self, project_data: Dict[str, Any]) -> str:
        system_prompt = "You are an expert in software requirements analysis. List detailed functional requirements based on the project description."
        user_prompt = f"""Generate functional requirements for the following project:
        Project Name: {project_data["projectName"]}
        Target Users: {project_data["targetUsers"]}
        Project Goals: {project_data["projectGoals"]}
        Project Scope: {project_data["projectScope"]}
        """
        return self.generate_section(system_prompt, user_prompt)

    def _generate_non_functional_requirements(
        self, project_data: Dict[str, Any]
    ) -> str:
        system_prompt = "You are an expert in software quality attributes. Specify non-functional requirements covering performance, security, reliability, and usability."
        user_prompt = f"""Generate non-functional requirements for the following project:
        Project Name: {project_data["projectName"]}
        Target Users: {project_data["targetUsers"]}
        Project Goals: {project_data["projectGoals"]}
        Project Scope: {project_data["projectScope"]}
        """
        return self.generate_section(system_prompt, user_prompt)

    def _generate_constraints(self, project_data: Dict[str, Any]) -> str:
        system_prompt = "You are an expert in software project planning. Identify technical, business, and operational constraints."
        user_prompt = f"""List project constraints for the following project:
        Project Name: {project_data["projectName"]}
        Target Users: {project_data["targetUsers"]}
        Project Goals: {project_data["projectGoals"]}
        Project Scope: {project_data["projectScope"]}
        """
        return self.generate_section(system_prompt, user_prompt)
