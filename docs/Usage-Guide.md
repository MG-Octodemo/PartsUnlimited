# Workflow Documentation Generator Usage Guide

This guide explains how to use the Project Workflow Documentation Generator for any codebase.

## Overview

The documentation generator is a configurable prompt template that automatically detects technology stacks, architecture patterns, and generates comprehensive workflow documentation. It's designed to work with multiple technologies including .NET, Java/Spring, Node.js, React, and more.

## Quick Start

1. **Copy the generator template** from `workflow-documentation-generator.md`
2. **Set configuration variables** based on your project needs
3. **Apply the generated prompt** to analyze your codebase
4. **Review and customize** the output documentation

## Configuration Variables

### Required Variables

```
PROJECT_TYPE=Auto-detect|.NET|Java|Spring|Node.js|Python|React|Angular|Microservices|Other
```
- **Auto-detect**: Analyzes file extensions, folder structure, and dependencies
- **Specific type**: Focus analysis on particular technology patterns

```
WORKFLOW_COUNT=1-5
```
- Number of representative workflows to document
- Recommended: 3-4 for comprehensive coverage

### Optional Variables

```
ENTRY_POINT=Auto-detect|API|GraphQL|Frontend|CLI|Message Consumer|Scheduled Job|Custom
PERSISTENCE_TYPE=Auto-detect|SQL Database|NoSQL Database|File System|External API|Message Queue|Cache|None
ARCHITECTURE_PATTERN=Auto-detect|Layered|Clean|CQRS|Microservices|MVC|MVVM|Serverless|Event-Driven|Other
DETAIL_LEVEL=Standard|Implementation-Ready
INCLUDE_SEQUENCE_DIAGRAM=true|false
INCLUDE_TEST_PATTERNS=true|false
```

## Example Configurations

### .NET Web Application
```
PROJECT_TYPE=.NET
ENTRY_POINT=Auto-detect
PERSISTENCE_TYPE=SQL Database
ARCHITECTURE_PATTERN=Layered
WORKFLOW_COUNT=4
DETAIL_LEVEL=Implementation-Ready
INCLUDE_SEQUENCE_DIAGRAM=true
INCLUDE_TEST_PATTERNS=true
```

### Java Spring Boot Microservice
```
PROJECT_TYPE=Spring
ENTRY_POINT=API
PERSISTENCE_TYPE=SQL Database
ARCHITECTURE_PATTERN=Clean
WORKFLOW_COUNT=3
DETAIL_LEVEL=Implementation-Ready
INCLUDE_SEQUENCE_DIAGRAM=true
INCLUDE_TEST_PATTERNS=true
```

### React Frontend Application
```
PROJECT_TYPE=React
ENTRY_POINT=Frontend
PERSISTENCE_TYPE=External API
ARCHITECTURE_PATTERN=Auto-detect
WORKFLOW_COUNT=2
DETAIL_LEVEL=Standard
INCLUDE_SEQUENCE_DIAGRAM=false
INCLUDE_TEST_PATTERNS=true
```

### Node.js Microservices
```
PROJECT_TYPE=Node.js
ENTRY_POINT=Auto-detect
PERSISTENCE_TYPE=Auto-detect
ARCHITECTURE_PATTERN=Microservices
WORKFLOW_COUNT=5
DETAIL_LEVEL=Implementation-Ready
INCLUDE_SEQUENCE_DIAGRAM=true
INCLUDE_TEST_PATTERNS=true
```

## Auto-Detection Logic

When using `Auto-detect`, the generator examines:

### Technology Detection
- **File extensions**: `.cs`, `.java`, `.js`, `.py`, `.jsx`, `.ts`
- **Configuration files**: `package.json`, `pom.xml`, `.csproj`, `requirements.txt`
- **Framework files**: `Startup.cs`, `Application.java`, `app.js`, `webpack.config.js`

### Architecture Pattern Detection
- **Folder structure**: `/controllers`, `/services`, `/repositories`, `/models`
- **Naming patterns**: `*Controller`, `*Service`, `*Repository`
- **Design patterns**: Dependency injection, command/query separation

### Entry Point Detection
- **API controllers**: Classes with routing attributes/annotations
- **GraphQL**: Resolver classes and schema files
- **Message handlers**: Queue/event subscription patterns
- **Scheduled jobs**: Cron or timer configurations

## Generated Documentation Structure

The generator produces documentation with these sections:

1. **Technology Stack Detection** - Identified technologies and versions
2. **Architecture Overview** - High-level design patterns
3. **Workflow Documentation** - Detailed end-to-end flows including:
   - Entry points with full code examples
   - Service layer implementation
   - Data access patterns
   - Error handling strategies
   - Response construction
4. **Implementation Templates** - Reusable code patterns
5. **Naming Conventions** - Consistent patterns to follow
6. **Best Practices** - Guidelines and common pitfalls

## Customization Options

### Adding New Technology Support

To support a new technology stack:

1. Add detection logic in the "Initial Detection Phase"
2. Create technology-specific implementation patterns section
3. Include framework-specific naming conventions
4. Add relevant error handling patterns

Example for Django:
```
**Django Implementation Patterns (if detected):**
- Complete view class with decorators and middleware
- Model definitions with relationships
- Serializer implementations
- URL configuration patterns
- Settings configuration for databases
```

### Custom Architecture Patterns

For unique architecture patterns:

1. Add pattern detection logic
2. Create specific documentation sections
3. Include relevant implementation templates

Example for Event Sourcing:
```
**Event Sourcing Patterns:**
- Event store implementation
- Aggregate root patterns
- Command handlers
- Event handlers
- Projection builders
```

### Domain-Specific Customizations

For specific domains (e.g., fintech, healthcare, e-commerce):

1. Add domain-specific workflow types
2. Include compliance considerations
3. Add security pattern documentation
4. Include performance requirements

## Output Quality Guidelines

### High-Quality Documentation Includes:

1. **Complete Code Examples**: Full method implementations, not just signatures
2. **Error Handling**: Comprehensive exception and error response patterns
3. **Configuration**: All necessary setup and dependency registration
4. **Testing**: Unit test examples and integration test patterns
5. **Performance**: Caching, async patterns, and optimization strategies

### Documentation Depth Levels:

**Standard Level:**
- Method signatures and basic implementations
- High-level architecture overview
- Basic error handling

**Implementation-Ready Level:**
- Complete, runnable code examples
- Full error handling with all edge cases
- Performance optimizations
- Security considerations
- Testing strategies

## Common Use Cases

### 1. New Team Member Onboarding
```
PROJECT_TYPE=Auto-detect
WORKFLOW_COUNT=3
DETAIL_LEVEL=Implementation-Ready
INCLUDE_TEST_PATTERNS=true
```
Focus on core workflows with complete implementation details.

### 2. Architecture Documentation
```
PROJECT_TYPE=Auto-detect
ARCHITECTURE_PATTERN=Auto-detect
WORKFLOW_COUNT=5
INCLUDE_SEQUENCE_DIAGRAM=true
```
Comprehensive coverage with visual diagrams.

### 3. API Documentation
```
ENTRY_POINT=API
DETAIL_LEVEL=Implementation-Ready
INCLUDE_SEQUENCE_DIAGRAM=true
```
Focus on API endpoints with detailed request/response flows.

### 4. Legacy System Documentation
```
PROJECT_TYPE=Auto-detect
WORKFLOW_COUNT=4
DETAIL_LEVEL=Implementation-Ready
INCLUDE_TEST_PATTERNS=false
```
Document existing patterns without requiring test coverage.

## Integration with Development Workflow

### Continuous Documentation

1. **Git Hooks**: Run generator on significant commits
2. **CI/CD Integration**: Update documentation during builds
3. **Pull Request Process**: Include documentation updates

### Documentation as Code

1. Store configuration files in version control
2. Automate generation with scripts
3. Review documentation changes like code changes

### Team Collaboration

1. **Code Reviews**: Include documentation quality checks
2. **Architecture Decisions**: Document with workflow examples
3. **Knowledge Sharing**: Use generated docs for training

## Troubleshooting

### Common Issues

**Generator doesn't detect technology correctly:**
- Manually specify PROJECT_TYPE
- Check file structure matches expected patterns
- Verify configuration files are in correct locations

**Missing implementation details:**
- Set DETAIL_LEVEL=Implementation-Ready
- Increase WORKFLOW_COUNT to cover more patterns
- Enable INCLUDE_TEST_PATTERNS for testing examples

**Documentation too verbose:**
- Reduce WORKFLOW_COUNT
- Set DETAIL_LEVEL=Standard
- Disable optional sections like sequence diagrams

### Best Practices

1. **Start with auto-detect** to understand what the generator finds
2. **Iterate on configuration** to refine output quality
3. **Combine with manual review** for domain-specific details
4. **Keep configurations in version control** for team consistency
5. **Update regularly** as codebase evolves

## Example Output Quality

The PartsUnlimited example demonstrates high-quality output with:

- **4 representative workflows** covering API, repository, MVC, and complex data loading patterns
- **Complete code implementations** for all layers
- **Error handling patterns** with HTTP status codes and exceptions
- **Dependency injection** configuration and usage
- **Caching strategies** with implementation details
- **Implementation templates** for extending the application
- **Naming conventions** documented and consistently applied

This level of detail enables new developers to understand the codebase quickly and implement new features following established patterns.