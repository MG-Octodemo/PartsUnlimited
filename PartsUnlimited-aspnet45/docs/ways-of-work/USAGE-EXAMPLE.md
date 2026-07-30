# Example: Using the Test Planning Framework

This document demonstrates how to use the comprehensive test planning framework implemented for PartsUnlimited.

## Sample GitHub Issue Creation

Below is an example of how to create test issues using the provided templates for the Shopping Cart Improvements feature:

### Test Strategy Issue Example

```markdown
# Test Strategy: Shopping Cart Improvements

## Test Strategy Overview
Comprehensive testing approach for enhanced shopping cart functionality including improved UX, performance optimization, and security enhancements following ISTQB and ISO 25010 standards.

## ISTQB Framework Application

**Test Design Techniques Used:**
- [x] Equivalence Partitioning
- [x] Boundary Value Analysis
- [x] Decision Table Testing
- [x] State Transition Testing
- [x] Experience-Based Testing

**Test Types Coverage:**
- [x] Functional Testing
- [x] Non-Functional Testing
- [x] Structural Testing
- [x] Change-Related Testing (Regression)

## ISO 25010 Quality Characteristics

**Priority Assessment:**
- [x] Functional Suitability: Critical
- [x] Performance Efficiency: High
- [x] Compatibility: High
- [x] Usability: High
- [x] Reliability: Critical
- [x] Security: Critical
- [x] Maintainability: Medium
- [x] Portability: Medium

## Quality Gates
- [x] Entry criteria defined
- [x] Exit criteria established
- [x] Quality thresholds documented

## Labels
`test-strategy`, `istqb`, `iso25010`, `quality-gates`

## Estimate
3 story points
```

### Playwright E2E Test Issue Example

```markdown
# Playwright Tests: Guest Checkout Workflow

## Test Implementation Scope
End-to-end testing of guest checkout workflow including cart operations, checkout process, and payment completion.

## ISTQB Test Case Design
**Test Design Technique**: State Transition Testing
**Test Type**: Functional

## Test Cases to Implement
**Functional Tests:**
- [x] Happy path scenarios (successful checkout)
- [x] Error handling validation (payment failures)
- [x] Boundary value testing (minimum/maximum quantities)
- [x] Input validation testing (invalid form data)

**Non-Functional Tests:**
- [x] Performance testing (response time ≤ 2 seconds)
- [x] Accessibility testing (WCAG compliance)
- [x] Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [x] Mobile responsiveness (iOS, Android)

## Playwright Implementation Tasks
- [x] Page Object Model development
- [x] Test fixture setup
- [x] Test data management
- [x] Test case implementation
- [x] Visual regression tests
- [x] CI/CD integration

## Acceptance Criteria
- [x] All test cases pass consistently
- [x] Code coverage targets met (80%)
- [x] Performance thresholds validated
- [x] Accessibility standards verified

## Labels
`playwright`, `e2e-test`, `quality-validation`

## Estimate
4 story points
```

## Framework Usage Workflow

### Step 1: Planning Phase
1. Create epic/feature directory: `docs/ways-of-work/plan/{epic-name}/{feature-name}/`
2. Copy and customize the three main documents from templates
3. Conduct risk assessment and prioritize quality characteristics

### Step 2: Issue Creation Phase
1. Use appropriate GitHub issue templates
2. Apply consistent labeling standards
3. Set priorities based on risk and business impact
4. Define dependencies and acceptance criteria

### Step 3: Execution Phase
1. Follow quality gates and entry/exit criteria
2. Track progress using test issues checklist
3. Validate coverage targets and metrics
4. Document lessons learned for continuous improvement

## Quality Metrics Dashboard (Example)

For the Shopping Cart Improvements feature, the following metrics would be tracked:

- **Test Coverage**: 85% (Target: 80%)
- **Defect Detection**: 97% (Target: 95%)
- **Performance**: 1.8s avg response time (Target: ≤2s)
- **Security**: 0 critical vulnerabilities (Target: 0)
- **Accessibility**: WCAG 2.1 AA compliant (Target: AA)

## Benefits Realized

1. **Standardized Approach**: Consistent testing methodology across all features
2. **Quality Assurance**: Systematic validation of all ISO 25010 characteristics
3. **Risk Management**: Proactive identification and mitigation of testing risks
4. **Traceability**: Clear mapping from requirements to test cases to quality metrics
5. **Continuous Improvement**: Data-driven insights for process optimization

This framework provides a scalable, industry-standard approach to test planning that can be applied to any feature or epic in the PartsUnlimited application.