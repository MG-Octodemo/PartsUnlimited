---
name: Unit Tests
about: Create unit tests for individual components and functions
title: '[UNIT TEST] {Component/Function Name}'
labels: ['unit-test', 'component-test', 'istqb-technique']
assignees: ''
---

# Unit Tests: {Component/Function Name}

## Component Testing Scope

**Component/Function**: {Specific component or function being tested}
**Business Logic**: {Description of business logic being validated}
**Dependencies**: {List component dependencies and external interfaces}

## ISTQB Test Design Application

**Test Design Technique**: Equivalence Partitioning, Boundary Value Analysis
**Test Type**: Structural Testing (White-box)
**Coverage Target**: 80% line coverage, 90% branch coverage

## Test Cases to Implement

### Equivalence Partitioning
- [ ] **Valid Input Classes**: Test representative valid inputs
  - Input class 1: {Define valid input category}
  - Input class 2: {Define valid input category}
  - Expected behavior: {Define expected outcomes}

- [ ] **Invalid Input Classes**: Test representative invalid inputs
  - Invalid class 1: {Define invalid input category}
  - Invalid class 2: {Define invalid input category}
  - Expected behavior: {Error handling validation}

### Boundary Value Analysis
- [ ] **Minimum Valid Value**: Test minimum acceptable input
- [ ] **Maximum Valid Value**: Test maximum acceptable input
- [ ] **Just Below Minimum**: Test value just below minimum (invalid)
- [ ] **Just Above Maximum**: Test value just above maximum (invalid)
- [ ] **Typical Values**: Test normal operational values

### Business Logic Testing
- [ ] **Core Functionality**: Primary business rule validation
- [ ] **Edge Cases**: Unusual but valid business scenarios
- [ ] **Error Conditions**: Invalid business rule scenarios
- [ ] **State Changes**: Object state transition testing

## Implementation Tasks

### Test Setup
- [ ] **Test Framework Configuration**: MSTest/NUnit/xUnit setup
- [ ] **Mock Objects**: Create test doubles for dependencies
- [ ] **Test Data**: Prepare representative test data sets
- [ ] **Test Utilities**: Common testing helper functions

### Test Code Development
- [ ] **Happy Path Tests**: Primary functionality validation
- [ ] **Error Path Tests**: Exception and error handling
- [ ] **Boundary Tests**: Edge case validation
- [ ] **State Tests**: Object state verification

### Code Coverage Analysis
- [ ] **Coverage Measurement**: Use coverage tools (dotCover, Coverlet)
- [ ] **Coverage Reporting**: Generate coverage reports
- [ ] **Gap Analysis**: Identify uncovered code paths
- [ ] **Coverage Improvement**: Add tests for uncovered areas

## Acceptance Criteria

### Quality Standards
- [ ] All unit tests pass consistently
- [ ] Code coverage ≥ 80% line coverage
- [ ] Code coverage ≥ 90% branch coverage for critical paths
- [ ] No skipped or ignored tests without justification

### Performance Standards
- [ ] Unit test execution time < 10ms per test
- [ ] Total test suite execution < 30 seconds
- [ ] No external dependencies in unit tests
- [ ] Fast feedback for developers

### Code Quality Standards
- [ ] Tests follow naming conventions
- [ ] Test code is readable and maintainable
- [ ] Test isolation - no test dependencies
- [ ] Appropriate use of mocks and stubs

## Test Data Requirements

**Test Fixtures**: {Define required test data structures}
**Mock Data**: {Specify mock object requirements}
**Edge Case Data**: {Boundary and exceptional data sets}

## Dependencies

- [ ] Component implementation completed
- [ ] Interface contracts defined
- [ ] Test framework configured
- [ ] Mock framework available

## Estimate

**Implementation Effort**: 0.5-1 story point per component
- Simple components: 0.5 story points
- Complex business logic: 1 story point

## Definition of Done

- [ ] All test cases implemented and passing
- [ ] Code coverage targets achieved
- [ ] Test code reviewed and approved
- [ ] CI/CD integration completed
- [ ] Documentation updated