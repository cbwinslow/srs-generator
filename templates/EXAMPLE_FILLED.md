# Example SRS Generation Request (Filled)

This is a complete example of an SRS generation request with all fields filled in. Use this as a reference when creating your own requests.

---

## Project Information

**Project Name:**
TaskFlow - Team Collaboration Platform

**Target Users:**
- Remote teams of 5-50 members
- Project managers and team leads
- Software development teams
- Marketing and creative agencies
- Age range: 25-55
- Tech-savvy professionals familiar with SaaS tools
- Users across different time zones

**Project Goals:**
1. Improve team collaboration efficiency by 40%
2. Reduce time spent in status meetings by 50%
3. Provide real-time visibility into project progress
4. Enable asynchronous communication across time zones
5. Integrate with existing tools (Slack, GitHub, Google Workspace)
6. Achieve 95% user satisfaction score within 6 months
7. Support 10,000 active teams within first year

**Project Scope:**

**Included:**
- User authentication and team management
- Project and task management with Kanban boards
- Real-time collaboration features (comments, mentions, notifications)
- File sharing and document collaboration
- Time tracking and reporting
- Mobile applications (iOS and Android)
- Web application
- API for third-party integrations
- Integration with Slack, GitHub, and Google Workspace
- Dashboard with analytics and insights
- Search functionality across projects and tasks
- Role-based access control (Admin, Manager, Member, Guest)

**Excluded:**
- Built-in video conferencing (will integrate with Zoom/Teams)
- Advanced financial management and invoicing
- HR and payroll management
- Customer relationship management (CRM)
- Email hosting
- Code repository hosting (will integrate with GitHub/GitLab)
- Design tools (will integrate with Figma)

---

## Constraints

**Technical Constraints:**
- Must support modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Backend must be built with Python/Django or Node.js
- Must use PostgreSQL for primary database
- Must use Redis for caching and real-time features
- API must be RESTful and support GraphQL for complex queries
- Must support mobile apps for iOS 14+ and Android 10+
- Must handle 1,000 concurrent users per instance
- API response time must be under 200ms for 95th percentile
- Must support horizontal scaling
- Must be deployable on AWS or Azure
- Must use Docker for containerization

**Business Constraints:**
- Must launch MVP within 4 months
- Full version 1.0 must launch within 8 months
- Development budget: $250,000 (including infrastructure)
- Must be profitable within 18 months
- Must comply with GDPR, CCPA, and SOC 2 Type II
- Must support WCAG 2.1 AA accessibility standards
- Must offer free tier for teams up to 5 users
- Paid plans starting at $10/user/month
- Data retention: minimum 1 year, with export capability
- 99.9% uptime SLA for paid plans

**Budget/Timeline:**
- Timeline: 8 months for version 1.0 (4 months for MVP)
- Budget: $250,000 total
  - Development: $180,000
  - Infrastructure: $30,000 (first year)
  - Design: $20,000
  - Testing & QA: $20,000
- Team size: 6 developers, 1 designer, 1 product manager, 1 QA engineer

---

## Required SRS Sections

- [x] Introduction & Purpose
- [x] Functional Requirements
- [x] Non-Functional Requirements  
- [x] System Constraints
- [x] Use Cases & User Stories
- [x] System Architecture Overview
- [x] Data Requirements
- [x] External Interface Requirements
- [x] Security Requirements
- [x] Performance Requirements

---

## Additional Requirements

**Specific Quality Attributes:**

1. **Performance:**
   - Page load time: < 2 seconds
   - API response time: < 200ms (95th percentile)
   - Search results: < 500ms
   - Real-time updates: < 100ms latency

2. **Scalability:**
   - Support 10,000 concurrent users
   - Handle 100,000 API requests per minute
   - Store 100TB of file data
   - Support 1 million tasks across all teams

3. **Reliability:**
   - 99.9% uptime for paid plans
   - 99.5% uptime for free plans
   - Maximum 4 hours downtime per month for maintenance
   - Automated failover within 5 minutes

4. **Usability:**
   - New users can complete first task within 5 minutes
   - Task completion time 30% faster than competitors
   - User satisfaction score > 4.5/5.0
   - Support 10 languages at launch

**Compliance Requirements:**
- GDPR compliance (EU users)
  - Right to be forgotten
  - Data portability
  - Consent management
- CCPA compliance (California users)
  - Privacy policy
  - Opt-out mechanisms
  - Data disclosure
- SOC 2 Type II certification within 12 months
- WCAG 2.1 AA accessibility compliance
- Data encryption at rest and in transit
- Regular security audits (quarterly)
- Penetration testing before launch

**Integration Requirements:**

1. **Slack Integration:**
   - Receive notifications in Slack channels
   - Create tasks from Slack messages
   - Update task status from Slack
   - Two-way sync

2. **GitHub Integration:**
   - Link GitHub issues to tasks
   - Sync commit activity
   - Display PR status
   - Trigger actions from commits

3. **Google Workspace Integration:**
   - Single Sign-On (SSO) with Google
   - Attach Google Drive files
   - Create Google Calendar events
   - Import contacts

4. **Authentication Providers:**
   - Google OAuth 2.0
   - Microsoft Azure AD
   - SAML 2.0 for enterprise SSO
   - Email/password with 2FA

5. **Export/Import:**
   - Export data to CSV, JSON, Excel
   - Import from Trello, Asana, Jira
   - API for custom integrations
   - Webhook support

**Security Requirements:**

1. **Authentication:**
   - Multi-factor authentication (MFA)
   - Password requirements: minimum 12 characters, complexity rules
   - Session timeout: 30 minutes of inactivity
   - Failed login lockout: 5 attempts, 15-minute lockout

2. **Authorization:**
   - Role-based access control (RBAC)
   - Team-level permissions
   - Project-level permissions
   - Task-level permissions

3. **Data Security:**
   - Encryption at rest (AES-256)
   - Encryption in transit (TLS 1.3)
   - Secure file storage with access controls
   - Regular security scans (weekly)
   - Vulnerability patching within 48 hours

4. **Audit & Monitoring:**
   - Comprehensive audit logs
   - Real-time threat detection
   - Suspicious activity alerts
   - Compliance reporting

---

## Priority

- [x] High

**Justification:**
This is a competitive market, and timely delivery is critical for capturing market share. The MVP timeline of 4 months is aggressive but necessary to validate product-market fit.

---

## Acceptance Criteria

- [x] SRS document generated with all required sections
- [x] Document reviewed by stakeholders (CTO, Product Manager, Lead Developer)
- [x] Technical requirements are clear and testable
- [x] Non-functional requirements are measurable
- [x] All constraints are documented
- [x] Use cases cover 90% of user workflows
- [x] Architecture diagram included
- [x] Data model documented
- [x] API specifications defined
- [x] Security requirements comprehensive

---

## Notes

**Market Research:**
- Competitor analysis completed (Asana, Trello, Monday.com)
- Identified gaps: better real-time collaboration, simpler UI, more affordable pricing
- Target market: 100,000 teams in first 2 years

**User Research:**
- Conducted 30 user interviews
- Common pain points: too many tools, difficult collaboration, lack of visibility
- Most requested features: real-time updates, mobile apps, integrations

**Technical Considerations:**
- Considering WebSocket for real-time features
- Evaluating AWS vs Azure (leaning toward AWS)
- Planning for multi-region deployment
- Considering microservices architecture for scalability

**Risk Factors:**
- Timeline is aggressive - may need to adjust scope
- Competition is fierce - need strong differentiation
- Scaling challenges with real-time features
- Integration complexity with third-party tools

**Success Metrics:**
- User acquisition: 1,000 teams in first 3 months
- User retention: 80% monthly active users
- Revenue: $50,000 MRR by month 12
- NPS score: > 50

---

## Expected Output

After generating the SRS document, the output should include:

1. **Comprehensive Introduction** (2-3 pages)
   - Project purpose and vision
   - Target audience detailed profiles
   - Success criteria and metrics

2. **Detailed Functional Requirements** (10-15 pages)
   - 50+ specific functional requirements
   - Organized by feature area
   - Priority and dependencies noted

3. **Non-Functional Requirements** (5-7 pages)
   - Performance benchmarks
   - Security specifications
   - Scalability requirements
   - Reliability targets

4. **System Constraints** (3-5 pages)
   - Technical limitations
   - Business constraints
   - Regulatory requirements

5. **Use Cases** (8-10 pages)
   - 20+ detailed use cases
   - User stories for Agile development
   - Acceptance criteria for each

6. **Architecture Overview** (5-7 pages)
   - System architecture diagram
   - Component descriptions
   - Technology stack details

7. **Data Requirements** (4-6 pages)
   - Data model/ER diagram
   - Data dictionary
   - Data flow descriptions

8. **External Interfaces** (3-5 pages)
   - API specifications
   - Integration requirements
   - Third-party dependencies

Total expected document: 40-60 pages
