# Unit Tests: {Component/Service Name}

## Test Implementation Scope
{Provide specific description of the component or service being tested at the unit level}

## ISTQB Test Case Design
**Test Design Technique**: {Select from: Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, Experience-Based Testing}

**Test Type**: Functional - Component Level Testing

**Component Type**: {Controller/Service/Repository/Utility/Model}

## Component Under Test

### Component Description:
{Provide detailed description of the component being tested}

### Dependencies:
- {List external dependencies that need mocking}

### Public Interface:
- {List public methods/properties to be tested}

## Test Cases to Implement

### Positive Test Cases:
- [ ] **Valid Input Scenarios**
  - {Describe valid input test cases}
  - Expected behavior: {Define expected outcomes}
  
- [ ] **Typical Use Cases**
  - {Describe common usage scenarios}
  - Expected results: {Define expected results}

### Negative Test Cases:
- [ ] **Invalid Input Handling**
  - {Describe invalid input scenarios}
  - Error handling: {Define error expectations}
  
- [ ] **Edge Case Validation**
  - {Describe boundary and edge cases}
  - Boundary behavior: {Define boundary expectations}

### Business Logic Tests:
- [ ] **Calculation Validation**
  - {Describe calculation scenarios if applicable}
  - Accuracy requirements: {Define accuracy expectations}
  
- [ ] **State Management**
  - {Describe state management scenarios}
  - State consistency: {Define state expectations}

## Mock and Stub Strategy

### External Dependencies to Mock:
- **Database Access**: {Define database mocking approach}
- **External APIs**: {Define API mocking strategy}
- **File System**: {Define file system mocking if needed}
- **Configuration**: {Define configuration mocking approach}

### Test Data Strategy:
- **Static Test Data**: {Define static data requirements}
- **Generated Test Data**: {Define data generation approach}
- **Data Builders**: {Define test data builder patterns}

## Test Implementation Details

### Test Framework:
- **Framework**: {MSTest/NUnit/xUnit}
- **Mocking Library**: {Moq/FakeItEasy/NSubstitute}
- **Assertion Library**: {FluentAssertions/Built-in}

### Test Structure:
```csharp
[TestClass]
public class {ComponentName}Tests
{
    // Arrange
    // Act  
    // Assert
}
```

### Test Categories:
- [ ] **Happy Path Tests**: {Number} test cases
- [ ] **Error Handling Tests**: {Number} test cases
- [ ] **Boundary Tests**: {Number} test cases
- [ ] **Performance Tests**: {Number} test cases (if applicable)

## Code Coverage Targets

### Coverage Requirements:
- **Line Coverage**: {percentage}% minimum
- **Branch Coverage**: {percentage}% minimum
- **Method Coverage**: {percentage}% minimum

### Critical Path Coverage:
- **Business Logic**: 100% coverage required
- **Error Handling**: 90% coverage required
- **Utility Functions**: 85% coverage required

## Test Organization

### Test Class Structure:
- **Setup Methods**: {Define setup requirements}
- **Teardown Methods**: {Define cleanup requirements}
- **Test Categories**: {Define test categorization}
- **Test Naming**: {Define naming conventions}

### Test Data Organization:
- **Test Constants**: {Define constant organization}
- **Test Helpers**: {Define helper method organization}
- **Test Fixtures**: {Define fixture organization}

## Performance Considerations

### Test Execution Performance:
- **Maximum Test Duration**: {time} milliseconds per test
- **Setup/Teardown Time**: Minimize setup and teardown overhead
- **Resource Usage**: Minimize memory and CPU usage

### Parallel Execution:
- **Thread Safety**: Ensure tests are thread-safe
- **Shared Resources**: Avoid shared mutable state
- **Isolation**: Maintain test isolation

## Acceptance Criteria
- [ ] All public methods have corresponding unit tests
- [ ] Code coverage targets met ({percentage}% line coverage)
- [ ] All test cases pass consistently
- [ ] Error scenarios properly tested
- [ ] Mock objects properly configured and verified
- [ ] Test execution time under {time} seconds
- [ ] No external dependencies in unit tests
- [ ] Test code follows coding standards

## Definition of Done
- [ ] Unit tests implemented for all required components
- [ ] Code coverage reports generated and reviewed
- [ ] All tests pass in CI/CD pipeline
- [ ] Mock strategy implemented and validated
- [ ] Test documentation updated
- [ ] Code review completed
- [ ] Performance benchmarks met
- [ ] Integration with build pipeline confirmed

## Dependencies

### Implementation Dependencies:
- {List implementation tasks that must be completed first}

### Framework Dependencies:
- {List testing framework setup requirements}

### Tool Dependencies:
- {List code coverage and testing tool requirements}

## Risk Assessment

### Testing Risks:
- **Complex Logic**: {Define approach for testing complex logic}
- **External Dependencies**: {Define strategy for isolating external dependencies}
- **Asynchronous Code**: {Define approach for testing async code}

### Mitigation Strategies:
- {List specific mitigation approaches for identified risks}

## Labels
`unit-test`, `{component-type}`, `functional-testing`, `{technology-stack}`, `{priority-level}`

## Estimate
{Unit test implementation effort: 0.5-2 story points per component}

## Linked Issues
- Implementation Story: #{story-number}
- Test Strategy: #{strategy-issue-number}
- Dependencies: #{dependency-issue-numbers}