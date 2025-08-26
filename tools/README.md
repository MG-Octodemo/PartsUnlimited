# Code Documentation Generator Tool

A comprehensive technology-agnostic prompt generator for documenting end-to-end application workflows. This tool automatically detects project architecture patterns, technology stacks, and data flow patterns to generate detailed implementation blueprints covering entry points, service layers, data access, error handling, and testing approaches across multiple technologies including .NET, Java/Spring, React, and microservices architectures.

## Features

- **Auto-Detection**: Automatically identifies technology stack, architecture patterns, and persistence mechanisms
- **Technology-Agnostic**: Supports multiple programming languages and frameworks
- **Comprehensive Analysis**: Analyzes entry points, service layers, data access patterns, and more
- **Implementation-Ready**: Generates detailed blueprints that serve as templates for new features
- **Configurable**: Customizable workflow count, detail level, and output options

## Supported Technologies

### Project Types
- .NET (ASP.NET, ASP.NET Core)
- Java (Spring Framework, vanilla Java)
- Node.js (Express, REST APIs)
- Python (Django, Flask, FastAPI)
- React (frontend applications)
- Angular (frontend applications)
- Microservices architectures

### Architecture Patterns
- Layered Architecture
- Clean Architecture  
- CQRS (Command Query Responsibility Segregation)
- MVC (Model-View-Controller)
- MVVM (Model-View-ViewModel)
- Microservices
- Event-Driven Architecture
- Serverless

### Persistence Types
- SQL Databases (Entity Framework, JPA, etc.)
- NoSQL Databases (MongoDB, Cosmos DB, etc.)
- File System storage
- External APIs
- Message Queues
- Caching solutions

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup
1. Clone or download the `code-documentation-generator.py` script
2. Make it executable:
   ```bash
   chmod +x code-documentation-generator.py
   ```

## Usage

### Basic Usage
```bash
python3 code-documentation-generator.py /path/to/your/codebase
```

### Advanced Usage
```bash
python3 code-documentation-generator.py /path/to/your/codebase \
  --workflows 5 \
  --output documentation.md
```

### Parameters

- `path`: Path to the codebase to analyze (required)
- `--workflows`: Number of representative workflows to document (default: 3)
- `--output`: Output file path for generated documentation (optional, prints to stdout if not specified)

## Configuration Variables

The tool automatically detects and configures the following variables:

- **PROJECT_TYPE**: Auto-detect|.NET|Java|Spring|Node.js|Python|React|Angular|Microservices|Other
- **ENTRY_POINT**: API|GraphQL|Frontend|CLI|Message Consumer|Scheduled Job|Custom
- **PERSISTENCE_TYPE**: Auto-detect|SQL Database|NoSQL Database|File System|External API|Message Queue|Cache|None
- **ARCHITECTURE_PATTERN**: Auto-detect|Layered|Clean|CQRS|Microservices|MVC|MVVM|Serverless|Event-Driven|Other
- **WORKFLOW_COUNT**: 1-5 (configurable via --workflows parameter)
- **DETAIL_LEVEL**: Implementation-Ready
- **INCLUDE_SEQUENCE_DIAGRAM**: true
- **INCLUDE_TEST_PATTERNS**: true

## Output Format

The generated documentation includes:

1. **Configuration Summary**: Auto-detected technology stack and patterns
2. **Detection Results**: Evidence and confidence level of auto-detection
3. **Workflow Documentation**: Detailed analysis of representative workflows
4. **Implementation Guidelines**: Technology-specific best practices and templates

## Example Output Structure

```markdown
# Application Workflow Documentation

## Configuration Variables (Auto-Detected)
- PROJECT_TYPE: .NET
- ENTRY_POINT: API, Frontend
- PERSISTENCE_TYPE: SQL Database
- ARCHITECTURE_PATTERN: MVC
- DETECTION_CONFIDENCE: 80.0%

## Initial Detection Phase Results
### Technology Stack Identified
### Detection Evidence
### Confidence Level

## Workflow Documentation
### Workflow 1: User Management Workflow
#### 1. Workflow Overview
#### 2. Implementation Pattern  
#### 3. Key Components

## Implementation Guidelines
### Technology-Specific Patterns
### Best Practices
### Next Steps
```

## Use Cases

### 1. Onboarding New Developers
Generate comprehensive documentation to help new team members understand the codebase architecture and implementation patterns.

### 2. Architecture Documentation
Create detailed architectural documentation for existing projects without extensive manual effort.

### 3. Code Reviews
Use generated patterns as templates to ensure new features follow established architectural guidelines.

### 4. Migration Planning
Analyze existing codebases to understand current patterns before planning migrations or refactoring.

### 5. Knowledge Transfer
Generate implementation blueprints for knowledge transfer between teams or when transitioning projects.

## Detection Algorithm

The tool uses multiple heuristics to detect technology patterns:

1. **File Pattern Analysis**: Examines file extensions and naming conventions
2. **Content Analysis**: Searches for technology-specific keywords and patterns
3. **Folder Structure**: Analyzes directory organization and naming
4. **Configuration Files**: Identifies build files, package managers, and configuration
5. **Framework Patterns**: Detects specific framework usage and conventions

## Limitations

- Detection accuracy depends on codebase size and pattern consistency
- Some complex or custom architectures may not be detected accurately
- Generated documentation is a starting point and may require manual refinement
- Large codebases may take longer to analyze

## Contributing

To extend the tool for additional technologies or patterns:

1. Add new enum values to `ProjectType`, `EntryPoint`, `PersistenceType`, or `ArchitecturePattern`
2. Implement detection logic in the corresponding `_detect_*` methods
3. Add technology-specific template generation in `DocumentationGenerator`
4. Test with sample codebases of the new technology

## License

This tool is provided as-is for documentation generation purposes. Modify and distribute according to your organization's policies.