---
name: Playwright E2E Test
about: Create end-to-end tests using Playwright for user workflow validation
title: '[E2E TEST] {User Story/Component Name}'
labels: ['playwright', 'e2e-test', 'quality-validation']
assignees: ''
---

# Playwright Tests: {Story/Component Name}

## Test Implementation Scope
{Specific user story or component being tested}

## ISTQB Test Case Design
**Test Design Technique**: {Selected ISTQB technique}
**Test Type**: {Functional/Non-Functional/Structural/Change-Related}

## User Workflow
**Primary User Flow:**
{Describe the main user journey being tested}

**Alternative Flows:**
{Describe any alternative paths or edge cases}

## Test Cases to Implement

### Functional Tests:
- [ ] Happy path scenarios
  - {Specific test case description}
  - {Expected behavior and outcomes}
- [ ] Error handling validation
  - {Error scenario description}
  - {Expected error handling behavior}
- [ ] Boundary value testing
  - {Boundary conditions to test}
  - {Expected behavior at boundaries}
- [ ] Input validation testing
  - {Invalid input scenarios}
  - {Expected validation behavior}

### Non-Functional Tests:
- [ ] Performance testing (response time < {threshold})
  - {Performance criteria and measurement approach}
- [ ] Accessibility testing (WCAG compliance)
  - {Specific accessibility requirements}
- [ ] Cross-browser compatibility
  - Chrome {version}, Firefox {version}, Safari {version}, Edge {version}
- [ ] Mobile responsiveness
  - iOS Safari, Chrome Mobile, responsive breakpoints

## Playwright Implementation Tasks
- [ ] Page Object Model development
  - {List key page objects needed}
- [ ] Test fixture setup
  - {Authentication, data setup, environment configuration}
- [ ] Test data management
  - {Test data requirements and preparation}
- [ ] Test case implementation
  - {Specific test scenarios to automate}
- [ ] Visual regression tests
  - {Screenshots and visual validation points}
- [ ] CI/CD integration
  - {Pipeline integration requirements}

## Test Environment Requirements
**Browser Configurations:**
- [ ] Chrome (latest)
- [ ] Firefox (latest) 
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

**Test Data Requirements:**
- [ ] {Specific data needed for testing}
- [ ] {User accounts or authentication requirements}
- [ ] {Product or catalog data requirements}

**Environment Dependencies:**
- [ ] {Staging environment access}
- [ ] {Third-party service mocks or integrations}
- [ ] {Database state or configuration}

## Acceptance Criteria
- [ ] All test cases pass consistently
- [ ] Code coverage targets met (80% for E2E flows)
- [ ] Performance thresholds validated
- [ ] Accessibility standards verified (WCAG 2.1 AA)
- [ ] Cross-browser compatibility confirmed
- [ ] Mobile responsiveness validated

## Test Scenarios Detail

### Scenario 1: {Scenario Name}
**Given**: {Initial conditions}
**When**: {User actions}
**Then**: {Expected outcomes}

### Scenario 2: {Scenario Name}
**Given**: {Initial conditions}
**When**: {User actions}
**Then**: {Expected outcomes}

## Error Handling Tests
- [ ] Network connectivity issues
- [ ] Service unavailability scenarios
- [ ] Session timeout handling
- [ ] Data validation failures
- [ ] Authentication/authorization errors

## Performance Validation
- [ ] Page load times < {threshold}ms
- [ ] User action response times < {threshold}ms
- [ ] Resource loading optimization
- [ ] Memory usage validation

## Definition of Done
- [ ] All Playwright tests implemented and passing
- [ ] Page Object Model following best practices
- [ ] Test data cleanup and isolation
- [ ] CI/CD pipeline integration complete
- [ ] Cross-browser testing validated
- [ ] Performance benchmarks met
- [ ] Code review completed and approved
- [ ] Documentation updated with test scenarios

## Estimate
{Test implementation effort: 2-5 story points}

## Dependencies
- [ ] {UI components implementation complete}
- [ ] {API endpoints available and tested}
- [ ] {Test environment configured}
- [ ] {Test data available}

## Risk Considerations
- [ ] {Flaky test potential and mitigation}
- [ ] {Environment stability issues}
- [ ] {Third-party service dependencies}
- [ ] {Data consistency challenges}