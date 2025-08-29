# PartsUnlimited End-to-End Workflow Documentation

This document provides comprehensive documentation for 4 representative end-to-end workflows in the PartsUnlimited application that can serve as implementation templates for similar features.

## Technology Stack Detection

**Primary Technology**: .NET Framework 4.5.1 with ASP.NET MVC 5
**Architecture Pattern**: Layered Architecture with Repository Pattern
**Persistence**: SQL Database with Entity Framework 6
**Dependency Injection**: Unity Container
**Entry Points**: Both Web API and MVC Controllers

## Project Structure Analysis

The PartsUnlimited application follows a traditional layered architecture:

```
├── Controllers/          # MVC Controllers for web UI
├── api/                 # Web API Controllers for REST endpoints  
├── Models/              # Domain models and Entity Framework context
├── Utils/               # Repository implementations and utilities
├── ViewModels/          # View models for MVC views
├── Views/               # Razor views
├── App_Start/           # Application configuration
└── Areas/               # Admin area with separate controllers
```

## Workflow 1: API Product Retrieval

### Overview
**Name**: Product API Retrieval Workflow  
**Business Purpose**: Provides REST API access to product data for external consumers and AJAX calls  
**Triggering Action**: HTTP GET request to `/api/products` or `/api/products/{id}`  
**Files Involved**:
- `/api/ProductsController.cs` - Web API controller
- `/Models/Product.cs` - Product domain model
- `/Models/PartsUnlimitedContext.cs` - Entity Framework context
- `/Models/IPartsUnlimitedContext.cs` - Context interface
- `/App_Start/WebApiConfig.cs` - Web API configuration
- `/App_Start/UnityConfig.cs` - Dependency injection setup

### Entry Point Implementation

**API Controller Class:**
```csharp
[RoutePrefix("api/products")]
public class ProductsController : ApiController
{
    private readonly IPartsUnlimitedContext _context;

    public ProductsController(IPartsUnlimitedContext context)
    {
        _context = context;
    }

    [HttpGet, Route]
    public IEnumerable<Product> Get(bool sale = false)
    {
        if (!sale)
        {
            return _context.Products;
        }
        return _context.Products.Where(p => p.Price != p.SalePrice);
    }

    [HttpGet, Route("{id}")]
    public async Task<IHttpActionResult> Get(int id)
    {
        var product = await _context.Products.FirstOrDefaultAsync(p => p.ProductId == id);
        if (product == null)
        {
            return NotFound();
        }
        return Content(HttpStatusCode.OK, product);
    }
}
```

**Route Configuration:**
- Base route: `/api/products`
- Individual product: `/api/products/{id}`
- Optional query parameter: `?sale=true` for sale products only

### Data Access Implementation

**Entity Framework Context:**
```csharp
public class PartsUnlimitedContext : IdentityDbContext<ApplicationUser>, IPartsUnlimitedContext
{
    public IDbSet<Product> Products { get; set; }
    // ... other DbSets

    protected override void OnModelCreating(DbModelBuilder builder)
    {
        builder.Entity<Product>().HasKey(a => a.ProductId);
        // ... other configurations
        base.OnModelCreating(builder);
    }
}
```

**Product Domain Model:**
```csharp
public class Product
{
    public int ProductId { get; set; }
    public string SkuNumber { get; set; }
    public string Title { get; set; }
    public decimal Price { get; set; }
    public decimal SalePrice { get; set; }
    public string ProductArtUrl { get; set; }
    public int CategoryId { get; set; }
    public string Description { get; set; }
    public DateTime Created { get; set; }
    public string ProductDetails { get; set; }
    public int Inventory { get; set; }
    public int LeadTime { get; set; }
    public int RecommendationId { get; set; }
    
    public virtual Category Category { get; set; }
    public virtual List<OrderDetail> OrderDetails { get; set; }
}
```

### Response Construction

The API returns:
- **Collection endpoint**: `IEnumerable<Product>` - automatically serialized to JSON
- **Single product endpoint**: `IHttpActionResult` with `HttpStatusCode.OK` and product data, or `NotFound()` for non-existent products

### Error Handling Patterns

```csharp
public async Task<IHttpActionResult> Get(int id)
{
    var product = await _context.Products.FirstOrDefaultAsync(p => p.ProductId == id);
    if (product == null)
    {
        return NotFound();  // Returns 404 status code
    }
    return Content(HttpStatusCode.OK, product);
}
```

### Dependency Injection Configuration

**Unity Container Registration:**
```csharp
public class UnityConfig
{
    public static UnityContainer BuildContainer()
    {
        var container = new UnityContainer();
        container.RegisterType<IPartsUnlimitedContext, PartsUnlimitedContext>();
        return container;
    }
}
```

**Web API Configuration:**
```csharp
public class WebApiConfig
{
    public static void RegisterWebApi(HttpConfiguration config, IUnityContainer container)
    {
        config.DependencyResolver = new UnityDependencyResolver(container);
        config.MapHttpAttributeRoutes();
    }
}
```

## Workflow 2: Raincheck Management API

### Overview
**Name**: Raincheck Management Workflow  
**Business Purpose**: Manages raincheck requests for out-of-stock products  
**Triggering Action**: HTTP requests to `/api/raincheck` endpoints  
**Files Involved**:
- `/api/RaincheckController.cs` - Web API controller
- `/Utils/IRaincheckQuery.cs` - Repository interface
- `/Utils/RaincheckQuery.cs` - Repository implementation
- `/Models/Raincheck.cs` - Raincheck domain model
- `/Models/Store.cs` - Store domain model

### Entry Point Implementation

**API Controller with Async Operations:**
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

### Service Layer Implementation

**Repository Interface:**
```csharp
public interface IRaincheckQuery
{
    Task<IEnumerable<Raincheck>> GetAllAsync();
    Task<Raincheck> FindAsync(int id);
    Task<int> AddAsync(Raincheck raincheck);
}
```

**Repository Implementation with Lazy Loading Workaround:**
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

    // Lazy loading is not available with EF 7.0, so manual loading is required
    private async Task FillRaincheckValuesAsync(Raincheck raincheck)
    {
        raincheck.IssuerStore = await context.Stores.FirstAsync(s => s.StoreId == raincheck.StoreId);
        raincheck.Product = await context.Products.FirstAsync(p => p.ProductId == raincheck.ProductId);
        raincheck.Product.Category = await context.Categories.FirstAsync(c => c.CategoryId == raincheck.Product.CategoryId);
    }
}
```

### Data Mapping Patterns

The repository handles complex object graph loading due to EF limitations:
1. Load the primary entity from database
2. Manually load related entities (Store, Product, Category)
3. Populate navigation properties

### Asynchronous Processing Patterns

All repository methods use async/await pattern:
- `Task<T>` return types for async operations
- `await` for database calls
- `CancellationToken.None` for save operations

### Error Handling Patterns

```csharp
public async Task<Raincheck> FindAsync(int id)
{
    var raincheck = await context.RainChecks.FirstOrDefaultAsync(r => r.RaincheckId == id);
    
    if (raincheck == null)
    {
        throw new ArgumentOutOfRangeException("id");  // Will result in 500 error
    }
    
    await FillRaincheckValuesAsync(raincheck);
    return raincheck;
}
```

## Workflow 3: Store Product Browsing (MVC)

### Overview
**Name**: Store Product Browsing Workflow  
**Business Purpose**: Displays products by category with caching for performance  
**Triggering Action**: HTTP GET request to `/Store/Browse?categoryId={id}` or `/Store/Details/{id}`  
**Files Involved**:
- `/Controllers/StoreController.cs` - MVC controller
- `/ViewModels/ProductViewModel.cs` - View model
- `/Utils/ConfigurationHelpers.cs` - Configuration utilities
- `/Views/Store/Browse.cshtml` - Razor view
- `/Views/Store/Details.cshtml` - Product detail view

### Entry Point Implementation

**MVC Controller with Caching:**
```csharp
public class StoreController : Controller
{
    private readonly IPartsUnlimitedContext db;

    public StoreController(IPartsUnlimitedContext context)
    {
        db = context;
    }

    public ActionResult Index()
    {
        var genres = db.Categories.ToList();
        return View(genres);
    }

    public ActionResult Browse(int categoryId)
    {
        // Retrieve Category and its Associated Products from database
        var genreModel = db.Categories.Include("Products").Single(g => g.CategoryId == categoryId);
        return View(genreModel);
    }

    public ActionResult Details(int id)
    {
        var productCacheKey = string.Format("product_{0}", id);
        var product = MemoryCache.Default[productCacheKey] as Product;
        
        if (product == null)
        {
            product = db.Products.Single(a => a.ProductId == id);
            // Cache for 10 minutes
            MemoryCache.Default.Add(productCacheKey, product, 
                new CacheItemPolicy { SlidingExpiration = TimeSpan.FromMinutes(10) });
        }
        
        var viewModel = new ProductViewModel
        {
            Product = product,
            ShowRecommendations = ConfigurationHelpers.GetBool("ShowRecommendations")
        };

        return View(viewModel);
    }
}
```

### Data Access Implementation

**Entity Framework Include Pattern:**
```csharp
// Eager loading of related products
var genreModel = db.Categories.Include("Products").Single(g => g.CategoryId == categoryId);
```

**Caching Strategy:**
- Uses `System.Runtime.Caching.MemoryCache`
- Cache key format: `"product_{productId}"`
- Sliding expiration of 10 minutes
- Cache-aside pattern implementation

### View Model Pattern

**ProductViewModel:**
```csharp
public class ProductViewModel
{
    public Product Product { get; set; }
    public bool ShowRecommendations { get; set; }
}
```

**Configuration Integration:**
```csharp
ShowRecommendations = ConfigurationHelpers.GetBool("ShowRecommendations")
```

### Response Construction

Returns `ActionResult` with:
- Model data passed to Razor view
- View automatically selected based on action name
- Configuration-driven feature flags

## Workflow 4: Home Page Data Loading

### Overview
**Name**: Home Page Complex Data Loading Workflow  
**Business Purpose**: Loads and caches multiple data sources for the home page dashboard  
**Triggering Action**: HTTP GET request to `/` or `/Home/Index`  
**Files Involved**:
- `/Controllers/HomeController.cs` - MVC controller
- `/ViewModels/HomeViewModel.cs` - Complex view model
- `/Models/CommunityPost.cs` - Community post model

### Entry Point Implementation

**Complex Controller with Multiple Data Sources:**
```csharp
public class HomeController : Controller
{
    private readonly IPartsUnlimitedContext _db;

    public HomeController(IPartsUnlimitedContext context)
    {
        _db = context;
    }

    public ActionResult Index()
    {
        // Get cached top selling products
        var topSellingProducts = MemoryCache.Default["topselling"] as List<Product>;
        if (topSellingProducts == null)
        {
            topSellingProducts = GetTopSellingProducts(4);
            MemoryCache.Default.Add("topselling", topSellingProducts, 
                new CacheItemPolicy { AbsoluteExpiration = DateTimeOffset.UtcNow.AddMinutes(10) });
        }

        // Get cached new products
        var newProducts = MemoryCache.Default["newarrivals"] as List<Product>;
        if (newProducts == null)
        {
            newProducts = GetNewProducts(4);
            MemoryCache.Default.Add("newarrivals", newProducts, 
                new CacheItemPolicy { AbsoluteExpiration = DateTimeOffset.UtcNow.AddMinutes(10) });
        }

        var viewModel = new HomeViewModel
        {
            NewProducts = newProducts,
            TopSellingProducts = topSellingProducts,
            CommunityPosts = GetCommunityPosts()
        };

        return View(viewModel);
    }
    
    private List<Product> GetTopSellingProducts(int count)
    {
        // Group the order details by product and return the products with the highest count
        return _db.Products
            .OrderByDescending(a => a.OrderDetails.Count())
            .Take(count)
            .ToList();
    }

    private List<Product> GetNewProducts(int count)
    {
        return _db.Products
            .OrderByDescending(a => a.Created)
            .Take(count)
            .ToList();
    }

    private List<CommunityPost> GetCommunityPosts()
    {
        // Returns hardcoded community posts for demo purposes
        return new List<CommunityPost>{
            new CommunityPost {
                Content= "Lorem ipsum...",
                DatePosted = DateTime.Now,
                Image = "community_1.png",
                Source = CommunitySource.Facebook
            }
            // ... more posts
        };
    }
}
```

### Data Access Implementation

**Multiple Query Patterns:**
1. **Aggregation Query**: `OrderByDescending(a => a.OrderDetails.Count())`
2. **Date-based Query**: `OrderByDescending(a => a.Created)`
3. **Static Data**: Hardcoded community posts

**Advanced Caching Strategy:**
- Different cache keys for different data types
- Absolute expiration (10 minutes)
- Cache-aside pattern for each data source

### View Model Composition

**Complex View Model:**
```csharp
public class HomeViewModel
{
    public List<Product> NewProducts { get; set; }
    public List<Product> TopSellingProducts { get; set; }
    public List<CommunityPost> CommunityPosts { get; set; }
}
```

## Naming Conventions

The PartsUnlimited application follows these consistent patterns:

### Controller Naming
- **MVC Controllers**: `{EntityName}Controller` (e.g., `HomeController`, `StoreController`)
- **API Controllers**: `{EntityName}Controller` in `/api` folder (e.g., `ProductsController`, `RaincheckController`)

### Service/Repository Naming
- **Interfaces**: `I{EntityName}Query` (e.g., `IRaincheckQuery`, `IOrdersQuery`)
- **Implementations**: `{EntityName}Query` (e.g., `RaincheckQuery`, `OrdersQuery`)

### Model Naming
- **Domain Models**: `{EntityName}` (e.g., `Product`, `Order`, `Category`)
- **View Models**: `{Purpose}ViewModel` (e.g., `HomeViewModel`, `ProductViewModel`)
- **Context**: `{ProjectName}Context` (e.g., `PartsUnlimitedContext`)

### Method Naming Patterns
- **CRUD Operations**: `Get`, `GetAll`, `Add`, `Update`, `Delete`
- **Async Methods**: `{MethodName}Async` (e.g., `GetAllAsync`, `FindAsync`)
- **Query Methods**: `Get{EntityName}`, `Find{EntityName}`

### File Organization
- Controllers in `/Controllers` (MVC) and `/api` (Web API)
- Models in `/Models`
- View Models in `/ViewModels`
- Utilities and repositories in `/Utils`
- Configuration in `/App_Start`

## Implementation Templates

### Creating a New API Endpoint

```csharp
[RoutePrefix("api/entityname")]
public class EntityNameController : ApiController
{
    private readonly IEntityNameQuery _query;

    public EntityNameController(IEntityNameQuery query)
    {
        _query = query;
    }

    [HttpGet, Route]
    public async Task<IEnumerable<EntityName>> Get()
    {
        return await _query.GetAllAsync();
    }

    [HttpGet, Route("{id}")]
    public async Task<IHttpActionResult> Get(int id)
    {
        try
        {
            var entity = await _query.FindAsync(id);
            return Content(HttpStatusCode.OK, entity);
        }
        catch (ArgumentOutOfRangeException)
        {
            return NotFound();
        }
    }

    [HttpPost, Route]
    public async Task<IHttpActionResult> Post([FromBody]EntityName entity)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }
        
        var id = await _query.AddAsync(entity);
        return Content(HttpStatusCode.Created, new { Id = id });
    }
}
```

### Creating a New Repository

```csharp
public interface IEntityNameQuery
{
    Task<IEnumerable<EntityName>> GetAllAsync();
    Task<EntityName> FindAsync(int id);
    Task<int> AddAsync(EntityName entity);
}

public class EntityNameQuery : IEntityNameQuery
{
    private readonly IPartsUnlimitedContext context;

    public EntityNameQuery(IPartsUnlimitedContext context)
    {
        this.context = context;
    }

    public async Task<IEnumerable<EntityName>> GetAllAsync()
    {
        return await context.EntityNames.ToListAsync();
    }

    public async Task<EntityName> FindAsync(int id)
    {
        var entity = await context.EntityNames.FirstOrDefaultAsync(e => e.Id == id);
        if (entity == null)
        {
            throw new ArgumentOutOfRangeException("id");
        }
        return entity;
    }

    public async Task<int> AddAsync(EntityName entity)
    {
        var added = context.EntityNames.Add(entity);
        await context.SaveChangesAsync(CancellationToken.None);
        return added.Id;
    }
}
```

### Dependency Injection Registration

```csharp
// In UnityConfig.cs
container.RegisterType<IEntityNameQuery, EntityNameQuery>();
```

### Adding Caching to MVC Controller

```csharp
public ActionResult Details(int id)
{
    var cacheKey = $"entityname_{id}";
    var entity = MemoryCache.Default[cacheKey] as EntityName;
    
    if (entity == null)
    {
        entity = repository.Find(id);
        MemoryCache.Default.Add(cacheKey, entity, 
            new CacheItemPolicy { SlidingExpiration = TimeSpan.FromMinutes(10) });
    }
    
    return View(entity);
}
```

## Implementation Guidelines

### Step-by-Step Implementation Process

1. **Create Domain Model** in `/Models` folder
2. **Add DbSet** to `PartsUnlimitedContext`
3. **Create Repository Interface** in `/Utils` folder
4. **Implement Repository** with async methods
5. **Register Dependencies** in `UnityConfig`
6. **Create API Controller** in `/api` folder (if needed)
7. **Create MVC Controller** in `/Controllers` folder (if needed)
8. **Add Views** in `/Views` folder (for MVC)
9. **Create View Models** in `/ViewModels` (if needed)

### Common Pitfalls to Avoid

1. **Lazy Loading**: EF6 lazy loading may not work properly - manually load related entities
2. **Async/Sync Mixing**: Always use async methods consistently throughout the call chain
3. **Cache Key Conflicts**: Use descriptive, unique cache keys with entity type and ID
4. **Missing Error Handling**: Always handle null returns from database queries
5. **Transaction Scope**: Be careful with `SaveChangesAsync()` calls in repositories

### Extension Mechanisms

1. **Adding New Repositories**: Implement the query interface pattern
2. **Adding New Controllers**: Follow MVC or Web API patterns consistently
3. **Adding Caching**: Use the `MemoryCache.Default` pattern with appropriate expiration
4. **Adding Configuration**: Use `ConfigurationHelpers.GetBool()` pattern
5. **Adding Background Processing**: Consider using recommendation engine pattern

## Conclusion

The PartsUnlimited application demonstrates a mature, layered .NET architecture with clear separation of concerns. Key patterns to follow when implementing new features:

1. **Repository Pattern** for data access with async operations
2. **Dependency Injection** with Unity container for loose coupling
3. **Caching Strategy** using MemoryCache for performance
4. **Error Handling** with appropriate HTTP status codes
5. **Consistent Naming** following established conventions
6. **View Model Pattern** for complex UI data composition

These patterns ensure maintainability, testability, and performance while keeping the codebase consistent and predictable for new developers joining the project.