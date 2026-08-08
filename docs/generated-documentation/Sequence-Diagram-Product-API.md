# Sequence Diagram: API Product Retrieval Workflow

This document contains a detailed sequence diagram for the API Product Retrieval workflow in the PartsUnlimited application.

## Workflow: GET /api/products/{id}

```mermaid
sequenceDiagram
    participant Client
    participant IIS
    participant ProductsController
    participant UnityContainer
    participant PartsUnlimitedContext
    participant SqlServer

    Client->>IIS: GET /api/products/123
    IIS->>ProductsController: Route to Get(int id)
    
    Note over ProductsController: Constructor called by Unity DI
    ProductsController->>UnityContainer: Resolve IPartsUnlimitedContext
    UnityContainer->>ProductsController: Return PartsUnlimitedContext instance
    
    ProductsController->>PartsUnlimitedContext: FirstOrDefaultAsync(p => p.ProductId == 123)
    PartsUnlimitedContext->>SqlServer: SELECT * FROM Products WHERE ProductId = 123
    SqlServer-->>PartsUnlimitedContext: Product row data or null
    
    alt Product found
        PartsUnlimitedContext-->>ProductsController: Product entity
        ProductsController->>ProductsController: Content(HttpStatusCode.OK, product)
        ProductsController-->>IIS: IHttpActionResult with 200 OK + JSON
        IIS-->>Client: HTTP 200 + Product JSON
    else Product not found
        PartsUnlimitedContext-->>ProductsController: null
        ProductsController->>ProductsController: NotFound()
        ProductsController-->>IIS: IHttpActionResult with 404
        IIS-->>Client: HTTP 404 Not Found
    end
```

## Workflow: GET /api/products (with sale filter)

```mermaid
sequenceDiagram
    participant Client
    participant IIS
    participant ProductsController
    participant PartsUnlimitedContext
    participant SqlServer

    Client->>IIS: GET /api/products?sale=true
    IIS->>ProductsController: Route to Get(bool sale = true)
    
    ProductsController->>PartsUnlimitedContext: Products.Where(p => p.Price != p.SalePrice)
    PartsUnlimitedContext->>SqlServer: SELECT * FROM Products WHERE Price != SalePrice
    SqlServer-->>PartsUnlimitedContext: Product collection
    PartsUnlimitedContext-->>ProductsController: IEnumerable<Product>
    ProductsController-->>IIS: Product collection as JSON
    IIS-->>Client: HTTP 200 + Products JSON Array
```

## Method Call Details

### ProductsController.Get(int id)

**Method Signature:**
```csharp
public async Task<IHttpActionResult> Get(int id)
```

**Parameters:**
- `id` (int): Product identifier from route parameter

**Return Type:**
- `Task<IHttpActionResult>`: Async task containing HTTP action result

**Internal Calls:**
1. `_context.Products.FirstOrDefaultAsync(p => p.ProductId == id)`
2. Conditional: `NotFound()` or `Content(HttpStatusCode.OK, product)`

### ProductsController.Get(bool sale)

**Method Signature:**
```csharp
public IEnumerable<Product> Get(bool sale = false)
```

**Parameters:**
- `sale` (bool): Optional query parameter to filter sale products

**Return Type:**
- `IEnumerable<Product>`: Collection of products

**Internal Calls:**
1. If `sale == false`: `_context.Products` (all products)
2. If `sale == true`: `_context.Products.Where(p => p.Price != p.SalePrice)`

## Error Paths

### Product Not Found (404)
```mermaid
sequenceDiagram
    participant ProductsController
    participant PartsUnlimitedContext
    participant SqlServer

    ProductsController->>PartsUnlimitedContext: FirstOrDefaultAsync(p => p.ProductId == 999)
    PartsUnlimitedContext->>SqlServer: SELECT * FROM Products WHERE ProductId = 999
    SqlServer-->>PartsUnlimitedContext: null (no rows)
    PartsUnlimitedContext-->>ProductsController: null
    ProductsController->>ProductsController: if (product == null) return NotFound()
    Note over ProductsController: Returns HTTP 404 status
```

### Database Connection Error (500)
```mermaid
sequenceDiagram
    participant ProductsController
    participant PartsUnlimitedContext
    participant SqlServer

    ProductsController->>PartsUnlimitedContext: FirstOrDefaultAsync(...)
    PartsUnlimitedContext->>SqlServer: Database query
    SqlServer-->>PartsUnlimitedContext: SqlException (connection timeout)
    PartsUnlimitedContext-->>ProductsController: Exception propagated
    Note over ProductsController: Exception results in HTTP 500
```

## Performance Considerations

1. **Async Operations**: All database calls use async/await pattern to avoid blocking threads
2. **Query Efficiency**: Simple WHERE clauses with indexed ProductId
3. **No N+1 Problem**: Single query per request
4. **Serialization**: Automatic JSON serialization of Product entities

## Caching Opportunities

While the API endpoints don't implement caching, the MVC controllers in the same application do:

```mermaid
sequenceDiagram
    participant StoreController
    participant MemoryCache
    participant PartsUnlimitedContext

    StoreController->>MemoryCache: Get("product_123")
    MemoryCache-->>StoreController: null (cache miss)
    StoreController->>PartsUnlimitedContext: Products.Single(a => a.ProductId == 123)
    PartsUnlimitedContext-->>StoreController: Product entity
    StoreController->>MemoryCache: Add("product_123", product, 10min expiration)
    StoreController-->>StoreController: Return product to view
```

This caching pattern could be applied to the API controllers for improved performance.