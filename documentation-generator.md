# PartsUnlimited Application Workflow Documentation

This document provides comprehensive end-to-end workflow documentation for the PartsUnlimited .NET MVC application, generated using the technology-agnostic workflow documentation template.

## Configuration Variables (Auto-Detected)

- **PROJECT_TYPE**: .NET (ASP.NET MVC 4.5)
- **ENTRY_POINT**: API + Frontend (MVC Controllers + Web API)
- **PERSISTENCE_TYPE**: SQL Database (Entity Framework)
- **ARCHITECTURE_PATTERN**: Layered (MVC + Repository pattern)
- **WORKFLOW_COUNT**: 3 representative workflows
- **DETAIL_LEVEL**: Implementation-Ready
- **INCLUDE_SEQUENCE_DIAGRAM**: true
- **INCLUDE_TEST_PATTERNS**: true

## Initial Detection Phase Results

### Technology Stack Identified:
- **Primary Framework**: .NET ASP.NET MVC 4.5
- **Programming Language**: C#
- **Database ORM**: Entity Framework 6.x
- **Dependency Injection**: Unity Container
- **Authentication**: ASP.NET Identity with OWIN
- **Frontend**: Razor Views with JavaScript/jQuery
- **Testing**: MSTest with Selenium for UI tests

### Entry Points Identified:
- **MVC Controllers**: AccountController, StoreController, ManageController, etc.
- **Web API Controllers**: RaincheckController for external API access
- **Authentication endpoints**: Login, Register, External login providers

### Persistence Mechanisms:
- **Primary Database**: SQL Server via Entity Framework
- **DbContext**: PartsUnlimitedContext with IdentityDbContext
- **Repository Pattern**: Query classes (IRaincheckQuery, IOrdersQuery)
- **Entities**: Product, Order, Category, CartItem, Store, Raincheck, ApplicationUser

## Workflow Documentation

### Workflow 1: User Registration and Authentication

#### 1. Workflow Overview
- **Name**: User Registration and Authentication Workflow
- **Business Purpose**: Allow new users to register and existing users to authenticate
- **Triggering Action**: HTTP POST to /Account/Register or /Account/Login
- **Files Involved**:
  - `Controllers/AccountController.cs`
  - `Models/AccountViewModels.cs`
  - `Models/ApplicationUser.cs`
  - `Views/Account/Register.cshtml`
  - `Views/Account/Login.cshtml`

#### 2. Entry Point Implementation

**MVC Controller Entry Points:**
```csharp
[AllowAnonymous]
public ActionResult Register()
{
    return View();
}

[HttpPost]
[AllowAnonymous]
[ValidateAntiForgeryToken]
public async Task<ActionResult> Register(RegisterViewModel model)
{
    if (ModelState.IsValid)
    {
        var user = new ApplicationUser { UserName = model.Email, Email = model.Email };
        var result = await UserManager.CreateAsync(user, model.Password);
        if (result.Succeeded)
        {
            await SignInManager.SignInAsync(user, isPersistent:false, rememberBrowser:false);
            return RedirectToAction("Index", "Home");
        }
        AddErrors(result);
    }
    return View(model);
}
```

**Request DTO/Model:**
```csharp
public class RegisterViewModel
{
    [Required]
    [EmailAddress]
    [Display(Name = "Email")]
    public string Email { get; set; }

    [Required]
    [StringLength(100, ErrorMessage = "The {0} must be at least {2} characters long.", MinimumLength = 6)]
    [DataType(DataType.Password)]
    [Display(Name = "Password")]
    public string Password { get; set; }

    [DataType(DataType.Password)]
    [Display(Name = "Confirm password")]
    [Compare("Password", ErrorMessage = "The password and confirmation password do not match.")]
    public string ConfirmPassword { get; set; }
}
```

**Authentication/Authorization:**
- Uses `[AllowAnonymous]` attribute for registration endpoints
- OWIN middleware handles authentication context
- ASP.NET Identity handles user management and password hashing

#### 3. Service Layer Implementation

**User Management Services:**
```csharp
private UserManager<ApplicationUser> UserManager
{
    get
    {
        return HttpContext.GetOwinContext().GetUserManager<UserManager<ApplicationUser>>();
    }
}

private SignInManager<ApplicationUser, string> SignInManager
{
    get
    {
        return HttpContext.GetOwinContext().Get<SignInManager<ApplicationUser, string>>();
    }
}
```

**Dependency Injection Registration (Unity):**
```csharp
// In UnityConfig.cs
public static UnityContainer BuildContainer()
{
    var container = new UnityContainer();
    // ASP.NET Identity services are registered via OWIN in Startup.cs
    return container;
}
```

#### 4. Data Mapping Patterns
- **ViewModel to Domain**: RegisterViewModel → ApplicationUser
- **Manual mapping** in controller action
- **Password hashing** handled by ASP.NET Identity automatically

#### 5. Data Access Implementation

**Entity Definition:**
```csharp
public class ApplicationUser : IdentityUser
{
    // Additional properties can be added here
}
```

**DbContext:**
```csharp
public class PartsUnlimitedContext : IdentityDbContext<ApplicationUser>, IPartsUnlimitedContext
{
    public PartsUnlimitedContext() : base("name=DefaultConnectionString")
    {
    }
    // User management tables are created by IdentityDbContext
}
```

**Transaction Handling:**
- ASP.NET Identity handles database transactions internally
- Entity Framework manages connection and transaction lifecycle

#### 6. Response Construction
- **Success**: Redirect to Home/Index
- **Failure**: Return View with ModelState errors
- **Status Codes**: 200 for view returns, 302 for redirects

#### 7. Error Handling Patterns

**Validation Errors:**
```csharp
if (!ModelState.IsValid)
{
    return View(model);
}

private void AddErrors(IdentityResult result)
{
    foreach (var error in result.Errors)
    {
        ModelState.AddModelError("", error);
    }
}
```

**Exception Types:**
- `IdentityResult.Errors` for user creation failures
- `ModelState` validation errors
- Global exception handling via `Application_Error` in Global.asax

### Workflow 2: Product Browsing and Details

#### 1. Workflow Overview
- **Name**: Product Browsing and Details Workflow
- **Business Purpose**: Allow users to browse products by category and view detailed product information
- **Triggering Action**: HTTP GET to /Store/Browse/{categoryId} or /Store/Details/{productId}
- **Files Involved**:
  - `Controllers/StoreController.cs`
  - `Models/Product.cs`
  - `Models/Category.cs`
  - `Models/PartsUnlimitedContext.cs`
  - `Views/Store/Browse.cshtml`
  - `Views/Store/Details.cshtml`

#### 2. Entry Point Implementation

**MVC Controller Entry Points:**
```csharp
public class StoreController : Controller
{
    private readonly IPartsUnlimitedContext db;

    public StoreController(IPartsUnlimitedContext context)
    {
        db = context;
    }

    // GET: /Store/Browse?categoryId=1
    public ActionResult Browse(int categoryId)
    {
        var genreModel = db.Categories.Include("Products").Single(g => g.CategoryId == categoryId);
        return View(genreModel);
    }

    // GET: /Store/Details/5
    public ActionResult Details(int id)
    {
        var productCacheKey = string.Format("product_{0}", id);
        var product = MemoryCache.Default[productCacheKey] as Product;
        if (product == null)
        {
            product = db.Products.Single(a => a.ProductId == id);
            MemoryCache.Default.Add(productCacheKey, product, 
                new CacheItemPolicy { SlidingExpiration = TimeSpan.FromMinutes(10) });
        }
        return View(product);
    }
}
```

#### 3. Service Layer Implementation
- **Direct DbContext usage** in this pattern (typical for MVC)
- **Caching layer** implemented using MemoryCache for performance

#### 4. Data Access Implementation

**Entity Definitions:**
```csharp
public class Product
{
    public int ProductId { get; set; }
    public string Title { get; set; }
    public decimal Price { get; set; }
    public string ProductArtUrl { get; set; }
    public int CategoryId { get; set; }
    public virtual Category Category { get; set; }
}

public class Category
{
    public int CategoryId { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public virtual List<Product> Products { get; set; }
}
```

**DbContext Configuration:**
```csharp
protected override void OnModelCreating(DbModelBuilder builder)
{
    builder.Entity<Product>().HasKey(a => a.ProductId);
    builder.Entity<Category>().HasKey(g => g.CategoryId);
    base.OnModelCreating(builder);
}
```

**Query Patterns:**
- **Eager Loading**: `db.Categories.Include("Products")`
- **Single Entity**: `db.Products.Single(a => a.ProductId == id)`
- **Caching**: MemoryCache for frequently accessed products

### Workflow 3: Raincheck API Management

#### 1. Workflow Overview
- **Name**: Raincheck API Management Workflow
- **Business Purpose**: Provide external API access for managing rainchecks (out-of-stock item requests)
- **Triggering Action**: HTTP requests to /api/raincheck endpoints
- **Files Involved**:
  - `api/RaincheckController.cs`
  - `Utils/IRaincheckQuery.cs`
  - `Utils/RaincheckQuery.cs`
  - `Models/Raincheck.cs`
  - `App_Start/UnityConfig.cs`

#### 2. Entry Point Implementation

**Web API Controller:**
```csharp
[RoutePrefix("api/raincheck")]
public class RaincheckController : ApiController
{
    private readonly IRaincheckQuery _query;

    public RaincheckController(IRaincheckQuery query)
    {
        _query = query;
    }

    [HttpGet, Route]
    public Task<IEnumerable<Raincheck>> Get()
    {
        return _query.GetAllAsync();
    }

    [HttpGet, Route("{id}")]
    public Task<Raincheck> Get(int id)
    {
        return _query.FindAsync(id);
    }

    [HttpPost, Route]
    public Task<int> Post([FromBody]Raincheck raincheck)
    {
        return _query.AddAsync(raincheck);
    }
}
```

#### 3. Service Layer Implementation

**Repository Interface:**
```csharp
public interface IRaincheckQuery
{
    Task<int> AddAsync(Raincheck raincheck);
    Task<Raincheck> FindAsync(int id);
    Task<IEnumerable<Raincheck>> GetAllAsync();
}
```

**Repository Implementation:**
```csharp
public class RaincheckQuery : IRaincheckQuery
{
    private readonly IPartsUnlimitedContext context;

    public RaincheckQuery(IPartsUnlimitedContext context)
    {
        this.context = context;
    }

    public async Task<IEnumerable<Raincheck>> GetAllAsync()
    {
        var rainchecks = await context.RainChecks.ToListAsync();
        foreach (var raincheck in rainchecks)
        {
            await FillRaincheckValuesAsync(raincheck);
        }
        return rainchecks;
    }

    public async Task<Raincheck> FindAsync(int id)
    {
        var raincheck = await context.RainChecks.FirstOrDefaultAsync(r => r.RaincheckId == id);
        if (raincheck == null)
        {
            throw new ArgumentOutOfRangeException("id");
        }
        await FillRaincheckValuesAsync(raincheck);
        return raincheck;
    }

    public async Task<int> AddAsync(Raincheck raincheck)
    {
        var addedRaincheck = context.RainChecks.Add(raincheck);
        await context.SaveChangesAsync(CancellationToken.None);
        return addedRaincheck.RaincheckId;
    }

    private async Task FillRaincheckValuesAsync(Raincheck raincheck)
    {
        raincheck.IssuerStore = await context.Stores.FirstAsync(s => s.StoreId == raincheck.StoreId);
        raincheck.Product = await context.Products.FirstAsync(p => p.ProductId == raincheck.ProductId);
        raincheck.Product.Category = await context.Categories.FirstAsync(c => c.CategoryId == raincheck.Product.CategoryId);
    }
}
```

**Dependency Injection Registration:**
```csharp
public static UnityContainer BuildContainer()
{
    var container = new UnityContainer();
    container.RegisterType<IPartsUnlimitedContext, PartsUnlimitedContext>();
    container.RegisterType<IRaincheckQuery, RaincheckQuery>();
    return container;
}
```

#### 4. Data Mapping Patterns
- **Direct entity usage** for API responses (JSON serialization)
- **Manual lazy loading** implementation to work around EF limitations

#### 5. Data Access Implementation

**Entity Definition:**
```csharp
public class Raincheck
{
    public int RaincheckId { get; set; }
    public string Name { get; set; }
    public int ProductId { get; set; }
    public virtual Product Product { get; set; }
    public int Count { get; set; }
    public double SalePrice { get; set; }
    public int StoreId { get; set; }
    public virtual Store IssuerStore { get; set; }
}
```

**Async Patterns:**
- All operations are async using `Task<T>`
- Entity Framework async methods (`ToListAsync`, `FirstOrDefaultAsync`)
- Cancellation token support for save operations

#### 6. Error Handling Patterns
```csharp
if (raincheck == null)
{
    throw new ArgumentOutOfRangeException("id");
}
```

**Global API Error Handling:**
- Web API automatically handles exceptions and returns appropriate HTTP status codes
- Model validation handled by `[FromBody]` parameter binding

## Testing Approach

### Unit Testing Patterns
```csharp
[TestClass]
public class RaincheckQueryTests
{
    [TestMethod]
    public async Task FindAsync_ValidId_ReturnsRaincheck()
    {
        // Arrange
        var mockContext = new Mock<IPartsUnlimitedContext>();
        var query = new RaincheckQuery(mockContext.Object);
        
        // Act & Assert
        // Test implementation
    }
}
```

### Integration Testing
- Selenium tests in `FabrikamFiber.SeleniumTests` project
- Database integration tests using in-memory or test database

## Naming Conventions

### Consistent Patterns:
- **Controllers**: `{EntityName}Controller` (e.g., `AccountController`, `StoreController`)
- **API Controllers**: `{EntityName}Controller` with `[RoutePrefix]` (e.g., `RaincheckController`)
- **Services/Queries**: `I{EntityName}Query` interface and `{EntityName}Query` implementation
- **Models**: `{EntityName}` for domain models, `{EntityName}ViewModel` for view models
- **DbSets**: Plural entity names (`Products`, `Categories`, `RainChecks`)

### Method Naming:
- **CRUD Operations**: `GetAllAsync()`, `FindAsync(id)`, `AddAsync(entity)`
- **Controller Actions**: HTTP verb + descriptive name (`Get()`, `Post()`, `Browse()`, `Details()`)

## Implementation Templates

### Creating a New API Endpoint
```csharp
[RoutePrefix("api/[entityname]")]
public class [EntityName]Controller : ApiController
{
    private readonly I[EntityName]Query _query;

    public [EntityName]Controller(I[EntityName]Query query)
    {
        _query = query;
    }

    [HttpGet, Route]
    public Task<IEnumerable<[EntityName]>> Get()
    {
        return _query.GetAllAsync();
    }

    [HttpGet, Route("{id}")]
    public Task<[EntityName]> Get(int id)
    {
        return _query.FindAsync(id);
    }

    [HttpPost, Route]
    public Task<int> Post([FromBody][EntityName] entity)
    {
        return _query.AddAsync(entity);
    }
}
```

### Implementing a New Repository
```csharp
public interface I[EntityName]Query
{
    Task<int> AddAsync([EntityName] entity);
    Task<[EntityName]> FindAsync(int id);
    Task<IEnumerable<[EntityName]>> GetAllAsync();
}

public class [EntityName]Query : I[EntityName]Query
{
    private readonly IPartsUnlimitedContext context;

    public [EntityName]Query(IPartsUnlimitedContext context)
    {
        this.context = context;
    }

    public async Task<IEnumerable<[EntityName]>> GetAllAsync()
    {
        return await context.[EntityName]s.ToListAsync();
    }

    public async Task<[EntityName]> FindAsync(int id)
    {
        var entity = await context.[EntityName]s.FirstOrDefaultAsync(e => e.[EntityName]Id == id);
        if (entity == null)
        {
            throw new ArgumentOutOfRangeException("id");
        }
        return entity;
    }

    public async Task<int> AddAsync([EntityName] entity)
    {
        var added = context.[EntityName]s.Add(entity);
        await context.SaveChangesAsync(CancellationToken.None);
        return added.[EntityName]Id;
    }
}
```

## .NET Implementation Patterns

### Complete Controller with Dependency Injection
```csharp
[Authorize] // or [AllowAnonymous] as needed
public class [EntityName]Controller : Controller
{
    private readonly IPartsUnlimitedContext db;

    public [EntityName]Controller(IPartsUnlimitedContext context)
    {
        db = context;
    }

    public ActionResult Index()
    {
        var entities = db.[EntityName]s.ToList();
        return View(entities);
    }

    public ActionResult Details(int id)
    {
        var entity = db.[EntityName]s.Single(e => e.[EntityName]Id == id);
        return View(entity);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public ActionResult Create([EntityName]ViewModel model)
    {
        if (ModelState.IsValid)
        {
            // Map ViewModel to Entity
            var entity = new [EntityName] { /* mapping */ };
            db.[EntityName]s.Add(entity);
            db.SaveChanges();
            return RedirectToAction("Index");
        }
        return View(model);
    }
}
```

### Entity Framework Configuration
```csharp
protected override void OnModelCreating(DbModelBuilder builder)
{
    builder.Entity<[EntityName]>().HasKey(e => e.[EntityName]Id);
    // Configure relationships, constraints, etc.
    base.OnModelCreating(builder);
}
```

### Unity Container Registration
```csharp
container.RegisterType<I[EntityName]Query, [EntityName]Query>();
container.RegisterType<IPartsUnlimitedContext, PartsUnlimitedContext>();
```

## Implementation Guidelines

### Step-by-Step Implementation Process
1. **Define Entity Model** with appropriate properties and relationships
2. **Create Repository Interface** following `I{EntityName}Query` pattern
3. **Implement Repository** with async patterns and error handling
4. **Register Dependencies** in UnityConfig
5. **Create Controller** (MVC or API) with dependency injection
6. **Add Views** (for MVC controllers) with appropriate ViewModels
7. **Test Implementation** with unit and integration tests

### Common Pitfalls to Avoid
- **Lazy Loading**: EF 7.0 doesn't support lazy loading; use explicit loading patterns
- **Async/Await**: Always use async patterns for database operations
- **Exception Handling**: Don't let database exceptions bubble up unhandled
- **Validation**: Use data annotations and ModelState validation
- **Security**: Apply appropriate authorization attributes

### Extension Mechanisms
- **Custom Filters**: Create action filters for cross-cutting concerns
- **Custom Model Binders**: For complex parameter binding scenarios
- **Middleware**: Use OWIN middleware for application-wide concerns
- **Dependency Injection**: Use Unity for loose coupling and testability

## Conclusion

The PartsUnlimited application follows a traditional .NET MVC layered architecture with clear separation of concerns. Key patterns to follow when implementing new features:

1. **Use Repository Pattern** for data access abstraction
2. **Apply Dependency Injection** for loose coupling
3. **Follow Async Patterns** for all database operations
4. **Implement Proper Error Handling** at each layer
5. **Use Data Annotations** for validation
6. **Apply Security Attributes** appropriately
7. **Follow Consistent Naming Conventions** across all components

This documentation serves as a blueprint for implementing similar features while maintaining consistency with the existing codebase architecture and patterns.