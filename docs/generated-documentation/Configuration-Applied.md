# PartsUnlimited Documentation Generator Configuration

This file shows the specific configuration used to generate the workflow documentation for the PartsUnlimited application.

## Configuration Variables Applied

```
PROJECT_TYPE=.NET
ENTRY_POINT=Auto-detect
PERSISTENCE_TYPE=SQL Database  
ARCHITECTURE_PATTERN=Layered
WORKFLOW_COUNT=4
DETAIL_LEVEL=Implementation-Ready
INCLUDE_SEQUENCE_DIAGRAM=false
INCLUDE_TEST_PATTERNS=false
```

## Auto-Detection Results

The documentation generator automatically detected the following characteristics:

### Technology Stack
- **.NET Framework 4.5.1** - Detected from .csproj file and assembly references
- **ASP.NET MVC 5** - Detected from System.Web.Mvc version 5.2.3 reference
- **Entity Framework 6** - Detected from EntityFramework 6.1.3 package reference
- **Web API** - Detected from System.Web.Http references and /api folder structure
- **Unity Container** - Detected from Microsoft.Practices.Unity references and UnityConfig.cs

### Architecture Patterns
- **Layered Architecture** - Detected from folder structure (Controllers, Models, Utils, ViewModels)
- **Repository Pattern** - Detected from IRaincheckQuery, IOrdersQuery interfaces
- **Dependency Injection** - Detected from Unity container configuration
- **MVC Pattern** - Detected from Controllers inheriting from Controller base class

### Entry Points
- **Web API Controllers** - Detected ProductsController, RaincheckController in /api folder
- **MVC Controllers** - Detected HomeController, StoreController, etc. in /Controllers folder

### Persistence Mechanisms
- **SQL Database** - Detected from Entity Framework DbContext usage
- **Entity Framework ORM** - Detected from DbSet properties and OnModelCreating method
- **Connection String** - Detected "DefaultConnectionString" in context constructor

### Workflows Selected for Documentation

Based on code analysis, the most representative workflows were identified:

1. **API Product Retrieval** - Simple REST API pattern with Entity Framework
2. **Raincheck Management** - Complex async repository pattern with manual relationship loading
3. **Store Product Browsing** - MVC pattern with caching and view models
4. **Home Page Data Loading** - Complex data composition with multiple caching strategies

## Code Analysis Patterns Discovered

### Naming Conventions
- Controllers: `{Entity}Controller` pattern
- Repositories: `I{Entity}Query` interface, `{Entity}Query` implementation
- Models: Simple entity names (`Product`, `Order`, `Category`)
- View Models: `{Purpose}ViewModel` pattern

### Common Implementation Patterns
- **Async/Await**: Used consistently in repository layer
- **Dependency Injection**: Constructor injection with Unity
- **Caching**: MemoryCache.Default with expiration policies
- **Error Handling**: HTTP status codes and exceptions
- **Entity Framework**: Include() for eager loading, FirstOrDefaultAsync for queries

### Configuration Detection
- **Unity DI Configuration**: App_Start/UnityConfig.cs
- **Web API Routing**: Attribute routing with RoutePrefix
- **MVC Routing**: Convention-based routing
- **Entity Framework**: Code-first with explicit key configuration

This configuration resulted in implementation-ready documentation that includes complete code examples, error handling patterns, and reusable templates for extending the application.