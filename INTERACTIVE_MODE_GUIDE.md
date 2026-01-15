# Interactive Mode Guide

## Overview

The **Interactive Mode** is an AI-powered conversational interface that guides users through creating comprehensive SRS documents. Instead of filling out a static form, you have a natural conversation with an intelligent agent that asks relevant questions and helps you articulate your requirements clearly.

## Why Use Interactive Mode?

### Traditional Form vs Interactive Mode

**Traditional Form:**
- ❌ Requires knowing what information to provide upfront
- ❌ Fixed fields may not capture all relevant details
- ❌ No guidance on what makes a good requirement
- ❌ Easy to skip important details

**Interactive Mode:**
- ✅ AI guides you step-by-step through all required information
- ✅ Asks clarifying questions when responses are vague
- ✅ Adapts questions based on your previous answers
- ✅ Ensures all critical SRS sections are covered
- ✅ More natural and intuitive experience
- ✅ Results in more complete, detailed documents

## How It Works

### 1. Starting a Session

When you navigate to the Interactive Mode page:
1. An AI agent automatically starts a conversation
2. You'll see a welcome message explaining the process
3. The agent asks its first question about your project

### 2. Having a Conversation

The conversation flow is natural and adaptive:

```
Agent: "Hello! I'm your AI assistant for creating a comprehensive 
       Software Requirements Specification (SRS) document. Let's start 
       with the basics: What is your project about?"

You: "I'm building a mobile app for fitness tracking"

Agent: "Great! A fitness tracking mobile app. Can you tell me more 
       about what specific problems this app will solve for users?"

You: "Users struggle to maintain workout routines and track their 
     progress over time"

Agent: "Perfect. Now, who are the primary users of this fitness app? 
       Please describe their characteristics and needs."
```

### 3. Progress Tracking

As you answer questions:
- A visual progress bar shows completion percentage
- The system tracks which SRS sections have been covered
- You can see how close you are to having all required information

### 4. Completion

When the agent has gathered sufficient information:
- You'll receive a completion message
- The system generates a complete SRS document
- You can download the document as a Markdown file

## Using the Interface

### Chat Interface

The interactive mode provides a modern chat interface:

**Elements:**
- **Chat Header**: Shows progress bar and completion percentage
- **Message Area**: Displays conversation history
- **Input Field**: Where you type your responses
- **Send Button**: Submits your message to the agent

**Visual Indicators:**
- **Agent messages**: Appear on the left in white bubbles
- **Your messages**: Appear on the right in colored bubbles
- **Typing indicator**: Shows when the agent is processing
- **Progress bar**: Green bar fills as you complete sections

### Navigation

- **Home Link**: Return to traditional form mode anytime
- **Download Button**: Appears when document is complete

## What the Agent Covers

The interactive agent ensures all critical SRS sections are addressed:

### 1. Project Overview
- Project name and purpose
- Problem being solved
- Target users and stakeholders

### 2. Functional Requirements
- Core features and capabilities
- User workflows and actions
- System behaviors

### 3. Non-Functional Requirements
- Performance requirements
- Security considerations
- Reliability and availability
- Scalability needs

### 4. User Interface
- Platform requirements (web, mobile, desktop)
- UI/UX specifications
- Accessibility requirements

### 5. Technical Constraints
- Required technologies or frameworks
- System integrations
- Deployment constraints
- Technical limitations

## Tips for Best Results

### 1. Be Specific

❌ **Vague:** "It's for managing stuff"
✅ **Specific:** "It's for managing software development tasks including story creation, sprint planning, and bug tracking"

### 2. Provide Context

❌ **Minimal:** "E-commerce site"
✅ **Contextual:** "B2B e-commerce platform for wholesale distributors selling to retailers, with features for bulk ordering and custom pricing"

### 3. Include Details

When the agent asks about features, provide:
- What the feature does
- Who will use it
- Why it's needed
- Any specific requirements

### 4. Ask for Clarification

If you don't understand a question:
- Say so! "I'm not sure what you mean by non-functional requirements"
- The agent will provide examples and clarification

### 5. Take Your Time

- There's no rush - think through your answers
- You can always expand on previous answers
- The agent will ask follow-up questions if needed

## Example Conversation

Here's an example of a complete interactive session:

```
Agent: "Hello! I'm your AI assistant for creating a comprehensive 
       Software Requirements Specification (SRS) document. Let's 
       start with the basics: What is your project about?"

User: "I want to build a project management tool for small teams"

Agent: "Excellent! A project management tool for small teams. Can you 
       describe what specific challenges or problems this tool will 
       solve for these teams?"

User: "Many small teams struggle with task visibility, deadline 
      tracking, and coordinating work across remote team members"

Agent: "That's very helpful context. Now, tell me about your target 
       users. Who are the people who will use this tool daily?"

User: "Small startup teams of 5-15 people, mostly in tech, working 
      remotely or hybrid. Team leads, developers, and designers"

Agent: "Perfect. Now let's talk about features. What are the main 
       features you envision for this project management tool?"

User: "Task creation and assignment, kanban boards, time tracking, 
      file sharing, team chat, and notifications"

Agent: "Great feature set! Now, regarding performance and technical 
       requirements: Are there any specific performance needs, like 
       response time or number of concurrent users?"

User: "Should handle up to 50 concurrent users per team, load pages 
      in under 2 seconds, work on mobile and desktop"

Agent: "Excellent. What about security? Any specific security 
       requirements for user data or authentication?"

User: "Need secure user authentication, role-based access control, 
      encrypted data storage, and GDPR compliance"

Agent: "What platforms will this run on, and are there any specific 
       UI/UX requirements?"

User: "Web application that works on desktop and mobile browsers, 
      with a clean, minimal interface similar to Linear or Notion"

Agent: "Finally, are there any technical constraints? Required 
       technologies, integrations, or limitations?"

User: "Must integrate with GitHub and Slack, prefer React for 
      frontend, Node.js for backend, deploy on AWS"

Agent: "Great! I have all the information needed. Generating your 
       complete SRS document now..."

[Download button appears]
```

## API Endpoints

If you want to integrate the interactive mode programmatically:

### Start Session

```bash
POST /api/v1/interactive/start
```

Response:
```json
{
  "status": "success",
  "session_id": "abc123",
  "message": "Hello! I'm your AI assistant...",
  "progress": {
    "percentage": 0,
    "completed_sections": [],
    "missing_sections": ["project_overview", "functional_requirements", ...]
  }
}
```

### Send Message

```bash
POST /api/v1/interactive/respond
Content-Type: application/json

{
  "session_id": "abc123",
  "message": "I'm building a mobile fitness app"
}
```

Response (in progress):
```json
{
  "status": "in_progress",
  "message": "Great! Can you tell me more about...",
  "progress": {
    "percentage": 20,
    "completed_sections": ["project_overview"],
    "missing_sections": [...]
  }
}
```

Response (complete):
```json
{
  "status": "complete",
  "message": "Your SRS is ready!",
  "sections": {
    "introduction": "...",
    "functional_requirements": "...",
    "non_functional_requirements": "...",
    ...
  },
  "progress": {
    "percentage": 100
  }
}
```

### Check Status

```bash
GET /api/v1/interactive/status/{session_id}
```

## Troubleshooting

### Common Issues

**Q: The agent stopped responding**
- Check your internet connection
- Refresh the page to start a new session
- Check browser console for errors

**Q: My responses aren't being understood**
- Try being more specific
- Use complete sentences
- Provide examples when possible

**Q: The progress bar isn't moving**
- The agent may need more detailed information
- Answer the follow-up questions fully
- Each major topic covered increases progress

**Q: I want to change a previous answer**
- Simply mention it: "Actually, regarding the users I mentioned earlier..."
- The agent will incorporate the new information

**Q: The generated document is incomplete**
- Make sure you answered all the agent's questions
- Check that progress reached 100% before generating
- Try providing more detail in your responses

## Best Practices

### 1. Prepare Information

Before starting, gather:
- Project overview and goals
- List of key features
- Information about target users
- Any technical requirements or constraints

### 2. Answer Thoroughly

Each question is designed to capture specific information:
- Don't give one-word answers
- Provide examples and context
- Think about edge cases

### 3. Use Examples

When describing features or requirements:
- ✅ "Users can export reports as PDF or Excel, with custom date ranges"
- ❌ "Export reports"

### 4. Think About Non-Functional Requirements

Don't forget to mention:
- Performance needs (speed, scale)
- Security requirements
- Reliability expectations
- Usability considerations

### 5. Review and Refine

After downloading:
- Review the generated document
- Add any missing technical details
- Refine requirements for clarity
- Share with stakeholders for feedback

## Comparison with Other Methods

| Feature | Quick Form | Interactive Mode | CLI Tool |
|---------|-----------|------------------|----------|
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡ Moderate | ⚡⚡ Moderate |
| **Completeness** | ⭐⭐ Basic | ⭐⭐⭐ Comprehensive | ⭐⭐ Basic |
| **Guidance** | ❌ None | ✅ Full guidance | ❌ None |
| **User Experience** | 📝 Form-based | 💬 Conversational | 💻 Command-line |
| **Best For** | Quick docs | First-time users | Automation |
| **Learning Curve** | Easy | Very Easy | Moderate |

## Next Steps

After generating your SRS:

1. **Review**: Read through the complete document
2. **Refine**: Add specific technical details
3. **Validate**: Check against your actual requirements
4. **Share**: Distribute to team and stakeholders
5. **Iterate**: Update as requirements evolve

## Support

Need help with Interactive Mode?
- Review this guide
- Check the main [README.md](README.md)
- See [USAGE_GUIDE.md](USAGE_GUIDE.md) for additional context
- Open an issue on GitHub for bugs or suggestions

---

**Ready to try it?** Start the application and navigate to `/interactive.html`!
