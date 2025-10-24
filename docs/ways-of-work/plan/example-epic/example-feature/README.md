# Example Feature: User Shopping Cart

## Overview

This directory contains a complete example of test planning documentation for a User Shopping Cart feature, demonstrating how to apply the Test Planning & Quality Assurance framework.

## Purpose

This example serves as a reference for teams creating test documentation for their features. It shows:
- How to apply ISTQB test design techniques
- How to prioritize ISO 25010 quality characteristics
- How to structure comprehensive test planning
- How to create quality assurance documentation

## Feature Context

**Epic**: E-Commerce Enhancement  
**Feature**: User Shopping Cart  
**Description**: Allow users to add products to a shopping cart, modify quantities, and proceed to checkout.

### Key User Stories
1. As a customer, I want to add products to my cart so I can purchase multiple items
2. As a customer, I want to modify quantities in my cart so I can adjust my order
3. As a customer, I want to remove items from my cart so I can change my mind
4. As a customer, I want to see the total cost so I know how much I'll pay

## Documentation Structure

### Required Input Documents
Before creating test documentation, you should have:
- `feature.md` - Product requirements document (this file)
- `technical-breakdown.md` - Technical design and architecture
- `implementation-plan.md` - Development task breakdown
- `project-plan.md` - Project timeline and resources

### Test Planning Documents (Created Using Templates)
1. **test-strategy.md** - Comprehensive test strategy
2. **test-issues-checklist.md** - Detailed test issue checklist
3. **qa-plan.md** - Quality assurance and validation plan

## How to Use This Example

### Step 1: Study the Input Documents
Review the feature requirements and technical design to understand:
- Business requirements and acceptance criteria
- Technical architecture and components
- Implementation approach and timeline
- Key risks and dependencies

### Step 2: Review Test Strategy
Examine `test-strategy.md` to see:
- How ISTQB techniques are selected and applied
- How ISO 25010 characteristics are prioritized
- How test environment and data requirements are defined
- How quality gates are established

### Step 3: Review Test Issues Checklist
Examine `test-issues-checklist.md` to understand:
- How to break down testing into granular tasks
- How to estimate test effort using story points
- How to identify and document dependencies
- How to map tests to quality characteristics

### Step 4: Review QA Plan
Examine `qa-plan.md` to learn:
- How to define quality gates with entry/exit criteria
- How to establish quality metrics and thresholds
- How to manage dependencies and risks
- How to structure quality sign-off process

### Step 5: Apply to Your Feature
Use the templates and this example to create your own test documentation:
1. Create your feature directory: `docs/ways-of-work/plan/{epic-name}/{feature-name}/`
2. Copy templates from `docs/ways-of-work/templates/`
3. Fill in templates based on your feature requirements
4. Create GitHub issues using issue templates in `.github/ISSUE_TEMPLATE/`

## Key Concepts Demonstrated

### ISTQB Test Design Techniques
- **Equivalence Partitioning**: Grouping cart quantities (0, 1-10, 11-100, >100)
- **Boundary Value Analysis**: Testing cart quantity limits (0, 1, 100, 101)
- **Decision Table Testing**: Discount rules based on cart total and customer type
- **State Transition Testing**: Cart states (empty, items added, checked out)
- **Experience-Based Testing**: Common user errors and edge cases

### ISO 25010 Quality Characteristics
Priority focus for shopping cart:
1. **Functional Suitability** (Critical): Core cart operations must work correctly
2. **Usability** (Critical): Cart must be easy to use and accessible
3. **Performance Efficiency** (High): Cart operations must be fast
4. **Security** (High): Cart data must be protected
5. **Reliability** (Medium): Cart must handle errors gracefully
6. **Compatibility** (Medium): Works across browsers and devices

### Test Types Coverage
- **Unit Tests**: Cart service, price calculator, inventory validator
- **Integration Tests**: Cart API, payment gateway integration, inventory system
- **E2E Tests**: Complete shopping workflows using Playwright
- **Performance Tests**: Load testing for concurrent cart operations
- **Security Tests**: SQL injection, XSS, session management
- **Accessibility Tests**: WCAG AA compliance for cart UI

## Quality Metrics Examples

### Coverage Targets
- Code Coverage: 85% (high-risk: cart calculation logic)
- Functional Coverage: 100% of acceptance criteria
- Risk Coverage: 100% of high-risk scenarios (pricing, inventory)

### Quality Thresholds
- Test Pass Rate: ≥95%
- Performance: Cart operations <200ms
- Security: Zero critical vulnerabilities
- Accessibility: WCAG AA compliance (score ≥95)
- Defect Density: ≤2 defects per KLOC

## References

### Framework Documentation
- Main README: `/docs/ways-of-work/README.md`
- Test Strategy Template: `/docs/ways-of-work/templates/test-strategy-template.md`
- Test Issues Template: `/docs/ways-of-work/templates/test-issues-checklist-template.md`
- QA Plan Template: `/docs/ways-of-work/templates/qa-plan-template.md`

### GitHub Issue Templates
- Test Strategy: `.github/ISSUE_TEMPLATE/test-strategy.md`
- Playwright Test: `.github/ISSUE_TEMPLATE/playwright-test.md`
- Quality Assurance: `.github/ISSUE_TEMPLATE/quality-assurance.md`

## Tips for Success

1. **Start Early**: Begin test planning during requirements phase
2. **Focus on Risk**: Prioritize testing based on risk assessment
3. **Be Specific**: Define clear, measurable acceptance criteria
4. **Automate**: Prioritize test automation, especially for regression
5. **Collaborate**: Involve QA in design and implementation reviews
6. **Measure**: Track quality metrics throughout development
7. **Iterate**: Refine test approach based on findings and feedback

## Questions?

If you need help applying this framework to your feature:
1. Review the template documentation carefully
2. Study this example as a reference
3. Consult with the QA team for guidance
4. Iterate and improve based on feedback

---

**Document Type**: Example / Reference
**Last Updated**: 2025-10-24
**Status**: Complete
