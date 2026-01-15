"""
Interactive AI Agent for guided SRS document generation.

This module provides an intelligent conversational agent that guides users
through the process of creating a complete SRS document by asking relevant
questions and validating input quality.
"""

from typing import Dict, Any
import openai
from flask import current_app


class InteractiveAgent:
    """
    An AI agent that interactively guides users through SRS creation.

    The agent:
    - Asks clarifying questions to gather complete information
    - Validates input quality and completeness
    - Guides users through all required SRS sections
    - Provides suggestions and examples when needed
    """

    # Standard SRS template sections that need to be filled
    SRS_TEMPLATE = {
        "project_overview": {
            "questions": [
                "What is the name of your project?",
                "What problem does this project solve?",
                "Who are the primary users/stakeholders?",
            ],
            "description": "High-level project information",
        },
        "functional_requirements": {
            "questions": [
                "What are the main features users need?",
                "What actions should users be able to perform?",
                "What are the core workflows?",
            ],
            "description": "Specific features and capabilities",
        },
        "non_functional_requirements": {
            "questions": [
                "What performance requirements exist (speed, scalability)?",
                "What are the security requirements?",
                "What are the reliability/availability requirements?",
            ],
            "description": "Quality attributes and constraints",
        },
        "user_interface": {
            "questions": [
                "What platforms will this run on (web, mobile, desktop)?",
                "Are there any specific UI/UX requirements?",
                "What accessibility requirements exist?",
            ],
            "description": "User interface specifications",
        },
        "technical_constraints": {
            "questions": [
                "What technologies or frameworks must be used?",
                "Are there any existing systems to integrate with?",
                "What are the deployment constraints?",
            ],
            "description": "Technical limitations and requirements",
        },
    }

    def __init__(self):
        """Initialize the interactive agent with OpenAI client."""
        try:
            self.client = openai.OpenAI(
                api_key=current_app.config["OPENROUTER_API_KEY"]
            )
            self.conversation_history = []
        except Exception as e:
            raise Exception(f"Failed to initialize agent: {str(e)}")

    def start_conversation(self) -> Dict[str, Any]:
        """
        Start a new interactive SRS generation conversation.

        Returns:
            dict: Initial message with agent introduction and first question
        """
        intro_message = (
            "Hello! I'm your AI assistant for creating a comprehensive "
            "Software Requirements Specification (SRS) document.\n\n"
            "I'll guide you through gathering all the necessary information "
            "to create a complete, professional SRS. Instead of filling out "
            "a form, we'll have a conversation where I'll ask relevant "
            "questions and help you articulate your requirements clearly.\n\n"
            "Let's start with the basics: **What is your project about?** "
            "Please provide a brief overview including:\n"
            "- Project name\n"
            "- What problem it solves\n"
            "- Who will use it"
        )

        self.conversation_history = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "assistant", "content": intro_message},
        ]

        return {
            "message": intro_message,
            "conversation_id": id(self),
            "progress": self._calculate_progress({}),
            "next_steps": list(self.SRS_TEMPLATE.keys()),
        }

    def process_user_input(
        self, user_input: str, collected_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process user input and generate next question or completion response.

        Args:
            user_input: The user's response
            collected_data: Previously collected information

        Returns:
            dict: Agent's response with next question or completion status
        """
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})

        # Extract information from user input
        extracted_info = self._extract_information(user_input, collected_data)

        # Update collected data
        collected_data.update(extracted_info)

        # Calculate progress
        progress = self._calculate_progress(collected_data)

        # Determine if we need more information
        if progress["percentage"] < 100:
            next_question = self._generate_next_question(collected_data)
            self.conversation_history.append(
                {"role": "assistant", "content": next_question}
            )

            return {
                "message": next_question,
                "collected_data": collected_data,
                "progress": progress,
                "complete": False,
            }
        else:
            # Generate final SRS document
            return {
                "message": (
                    "Great! I have all the information needed. "
                    "Generating your complete SRS document now..."
                ),
                "collected_data": collected_data,
                "progress": progress,
                "complete": True,
            }

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI agent."""
        return (
            "You are an expert business analyst and technical writer "
            "specializing in Software Requirements Specification documents.\n\n"
            "Your role is to:\n"
            "1. Guide users through providing complete project information "
            "through natural conversation\n"
            "2. Ask clarifying questions when responses are vague or incomplete\n"
            "3. Validate that information meets professional SRS standards\n"
            "4. Suggest improvements and examples when needed\n"
            "5. Ensure all critical SRS sections are covered\n\n"
            "Be friendly, professional, and patient. Ask one focused question "
            "at a time. Acknowledge good answers and gently prompt for more "
            "detail when needed."
        )

    def _extract_information(
        self, user_input: str, existing_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract structured information from user's natural language input.

        Args:
            user_input: Raw user input text
            existing_data: Previously collected data

        Returns:
            dict: Extracted and structured information
        """
        # Store raw user input for comprehensive context
        # The full conversation history will be used when generating
        # the final SRS document, allowing the AI to understand the
        # complete project context
        return {"raw_notes": existing_data.get("raw_notes", []) + [user_input]}

    def _calculate_progress(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate completion progress based on collected data.

        Args:
            collected_data: Information collected so far

        Returns:
            dict: Progress information with percentage and missing sections
        """
        total_sections = len(self.SRS_TEMPLATE)
        completed_sections = []
        missing_sections = []

        # Simple heuristic: check if we have raw notes
        # In a more sophisticated system, this would validate each section
        raw_notes = collected_data.get("raw_notes", [])

        if len(raw_notes) >= 1:
            completed_sections.append("project_overview")
        if len(raw_notes) >= 2:
            completed_sections.append("functional_requirements")
        if len(raw_notes) >= 3:
            completed_sections.append("non_functional_requirements")
        if len(raw_notes) >= 4:
            completed_sections.append("user_interface")
        if len(raw_notes) >= 5:
            completed_sections.append("technical_constraints")

        for section in self.SRS_TEMPLATE.keys():
            if section not in completed_sections:
                missing_sections.append(section)

        percentage = (len(completed_sections) / total_sections) * 100

        return {
            "percentage": int(percentage),
            "completed_sections": completed_sections,
            "missing_sections": missing_sections,
            "total_sections": total_sections,
        }

    def _generate_next_question(self, collected_data: Dict[str, Any]) -> str:
        """
        Generate the next appropriate question based on collected data.

        Args:
            collected_data: Information collected so far

        Returns:
            str: Next question to ask the user
        """
        progress = self._calculate_progress(collected_data)
        missing_sections = progress["missing_sections"]

        if not missing_sections:
            return (
                "Let me review what we've covered. Is there anything else "
                "you'd like to add or clarify?"
            )

        # Get the next section to cover
        next_section = missing_sections[0]
        section_info = self.SRS_TEMPLATE[next_section]

        # Use AI to generate a contextual question
        try:
            context = "\n".join(collected_data.get("raw_notes", []))
            question_prompt = (
                f"Based on the following project information collected so far:\n\n"
                f"{context}\n\n"
                f"Generate a natural, conversational question to gather "
                f"information about: {section_info['description']}\n\n"
                f"The question should:\n"
                f"1. Be friendly and clear\n"
                f"2. Reference what we've already discussed if relevant\n"
                f"3. Help the user understand what information is needed\n"
                f"4. Provide examples if helpful\n\n"
                f"Focus on: {', '.join(section_info['questions'][:2])}"
            )

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": question_prompt},
                ],
                temperature=0.7,
                max_tokens=300,
            )

            return response.choices[0].message.content

        except Exception as e:
            current_app.logger.error(f"Error generating question: {str(e)}")
            # Fall back to template questions
            return (
                f"Now let's discuss {next_section.replace('_', ' ')}. "
                f"{section_info['questions'][0]}"
            )

    def generate_complete_srs(self, collected_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate complete SRS document from collected information.

        Args:
            collected_data: All information collected during conversation

        Returns:
            dict: Complete SRS document sections
        """
        try:
            # Consolidate all collected information
            all_notes = "\n\n".join(collected_data.get("raw_notes", []))

            # Generate each section using AI
            sections = {}

            # Introduction section
            sections["introduction"] = self._generate_section(
                "introduction",
                all_notes,
                "Write a professional introduction section including purpose, "
                "scope, and definitions.",
            )

            # System description
            sections["system_description"] = self._generate_section(
                "system_description",
                all_notes,
                "Describe the system context, features, and high-level "
                "architecture.",
            )

            # Functional requirements
            sections["functional_requirements"] = self._generate_section(
                "functional_requirements",
                all_notes,
                "List detailed, numbered functional requirements (FR1, FR2, etc.) "
                "covering all features and capabilities.",
            )

            # Non-functional requirements
            sections["non_functional_requirements"] = self._generate_section(
                "non_functional_requirements",
                all_notes,
                "Specify non-functional requirements (NFR1, NFR2, etc.) for "
                "performance, security, reliability, usability, etc.",
            )

            # System constraints
            sections["constraints"] = self._generate_section(
                "constraints",
                all_notes,
                "List all technical, business, and operational constraints.",
            )

            # User interface requirements
            sections["user_interface"] = self._generate_section(
                "user_interface",
                all_notes,
                "Describe user interface requirements, platforms, and UX "
                "considerations.",
            )

            return sections

        except Exception as e:
            current_app.logger.error(f"Error generating SRS: {str(e)}")
            raise Exception(f"Failed to generate complete SRS: {str(e)}")

    def _generate_section(
        self, section_name: str, context: str, instructions: str
    ) -> str:
        """Generate a specific SRS section."""
        try:
            prompt = (
                f"Based on the following project information:\n\n"
                f"{context}\n\n"
                f"{instructions}\n\n"
                f"Write in a professional, clear, and structured format "
                f"suitable for a Software Requirements Specification document."
            )

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert technical writer creating "
                            "professional SRS documentation."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=1000,
            )

            return response.choices[0].message.content

        except Exception as e:
            current_app.logger.error(
                f"Error generating section {section_name}: {str(e)}"
            )
            return (
                f"Error generating {section_name} section. Please try again."
            )
