workspace "mad-scientist-skills" "Claude Code plugin providing architecture auditing, C4 architecture diagrams, cognitive interface auditing, security auditing, observability auditing, optimization auditing, documentation auditing, and pre-commit quality gates" {

    model {
        developer = person "Developer" "Uses Claude Code for software engineering tasks"

        plugin = softwareSystem "mad-scientist-skills" "Claude Code plugin with skills for architecture auditing, architecture visualization, cognitive interface auditing, security auditing, observability auditing, optimization auditing, documentation auditing, and pre-commit quality review" {
            architectureAuditSkill = container "architecture-audit Skill" "Architecture audit covering Hexagonal/Ports & Adapters, DDD bounded contexts, Clean Architecture, SOLID, coupling/cohesion, CQRS, Event Sourcing, Twelve-Factor, API-First, and ADRs (beta)" "SKILL.md"
            c4Skill = container "c4 Skill" "Generates interactive C4 architecture diagrams from Structurizr DSL" "SKILL.md, c4_assemble.py, 5 templates"
            cognitiveAuditSkill = container "cognitive-interface-audit Skill" "Cognitive interface audit covering GOMS, Norman's Gulfs, Wood error tolerance, Gergle visual grounding, NASA-TLX, Dual-Process Theory, Kirk data visualization integrity, Cleveland & McGill, Trust Calibration, Information Foraging, Gestalt, EID, and accessibility" "SKILL.md, 5 templates"
            documentationAuditSkill = container "documentation-audit Skill" "Single-tier documentation audit covering Diataxis structural taxonomy, Strunk & White linguistic precision, Google/Microsoft style guides, CLT pedagogical scaffolding, Carroll's Minimalism, Lemov instructional techniques, Voss tactical empathy, Kirk simplify-vs-clarify, information foraging, and audience calibration" "SKILL.md, 6 templates"
            finalReviewSkill = container "final-review Skill" "Pre-commit quality gate that reviews code, docs, and generates architecture diagrams" "SKILL.md"
            observabilityAuditSkill = container "observability-audit Skill" "Two-tier observability audit covering instrumentation, logging, metrics, tracing, pipeline/ML monitoring, alerting, and SLIs/SLOs (beta)" "SKILL.md, 7 templates"
            optimizationAuditSkill = container "optimization-audit Skill" "Single-tier optimization audit covering algorithm efficiency, database queries, caching, concurrency, pipelines, distributed execution, cloud cost, and profiling" "SKILL.md, 8 templates"
            securityAuditSkill = container "security-audit Skill" "Two-tier security audit covering STRIDE (incl. cross-org boundaries), OWASP Top 10, ML/AI model security, AI regulatory compliance, infrastructure (incl. confidential computing), and supply chain" "SKILL.md, 6 templates"
        }

        claudeCode = softwareSystem "Claude Code" "Anthropic CLI agent for software engineering" "External"
        structurizr = softwareSystem "Structurizr" "Exports DSL to PlantUML C4 format" "External"
        plantuml = softwareSystem "PlantUML" "Renders PlantUML diagrams to SVG" "External"

        developer -> claudeCode "Invokes skills via" "/mad-scientist-skills:<skill>"
        claudeCode -> plugin "Loads and executes" "Plugin system"
        claudeCode -> architectureAuditSkill "Invokes" "/mad-scientist-skills:architecture-audit"
        claudeCode -> c4Skill "Invokes" "/mad-scientist-skills:c4"
        claudeCode -> cognitiveAuditSkill "Invokes" "/mad-scientist-skills:cognitive-interface-audit"
        claudeCode -> documentationAuditSkill "Invokes" "/mad-scientist-skills:documentation-audit"
        claudeCode -> finalReviewSkill "Invokes" "/mad-scientist-skills:final-review"
        claudeCode -> observabilityAuditSkill "Invokes" "/mad-scientist-skills:observability-audit"
        claudeCode -> optimizationAuditSkill "Invokes" "/mad-scientist-skills:optimization-audit"
        claudeCode -> securityAuditSkill "Invokes" "/mad-scientist-skills:security-audit"
        finalReviewSkill -> c4Skill "Delegates diagram generation to" "Skill invocation"
        c4Skill -> structurizr "Exports DSL via" "structurizr.war CLI"
        c4Skill -> plantuml "Renders SVGs via" "plantuml.jar CLI"
    }

    views {
        systemContext plugin "SystemContext" {
            include *
            autoLayout
        }

        container plugin "Containers" {
            include *
            autoLayout
        }

        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
        }
    }

}
