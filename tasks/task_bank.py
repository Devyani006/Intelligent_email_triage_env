TASK_BANK = [
    # ─── EASY: Priority Classification ────────────────────────────────────────
    {
        "task_id": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the email priority as: low / medium / high / urgent",
        "email": {
            "id": "e001",
            "subject": "URGENT: Production server down — all services offline",
            "sender": "ops-alert@company.com",
            "body": (
                "All production services are currently offline. "
                "The main DB cluster failed 10 minutes ago. "
                "Customer-facing APIs returning 503. "
                "Need immediate action from on-call engineer."
            ),
            "timestamp": "2024-01-15T03:22:00Z",
        },
        "rubric": {"expected_priority": "urgent"},
    },
    {
        "task_id": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the email priority as: low / medium / high / urgent",
        "email": {
            "id": "e002",
            "subject": "Team lunch next Friday",
            "sender": "hr@company.com",
            "body": (
                "Hi everyone, we're planning a team lunch on Friday the 20th at 12:30pm. "
                "Please fill out the RSVP form by Wednesday. No action needed if you can't make it."
            ),
            "timestamp": "2024-01-15T09:00:00Z",
        },
        "rubric": {"expected_priority": "low"},
    },
    {
        "task_id": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the email priority as: low / medium / high / urgent",
        "email": {
            "id": "e003",
            "subject": "Q4 board report due tomorrow",
            "sender": "cfo@company.com",
            "body": (
                "Hi, just a reminder that the Q4 financial summary slides are due tomorrow by 5pm. "
                "Please send your department's numbers to me by 3pm so I can compile them. "
                "This goes directly to the board."
            ),
            "timestamp": "2024-01-15T08:00:00Z",
        },
        "rubric": {"expected_priority": "high"},
    },
    {
        "task_id": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the email priority as: low / medium / high / urgent",
        "email": {
            "id": "e004",
            "subject": "Security breach detected — customer data potentially exposed",
            "sender": "security@company.com",
            "body": (
                "Our IDS flagged unusual outbound traffic at 2:14am. "
                "Initial analysis suggests up to 50,000 customer records may have been accessed. "
                "Legal and PR need to be looped in immediately. "
                "Incident response team please assemble now."
            ),
            "timestamp": "2024-01-15T02:30:00Z",
        },
        "rubric": {"expected_priority": "urgent"},
    },
    {
        "task_id": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the email priority as: low / medium / high / urgent",
        "email": {
            "id": "e005",
            "subject": "Office printer maintenance scheduled",
            "sender": "facilities@company.com",
            "body": (
                "The 3rd floor printers will be offline for routine maintenance on Tuesday between 10–11am. "
                "Please plan accordingly or use the 2nd floor printers during that time."
            ),
            "timestamp": "2024-01-15T11:00:00Z",
        },
        "rubric": {"expected_priority": "low"},
    },
    {
        "task_id": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the email priority as: low / medium / high / urgent",
        "email": {
            "id": "e006",
            "subject": "Client contract renewal — decision needed this week",
            "sender": "sales@company.com",
            "body": (
                "Acme Corp's annual contract expires on the 20th. "
                "They've asked for a 15% discount to renew. "
                "Need approval from leadership by Thursday — they'll go to a competitor otherwise."
            ),
            "timestamp": "2024-01-15T09:30:00Z",
        },
        "rubric": {"expected_priority": "high"},
    },

    # ─── MEDIUM: Action Extraction ─────────────────────────────────────────────
    {
        "task_id": "action_extraction",
        "difficulty": "medium",
        "description": "Extract all required action items from the email as a list of strings",
        "email": {
            "id": "e007",
            "subject": "Post-mortem follow-up actions",
            "sender": "engineering-lead@company.com",
            "body": (
                "Following yesterday's incident post-mortem, we have the following action items:\n"
                "1. Add circuit breaker to the payment service by end of sprint.\n"
                "2. Update runbook with new escalation path — owner: Sarah.\n"
                "3. Schedule a 30-min training on alerting for the team next week.\n"
                "4. File a ticket to audit all DB connection pool settings.\n"
                "Please confirm ownership by EOD."
            ),
            "timestamp": "2024-01-15T10:00:00Z",
        },
        "rubric": {
            "expected_actions": [
                "Add circuit breaker to the payment service by end of sprint",
                "Update runbook with new escalation path",
                "Schedule a 30-min training on alerting for the team",
                "File a ticket to audit all DB connection pool settings",
            ]
        },
    },
    {
        "task_id": "action_extraction",
        "difficulty": "medium",
        "description": "Extract all required action items from the email as a list of strings",
        "email": {
            "id": "e008",
            "subject": "Product launch checklist",
            "sender": "pm@company.com",
            "body": (
                "Hi team, launch is next Monday. Before then we need to:\n"
                "- Finalize the pricing page copy (marketing team).\n"
                "- Complete QA on the checkout flow.\n"
                "- Set up monitoring dashboards in Datadog.\n"
                "- Send press release to PR agency by Thursday.\n"
                "- Brief the support team on new FAQs.\n"
                "Let me know if anything is blocked."
            ),
            "timestamp": "2024-01-15T11:00:00Z",
        },
        "rubric": {
            "expected_actions": [
                "Finalize the pricing page copy",
                "Complete QA on the checkout flow",
                "Set up monitoring dashboards in Datadog",
                "Send press release to PR agency by Thursday",
                "Brief the support team on new FAQs",
            ]
        },
    },
    {
        "task_id": "action_extraction",
        "difficulty": "medium",
        "description": "Extract all required action items from the email as a list of strings",
        "email": {
            "id": "e009",
            "subject": "Board meeting prep",
            "sender": "ceo@company.com",
            "body": (
                "For next week's board meeting, I need everyone to submit their slides by Friday noon. "
                "Finance should prepare the updated P&L. "
                "Legal needs to confirm the IP filing status. "
                "HR, please have headcount numbers ready. "
                "I'll send the agenda by Wednesday."
            ),
            "timestamp": "2024-01-15T08:00:00Z",
        },
        "rubric": {
            "expected_actions": [
                "Submit slides by Friday noon",
                "Finance to prepare the updated P&L",
                "Legal to confirm IP filing status",
                "HR to have headcount numbers ready",
            ]
        },
    },
    {
        "task_id": "action_extraction",
        "difficulty": "medium",
        "description": "Extract all required action items from the email as a list of strings",
        "email": {
            "id": "e010",
            "subject": "Customer escalation — Acme Corp",
            "sender": "support-lead@company.com",
            "body": (
                "Acme Corp's CTO called in very upset. Their data export has been failing for 3 days. "
                "Action needed: Engineering to investigate the export pipeline bug today. "
                "Account manager to call them back within 2 hours. "
                "Prepare a written RCA to send by tomorrow EOD."
            ),
            "timestamp": "2024-01-15T13:00:00Z",
        },
        "rubric": {
            "expected_actions": [
                "Engineering to investigate the export pipeline bug today",
                "Account manager to call Acme Corp back within 2 hours",
                "Prepare a written RCA to send by tomorrow EOD",
            ]
        },
    },

    # ─── HARD: Full Triage ─────────────────────────────────────────────────────
    {
        "task_id": "full_triage",
        "difficulty": "hard",
        "description": (
            "Perform full triage: classify priority (low/medium/high/urgent), "
            "extract action items, identify sender intent, and suggest a response strategy"
        ),
        "email": {
            "id": "e011",
            "subject": "Immediate review required — compliance audit findings",
            "sender": "external-auditor@auditfirm.com",
            "body": (
                "Dear team,\n\n"
                "Following our audit completed last week, we have identified three critical findings "
                "that require immediate remediation:\n\n"
                "1. Access control logs are not being retained for the required 90 days.\n"
                "2. Two admin accounts have not been reviewed in over 180 days.\n"
                "3. Encryption at rest is not enabled on the backup storage bucket.\n\n"
                "These findings must be addressed within 30 days to avoid regulatory penalties. "
                "We require a written remediation plan within 5 business days.\n\n"
                "Please confirm receipt and assign owners for each finding."
            ),
            "timestamp": "2024-01-15T09:00:00Z",
        },
        "rubric": {
            "expected_priority": "urgent",
            "expected_actions": [
                "Retain access control logs for 90 days",
                "Review the two inactive admin accounts",
                "Enable encryption at rest on backup storage bucket",
                "Send written remediation plan within 5 business days",
                "Confirm receipt and assign owners",
            ],
            "expected_intent": "external compliance audit with regulatory deadline",
            "expected_escalate": True,
        },
    },
    {
        "task_id": "full_triage",
        "difficulty": "hard",
        "description": (
            "Perform full triage: classify priority (low/medium/high/urgent), "
            "extract action items, identify sender intent, and suggest a response strategy"
        ),
        "email": {
            "id": "e012",
            "subject": "Partnership proposal — co-marketing opportunity",
            "sender": "partnerships@bigcorp.com",
            "body": (
                "Hi,\n\n"
                "I'm reaching out from BigCorp's partnerships team. "
                "We'd love to explore a co-marketing campaign ahead of our joint product launch in March. "
                "We're proposing a 50/50 budget split and shared press coverage.\n\n"
                "We'd need a decision by Feb 1st to meet our campaign timeline. "
                "Could you set up a 30-min call with your marketing lead this week?\n\n"
                "Happy to share more details on the proposal."
            ),
            "timestamp": "2024-01-15T10:30:00Z",
        },
        "rubric": {
            "expected_priority": "medium",
            "expected_actions": [
                "Schedule a 30-min call with marketing lead this week",
                "Review the partnership proposal details",
                "Make a decision by Feb 1st",
            ],
            "expected_intent": "business development / co-marketing partnership request",
            "expected_escalate": False,
        },
    },
    {
        "task_id": "full_triage",
        "difficulty": "hard",
        "description": (
            "Perform full triage: classify priority (low/medium/high/urgent), "
            "extract action items, identify sender intent, and suggest a response strategy"
        ),
        "email": {
            "id": "e013",
            "subject": "Employee complaint — hostile work environment",
            "sender": "anonymous-hr-portal@company.com",
            "body": (
                "This is an anonymous submission via HR portal.\n\n"
                "I want to report that a manager in the engineering department has been making "
                "demeaning comments during team meetings for the past two months. "
                "Multiple people are affected but afraid to speak up. "
                "This is creating a hostile work environment and impacting productivity.\n\n"
                "I am requesting a formal investigation."
            ),
            "timestamp": "2024-01-15T14:00:00Z",
        },
        "rubric": {
            "expected_priority": "high",
            "expected_actions": [
                "Acknowledge receipt of complaint",
                "Open a formal HR investigation",
                "Maintain complainant anonymity",
                "Notify legal or compliance if required",
            ],
            "expected_intent": "formal workplace complaint requiring HR investigation",
            "expected_escalate": True,
        },
    },
    {
        "task_id": "full_triage",
        "difficulty": "hard",
        "description": (
            "Perform full triage: classify priority (low/medium/high/urgent), "
            "extract action items, identify sender intent, and suggest a response strategy"
        ),
        "email": {
            "id": "e014",
            "subject": "Vendor invoice — overdue 45 days",
            "sender": "billing@cloudprovider.com",
            "body": (
                "Dear accounts payable,\n\n"
                "Invoice #INV-2024-0045 for $42,500 is now 45 days overdue. "
                "Per our agreement, a late fee of 1.5% per month will be applied after 60 days. "
                "Please arrange payment immediately to avoid service interruption.\n\n"
                "Contact our billing team at billing@cloudprovider.com if you have questions."
            ),
            "timestamp": "2024-01-15T08:00:00Z",
        },
        "rubric": {
            "expected_priority": "high",
            "expected_actions": [
                "Process payment for invoice INV-2024-0045 of $42,500",
                "Confirm payment with vendor to avoid service interruption",
                "Investigate why payment was delayed",
            ],
            "expected_intent": "overdue invoice with threat of service interruption and late fees",
            "expected_escalate": False,
        },
    },
]