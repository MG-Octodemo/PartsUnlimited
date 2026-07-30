#!/usr/bin/env python3
"""
Code Documentation Generator Tool
Automatically detects project architecture patterns, technology stacks, and data flow patterns
to generate detailed implementation blueprints following the comprehensive template.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

class ProjectType(Enum):
    DOTNET = ".NET"
    JAVA = "Java"
    SPRING = "Spring"
    NODEJS = "Node.js"
    PYTHON = "Python"
    REACT = "React"
    ANGULAR = "Angular"
    MICROSERVICES = "Microservices"
    OTHER = "Other"

class EntryPoint(Enum):
    API = "API"
    GRAPHQL = "GraphQL"
    FRONTEND = "Frontend"
    CLI = "CLI"
    MESSAGE_CONSUMER = "Message Consumer"
    SCHEDULED_JOB = "Scheduled Job"
    CUSTOM = "Custom"

class PersistenceType(Enum):
    SQL_DATABASE = "SQL Database"
    NOSQL_DATABASE = "NoSQL Database"
    FILE_SYSTEM = "File System"
    EXTERNAL_API = "External API"
    MESSAGE_QUEUE = "Message Queue"
    CACHE = "Cache"
    NONE = "None"

class ArchitecturePattern(Enum):
    LAYERED = "Layered"
    CLEAN = "Clean"
    CQRS = "CQRS"
    MICROSERVICES = "Microservices"
    MVC = "MVC"
    MVVM = "MVVM"
    SERVERLESS = "Serverless"
    EVENT_DRIVEN = "Event-Driven"
    OTHER = "Other"

@dataclass
class DetectionResult:
    project_type: ProjectType
    entry_points: List[EntryPoint]
    persistence_type: PersistenceType
    architecture_pattern: ArchitecturePattern
    confidence: float
    evidence: List[str]

@dataclass
class WorkflowInfo:
    name: str
    description: str
    entry_file: str
    related_files: List[str]
    business_purpose: str

class CodebaseAnalyzer:
    """Analyzes codebase structure to detect technology patterns and architecture."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.files = self._discover_files()
    
    def _discover_files(self) -> List[Path]:
        """Discover all relevant code files in the repository."""
        patterns = [
            "**/*.cs", "**/*.csproj", "**/*.sln",  # .NET
            "**/*.java", "**/*.xml", "**/*.gradle",  # Java
            "**/*.js", "**/*.ts", "**/*.json",  # JavaScript/TypeScript
            "**/*.py", "**/*.requirements.txt",  # Python
            "**/*.rb", "**/*.gemfile",  # Ruby
            "**/*.php", "**/*.composer.json",  # PHP
            "**/*.go", "**/*.mod",  # Go
        ]
        
        files = []
        for pattern in patterns:
            files.extend(self.root_path.glob(pattern))
        
        return [f for f in files if not any(exclude in str(f) for exclude in 
                ['node_modules', 'bin', 'obj', 'target', '__pycache__', '.git'])]
    
    def detect_project_patterns(self) -> DetectionResult:
        """Auto-detect project type, architecture, and persistence patterns."""
        evidence = []
        
        # Detect project type
        project_type = self._detect_project_type(evidence)
        
        # Detect entry points
        entry_points = self._detect_entry_points(evidence)
        
        # Detect persistence
        persistence_type = self._detect_persistence_type(evidence)
        
        # Detect architecture
        architecture_pattern = self._detect_architecture_pattern(evidence)
        
        # Calculate confidence based on evidence strength
        confidence = min(1.0, len(evidence) / 10.0)
        
        return DetectionResult(
            project_type=project_type,
            entry_points=entry_points,
            persistence_type=persistence_type,
            architecture_pattern=architecture_pattern,
            confidence=confidence,
            evidence=evidence
        )
    
    def _detect_project_type(self, evidence: List[str]) -> ProjectType:
        """Detect the primary project type based on file patterns and content."""
        
        # Check for .NET patterns
        if any(f.suffix == '.sln' for f in self.files):
            evidence.append("Found .NET solution file (.sln)")
            return ProjectType.DOTNET
        
        if any(f.suffix == '.csproj' for f in self.files):
            evidence.append("Found .NET project file (.csproj)")
            return ProjectType.DOTNET
        
        # Check for Java/Spring patterns
        if any('pom.xml' in f.name for f in self.files):
            evidence.append("Found Maven project file (pom.xml)")
            if self._check_file_content_contains(['spring', 'springframework']):
                evidence.append("Found Spring Framework references")
                return ProjectType.SPRING
            return ProjectType.JAVA
        
        if any('build.gradle' in f.name for f in self.files):
            evidence.append("Found Gradle build file")
            return ProjectType.JAVA
        
        # Check for Node.js patterns
        if any('package.json' in f.name for f in self.files):
            evidence.append("Found Node.js package.json")
            if self._check_file_content_contains(['react', 'jsx']):
                evidence.append("Found React components")
                return ProjectType.REACT
            if self._check_file_content_contains(['angular', '@angular']):
                evidence.append("Found Angular framework")
                return ProjectType.ANGULAR
            return ProjectType.NODEJS
        
        # Check for Python patterns
        if any('requirements.txt' in f.name or f.suffix == '.py' for f in self.files):
            evidence.append("Found Python files")
            return ProjectType.PYTHON
        
        return ProjectType.OTHER
    
    def _detect_entry_points(self, evidence: List[str]) -> List[EntryPoint]:
        """Detect application entry points."""
        entry_points = []
        
        # Check for API controllers
        if self._check_file_content_contains(['Controller', 'ApiController', '[Route', '[HttpGet']):
            evidence.append("Found API controller patterns")
            entry_points.append(EntryPoint.API)
        
        # Check for GraphQL
        if self._check_file_content_contains(['GraphQL', 'resolver', 'schema']):
            evidence.append("Found GraphQL patterns")
            entry_points.append(EntryPoint.GRAPHQL)
        
        # Check for frontend entry points
        if self._check_file_content_contains(['React', 'Vue', 'Angular', 'component']):
            evidence.append("Found frontend component patterns")
            entry_points.append(EntryPoint.FRONTEND)
        
        return entry_points if entry_points else [EntryPoint.API]
    
    def _detect_persistence_type(self, evidence: List[str]) -> PersistenceType:
        """Detect persistence mechanisms."""
        
        # Check for Entity Framework
        if self._check_file_content_contains(['DbContext', 'Entity Framework', 'DbSet']):
            evidence.append("Found Entity Framework patterns")
            return PersistenceType.SQL_DATABASE
        
        # Check for SQL patterns
        if self._check_file_content_contains(['SqlConnection', 'SELECT', 'INSERT', 'UPDATE']):
            evidence.append("Found SQL database patterns")
            return PersistenceType.SQL_DATABASE
        
        # Check for NoSQL patterns
        if self._check_file_content_contains(['MongoDB', 'Cosmos', 'DynamoDB']):
            evidence.append("Found NoSQL database patterns")
            return PersistenceType.NOSQL_DATABASE
        
        return PersistenceType.SQL_DATABASE
    
    def _detect_architecture_pattern(self, evidence: List[str]) -> ArchitecturePattern:
        """Detect architectural patterns."""
        
        # Check for MVC pattern
        if any('Controller' in f.name for f in self.files) and \
           any('Models' in str(f) for f in self.files) and \
           any('Views' in str(f) for f in self.files):
            evidence.append("Found MVC folder structure")
            return ArchitecturePattern.MVC
        
        # Check for Clean Architecture
        if self._check_file_content_contains(['UseCase', 'Interactor', 'Repository']):
            evidence.append("Found Clean Architecture patterns")
            return ArchitecturePattern.CLEAN
        
        # Check for CQRS
        if self._check_file_content_contains(['Command', 'Query', 'Handler']):
            evidence.append("Found CQRS patterns")
            return ArchitecturePattern.CQRS
        
        # Default to layered for traditional architectures
        evidence.append("Using layered architecture as default pattern")
        return ArchitecturePattern.LAYERED
    
    def _check_file_content_contains(self, patterns: List[str]) -> bool:
        """Check if any file contains the specified patterns."""
        for file_path in self.files:
            try:
                if file_path.suffix in ['.cs', '.java', '.js', '.ts', '.py', '.rb']:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if any(pattern.lower() in content.lower() for pattern in patterns):
                        return True
            except Exception:
                continue
        return False
    
    def identify_representative_workflows(self, count: int = 3) -> List[WorkflowInfo]:
        """Identify representative workflows in the codebase."""
        workflows = []
        
        # Find controllers as workflow entry points
        controller_files = [f for f in self.files if 'controller' in f.name.lower()]
        
        for controller_file in controller_files[:count]:
            try:
                content = controller_file.read_text(encoding='utf-8', errors='ignore')
                
                # Extract class name and methods
                class_match = re.search(r'class\s+(\w+)', content)
                if class_match:
                    class_name = class_match.group(1)
                    
                    # Find related files
                    base_name = class_name.replace('Controller', '')
                    related_files = [str(f) for f in self.files 
                                   if base_name.lower() in f.name.lower()]
                    
                    workflows.append(WorkflowInfo(
                        name=f"{base_name} Management Workflow",
                        description=f"Handles {base_name.lower()} operations and business logic",
                        entry_file=str(controller_file),
                        related_files=related_files,
                        business_purpose=f"Manage {base_name.lower()} entities and related operations"
                    ))
            except Exception:
                continue
        
        return workflows

class DocumentationGenerator:
    """Generates comprehensive workflow documentation based on analysis results."""
    
    def __init__(self, analyzer: CodebaseAnalyzer):
        self.analyzer = analyzer
    
    def generate_documentation(self, 
                             workflow_count: int = 3,
                             detail_level: str = "Implementation-Ready",
                             include_sequence_diagram: bool = True,
                             include_test_patterns: bool = True) -> str:
        """Generate comprehensive documentation following the template."""
        
        detection_result = self.analyzer.detect_project_patterns()
        workflows = self.analyzer.identify_representative_workflows(workflow_count)
        
        doc_parts = []
        
        # Header and configuration
        doc_parts.append(self._generate_header(detection_result, workflow_count, 
                                              detail_level, include_sequence_diagram, 
                                              include_test_patterns))
        
        # Detection phase results
        doc_parts.append(self._generate_detection_results(detection_result))
        
        # Workflow documentation
        doc_parts.append(self._generate_workflow_documentation(workflows, detection_result))
        
        # Implementation guidelines
        doc_parts.append(self._generate_implementation_guidelines(detection_result))
        
        return "\n\n".join(doc_parts)
    
    def _generate_header(self, detection_result: DetectionResult, workflow_count: int,
                        detail_level: str, include_sequence_diagram: bool,
                        include_test_patterns: bool) -> str:
        """Generate documentation header with configuration variables."""
        
        return f"""# Application Workflow Documentation

This document provides comprehensive end-to-end workflow documentation generated using automated codebase analysis.

## Configuration Variables (Auto-Detected)

- **PROJECT_TYPE**: {detection_result.project_type.value}
- **ENTRY_POINT**: {', '.join(ep.value for ep in detection_result.entry_points)}
- **PERSISTENCE_TYPE**: {detection_result.persistence_type.value}
- **ARCHITECTURE_PATTERN**: {detection_result.architecture_pattern.value}
- **WORKFLOW_COUNT**: {workflow_count}
- **DETAIL_LEVEL**: {detail_level}
- **INCLUDE_SEQUENCE_DIAGRAM**: {include_sequence_diagram}
- **INCLUDE_TEST_PATTERNS**: {include_test_patterns}
- **DETECTION_CONFIDENCE**: {detection_result.confidence:.1%}"""
    
    def _generate_detection_results(self, detection_result: DetectionResult) -> str:
        """Generate detection phase results section."""
        
        evidence_list = "\n".join(f"- {evidence}" for evidence in detection_result.evidence)
        
        return f"""## Initial Detection Phase Results

### Technology Stack Identified:
- **Primary Technology**: {detection_result.project_type.value}
- **Architecture Pattern**: {detection_result.architecture_pattern.value}
- **Persistence Mechanism**: {detection_result.persistence_type.value}
- **Entry Points**: {', '.join(ep.value for ep in detection_result.entry_points)}

### Detection Evidence:
{evidence_list}

### Confidence Level: {detection_result.confidence:.1%}"""
    
    def _generate_workflow_documentation(self, workflows: List[WorkflowInfo], 
                                       detection_result: DetectionResult) -> str:
        """Generate detailed workflow documentation."""
        
        workflow_sections = []
        
        for i, workflow in enumerate(workflows, 1):
            section = f"""### Workflow {i}: {workflow.name}

#### 1. Workflow Overview
- **Name**: {workflow.name}
- **Business Purpose**: {workflow.business_purpose}
- **Entry File**: `{workflow.entry_file}`
- **Related Files**: {len(workflow.related_files)} files identified

#### 2. Implementation Pattern
Based on detected {detection_result.architecture_pattern.value} architecture pattern with {detection_result.persistence_type.value} persistence.

#### 3. Key Components
- Entry point implementation in `{workflow.entry_file}`
- Supporting files: {', '.join(f'`{f}`' for f in workflow.related_files[:3])}
- Technology stack: {detection_result.project_type.value}"""
            
            workflow_sections.append(section)
        
        return "## Workflow Documentation\n\n" + "\n\n".join(workflow_sections)
    
    def _generate_implementation_guidelines(self, detection_result: DetectionResult) -> str:
        """Generate implementation guidelines specific to detected technology."""
        
        guidelines = f"""## Implementation Guidelines

### Technology-Specific Patterns for {detection_result.project_type.value}

#### Architecture Pattern: {detection_result.architecture_pattern.value}
- Follow established patterns for this architecture
- Maintain separation of concerns across layers
- Implement proper dependency injection

#### Persistence Pattern: {detection_result.persistence_type.value}
- Use appropriate data access patterns
- Implement proper transaction handling
- Follow async/await patterns where applicable

#### Best Practices
1. **Consistency**: Follow existing naming conventions and code organization
2. **Testing**: Implement unit and integration tests for new features
3. **Error Handling**: Use established error handling patterns
4. **Documentation**: Update documentation when adding new features
5. **Security**: Apply appropriate authentication and authorization

### Next Steps
1. Review identified workflows to understand implementation patterns
2. Use detected patterns as templates for new feature development
3. Ensure new code follows the established architecture
4. Add appropriate tests following existing patterns"""
        
        return guidelines

def main():
    """Main entry point for the documentation generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate comprehensive code documentation")
    parser.add_argument("path", help="Path to the codebase to analyze")
    parser.add_argument("--workflows", type=int, default=3, help="Number of workflows to document")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    # Analyze codebase
    analyzer = CodebaseAnalyzer(args.path)
    generator = DocumentationGenerator(analyzer)
    
    # Generate documentation
    documentation = generator.generate_documentation(workflow_count=args.workflows)
    
    # Output results
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(documentation)
        print(f"Documentation generated: {args.output}")
    else:
        print(documentation)

if __name__ == "__main__":
    main()