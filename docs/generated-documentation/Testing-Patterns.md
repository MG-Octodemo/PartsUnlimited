# Testing Patterns Documentation for PartsUnlimited

This document provides comprehensive testing patterns discovered in the PartsUnlimited codebase that can be used as templates for testing similar .NET applications.

## Testing Architecture Overview

The PartsUnlimited application uses the following testing approach:

- **Unit Testing Framework**: MSTest (`Microsoft.VisualStudio.TestTools.UnitTesting`)
- **Mocking Framework**: Moq for creating mock objects
- **Test Data**: FakeDbSet for in-memory Entity Framework testing
- **Test Organization**: Separate test project with mirrors main project structure

## Test Project Structure

```
PartsUnlimited.UnitTests/
├── Controllers/
│   ├── HomeControllerTests.cs
│   └── OrdersControllerTests.cs
├── Utils/
│   └── OrdersQueryTests.cs
├── Recommendations/
│   └── AzureMLFrequentlyBoughtTogetherRecommendationsTests.cs
├── Mocks/
│   ├── MockDataContext.cs
│   ├── MockHttpContext.cs
│   └── TestDbSet.cs
└── Properties/
    └── AssemblyInfo.cs
```

## 1. Controller Testing Patterns

### MVC Controller Unit Test Template

```csharp
[TestClass]
public class HomeControllerTests
{
    [TestMethod]
    public void Home_Index()
    {
        // Arrange
        var controller = new HomeController(new MockDataContext());

        // Act
        ViewResult result = controller.Index() as ViewResult;

        // Assert
        Assert.IsNotNull(result);
        var model = result.Model as HomeViewModel;
        Assert.IsNotNull(model);
        Assert.AreEqual(4, model.TopSellingProducts.Count);
        Assert.IsTrue(model.TopSellingProducts.Any(t => t.ProductId == 1));
        Assert.AreEqual(4, model.NewProducts.Count);
        Assert.AreEqual(4, model.CommunityPosts.Count);
    }
}
```

**Key Testing Patterns:**
- **Arrange-Act-Assert** pattern consistently used
- **Mock dependencies** injected through constructor
- **View result validation** checking both result type and model
- **Collection assertions** using LINQ for specific validations

### API Controller Testing Pattern

```csharp
[TestClass]
public class ProductsControllerTests
{
    private Mock<IPartsUnlimitedContext> mockContext;
    private ProductsController controller;

    [TestInitialize]
    public void Setup()
    {
        mockContext = new Mock<IPartsUnlimitedContext>();
        controller = new ProductsController(mockContext.Object);
    }

    [TestMethod]
    public async Task Get_ValidId_ReturnsProduct()
    {
        // Arrange
        var expectedProduct = new Product { ProductId = 1, Title = "Test Product" };
        var mockDbSet = CreateMockDbSet(new List<Product> { expectedProduct });
        mockContext.Setup(c => c.Products).Returns(mockDbSet.Object);

        // Act
        var result = await controller.Get(1);

        // Assert
        Assert.IsInstanceOfType(result, typeof(OkNegotiatedContentResult<Product>));
        var okResult = result as OkNegotiatedContentResult<Product>;
        Assert.AreEqual(expectedProduct.ProductId, okResult.Content.ProductId);
    }

    [TestMethod]
    public async Task Get_InvalidId_ReturnsNotFound()
    {
        // Arrange
        var mockDbSet = CreateMockDbSet(new List<Product>());
        mockContext.Setup(c => c.Products).Returns(mockDbSet.Object);

        // Act
        var result = await controller.Get(999);

        // Assert
        Assert.IsInstanceOfType(result, typeof(NotFoundResult));
    }

    private Mock<IDbSet<T>> CreateMockDbSet<T>(List<T> data) where T : class
    {
        var queryable = data.AsQueryable();
        var mockSet = new Mock<IDbSet<T>>();
        mockSet.As<IQueryable<T>>().Setup(m => m.Provider).Returns(queryable.Provider);
        mockSet.As<IQueryable<T>>().Setup(m => m.Expression).Returns(queryable.Expression);
        mockSet.As<IQueryable<T>>().Setup(m => m.ElementType).Returns(queryable.ElementType);
        mockSet.As<IQueryable<T>>().Setup(m => m.GetEnumerator()).Returns(queryable.GetEnumerator());
        return mockSet;
    }
}
```

## 2. Repository Testing Patterns

### Repository Unit Test with Mock Context

```csharp
[TestClass]
public class OrdersQueryTests
{
    private Mock<IPartsUnlimitedContext> mockContext;
    private OrdersQuery ordersQuery;

    [TestInitialize]
    public void Setup()
    {
        mockContext = new Mock<IPartsUnlimitedContext>();
        ordersQuery = new OrdersQuery(mockContext.Object);
    }

    [TestMethod]
    public async Task GetOrdersAsync_ValidUsername_ReturnsUserOrders()
    {
        // Arrange
        var username = "testuser";
        var orders = new List<Order>
        {
            new Order { OrderId = 1, Username = username },
            new Order { OrderId = 2, Username = username },
            new Order { OrderId = 3, Username = "otheruser" }
        };
        
        var mockDbSet = CreateMockDbSet(orders);
        mockContext.Setup(c => c.Orders).Returns(mockDbSet.Object);

        // Act
        var result = await ordersQuery.GetOrdersAsync(username);

        // Assert
        Assert.AreEqual(2, result.Count());
        Assert.IsTrue(result.All(o => o.Username == username));
    }

    [TestMethod]
    public async Task AddAsync_ValidOrder_ReturnsOrderId()
    {
        // Arrange
        var order = new Order { Username = "testuser", OrderDate = DateTime.Now };
        var mockDbSet = new Mock<IDbSet<Order>>();
        mockDbSet.Setup(m => m.Add(It.IsAny<Order>())).Returns(order);
        mockContext.Setup(c => c.Orders).Returns(mockDbSet.Object);
        mockContext.Setup(c => c.SaveChangesAsync(It.IsAny<CancellationToken>()))
                  .ReturnsAsync(1);

        // Act
        var result = await ordersQuery.AddAsync(order);

        // Assert
        Assert.AreEqual(order.OrderId, result);
        mockDbSet.Verify(m => m.Add(order), Times.Once);
        mockContext.Verify(c => c.SaveChangesAsync(It.IsAny<CancellationToken>()), Times.Once);
    }
}
```

## 3. Mock Data Context Pattern

### Complete Mock Implementation

```csharp
public class MockDataContext : IPartsUnlimitedContext
{
    public MockDataContext()
    {
        InitProducts();
        InitOrders();
        InitCategories();
    }

    public IDbSet<Product> Products { get; set; }
    public IDbSet<Order> Orders { get; set; }
    public IDbSet<Category> Categories { get; set; }
    public IDbSet<CartItem> CartItems { get; set; }
    public IDbSet<OrderDetail> OrderDetails { get; set; }
    public IDbSet<Raincheck> RainChecks { get; set; }
    public IDbSet<Store> Stores { get; set; }
    public IDbSet<ApplicationUser> Users { get; set; }

    public Task<int> SaveChangesAsync(CancellationToken requestAborted)
    {
        int changes = 0;
        changes += DbSetHelper.IncrementPrimaryKey(p => p.ProductId, Products);
        changes += DbSetHelper.IncrementPrimaryKey(o => o.OrderId, Orders);
        return Task.FromResult(changes);
    }

    private void InitProducts()
    {
        Products = new TestDbSet<Product>();
        Products.Add(CreateProduct(1, 5)); // Product with 5 orders
        Products.Add(CreateProduct(2, 4)); // Product with 4 orders
        Products.Add(CreateProduct(3, 3)); // Product with 3 orders
        Products.Add(CreateProduct(4, 2)); // Product with 2 orders
        Products.Add(CreateProduct(5, 1)); // Product with 1 order
        Products.Add(CreateProduct(6, 0)); // Product with 0 orders
    }

    private static Product CreateProduct(int id, int orderCount)
    {
        var product = new Product()
        {
            ProductId = id,
            Title = $"Product {id}",
            Description = $"Product {id} description",
            Inventory = 2,
            LeadTime = 10,
            Price = 125,
            SalePrice = 125,
            ProductDetails = $"Product {id} details",
            CategoryId = 1,
            SkuNumber = $"SKU-{id}",
            Created = DateTime.Now.AddDays(-id), // Newer products have higher IDs
            OrderDetails = new List<OrderDetail>()
        };

        AddProductOrders(product, orderCount);
        return product;
    }

    private static void AddProductOrders(Product product, int orderCount)
    {
        for (int i = 0; i < orderCount; i++)
        {
            product.OrderDetails.Add(new OrderDetail()
            {
                OrderDetailId = (product.ProductId * 100) + i,
                Count = 1,
                UnitPrice = 125,
                ProductId = product.ProductId
            });
        }
    }

    public void Dispose() { /* no-op for testing */ }
    public DbEntityEntry Entry(object entity) => throw new NotImplementedException();
}
```

## 4. Test Data Management Patterns

### Test Data Builder Pattern

```csharp
public class ProductBuilder
{
    private Product product;

    public ProductBuilder()
    {
        product = new Product
        {
            ProductId = 1,
            Title = "Default Product",
            Price = 100,
            SalePrice = 100,
            Inventory = 10,
            Created = DateTime.Now
        };
    }

    public ProductBuilder WithId(int id)
    {
        product.ProductId = id;
        return this;
    }

    public ProductBuilder WithTitle(string title)
    {
        product.Title = title;
        return this;
    }

    public ProductBuilder WithPrice(decimal price, decimal? salePrice = null)
    {
        product.Price = price;
        product.SalePrice = salePrice ?? price;
        return this;
    }

    public ProductBuilder OnSale(decimal salePrice)
    {
        product.SalePrice = salePrice;
        return this;
    }

    public ProductBuilder WithOrders(int orderCount)
    {
        product.OrderDetails = new List<OrderDetail>();
        for (int i = 0; i < orderCount; i++)
        {
            product.OrderDetails.Add(new OrderDetail
            {
                OrderDetailId = i + 1,
                ProductId = product.ProductId,
                Count = 1,
                UnitPrice = product.Price
            });
        }
        return this;
    }

    public Product Build() => product;
}

// Usage in tests:
var product = new ProductBuilder()
    .WithId(1)
    .WithTitle("Test Product")
    .WithPrice(100, 80)
    .WithOrders(5)
    .Build();
```

## 5. Integration Testing Patterns

### Test Database Setup

```csharp
[TestClass]
public class ProductsControllerIntegrationTests
{
    private PartsUnlimitedContext context;
    private ProductsController controller;

    [TestInitialize]
    public void Setup()
    {
        // Use in-memory database for integration tests
        var connection = Effort.DbConnectionFactory.CreateTransient();
        context = new PartsUnlimitedContext(connection);
        controller = new ProductsController(context);
        
        SeedTestData();
    }

    [TestCleanup]
    public void Cleanup()
    {
        context?.Dispose();
    }

    private void SeedTestData()
    {
        var category = new Category { CategoryId = 1, Name = "Test Category" };
        context.Categories.Add(category);

        var products = new List<Product>
        {
            new Product { ProductId = 1, Title = "Product 1", CategoryId = 1, Price = 100 },
            new Product { ProductId = 2, Title = "Product 2", CategoryId = 1, Price = 150 }
        };
        
        context.Products.AddRange(products);
        context.SaveChanges();
    }

    [TestMethod]
    public async Task Get_AllProducts_ReturnsAllSeededProducts()
    {
        // Act
        var result = controller.Get();

        // Assert
        Assert.AreEqual(2, result.Count());
    }
}
```

## 6. Performance Testing Patterns

### Caching Behavior Tests

```csharp
[TestClass]
public class StoreControllerCachingTests
{
    [TestMethod]
    public void Details_SecondCall_UsesCache()
    {
        // Arrange
        var mockContext = new Mock<IPartsUnlimitedContext>();
        var controller = new StoreController(mockContext.Object);
        var productId = 1;
        
        // Clear any existing cache
        MemoryCache.Default.Remove($"product_{productId}");
        
        var product = new Product { ProductId = productId, Title = "Test Product" };
        mockContext.Setup(c => c.Products.Single(It.IsAny<Expression<Func<Product, bool>>>()))
                   .Returns(product);

        // Act - First call should hit database
        var result1 = controller.Details(productId);
        
        // Act - Second call should use cache
        var result2 = controller.Details(productId);

        // Assert
        mockContext.Verify(c => c.Products.Single(It.IsAny<Expression<Func<Product, bool>>>()), 
                          Times.Once, "Database should only be called once due to caching");
        
        Assert.IsInstanceOfType(result1, typeof(ViewResult));
        Assert.IsInstanceOfType(result2, typeof(ViewResult));
    }
}
```

## 7. Error Handling Testing Patterns

### Exception Testing

```csharp
[TestClass]
public class RaincheckQueryErrorTests
{
    [TestMethod]
    public async Task FindAsync_NonExistentId_ThrowsArgumentOutOfRangeException()
    {
        // Arrange
        var mockContext = new Mock<IPartsUnlimitedContext>();
        var mockDbSet = new Mock<IDbSet<Raincheck>>();
        
        mockDbSet.Setup(m => m.FirstOrDefaultAsync(It.IsAny<Expression<Func<Raincheck, bool>>>()))
                 .ReturnsAsync((Raincheck)null);
        
        mockContext.Setup(c => c.RainChecks).Returns(mockDbSet.Object);
        
        var query = new RaincheckQuery(mockContext.Object);

        // Act & Assert
        await Assert.ThrowsExceptionAsync<ArgumentOutOfRangeException>(
            () => query.FindAsync(999)
        );
    }

    [TestMethod]
    public async Task AddAsync_DatabaseError_PropagatesException()
    {
        // Arrange
        var mockContext = new Mock<IPartsUnlimitedContext>();
        var mockDbSet = new Mock<IDbSet<Raincheck>>();
        
        mockDbSet.Setup(m => m.Add(It.IsAny<Raincheck>()))
                 .Returns(new Raincheck { RaincheckId = 1 });
        
        mockContext.Setup(c => c.RainChecks).Returns(mockDbSet.Object);
        mockContext.Setup(c => c.SaveChangesAsync(It.IsAny<CancellationToken>()))
                   .ThrowsAsync(new InvalidOperationException("Database connection failed"));
        
        var query = new RaincheckQuery(mockContext.Object);
        var raincheck = new Raincheck();

        // Act & Assert
        await Assert.ThrowsExceptionAsync<InvalidOperationException>(
            () => query.AddAsync(raincheck)
        );
    }
}
```

## 8. Test Organization Best Practices

### Test Categories and Traits

```csharp
[TestClass]
[TestCategory("Unit")]
public class ProductServiceTests
{
    [TestMethod]
    [TestCategory("Fast")]
    public void CalculateDiscount_ValidInput_ReturnsCorrectAmount()
    {
        // Fast unit test
    }
}

[TestClass]
[TestCategory("Integration")]
public class ProductServiceIntegrationTests
{
    [TestMethod]
    [TestCategory("Slow")]
    public async Task SaveProduct_ValidProduct_PersistsToDatabase()
    {
        // Slower integration test
    }
}
```

### Parameterized Tests

```csharp
[TestClass]
public class PriceCalculationTests
{
    [TestMethod]
    [DataRow(100, 0.1, 90)]
    [DataRow(50, 0.2, 40)]
    [DataRow(200, 0.05, 190)]
    public void CalculateSalePrice_VariousDiscounts_ReturnsCorrectPrice(
        decimal originalPrice, decimal discountPercent, decimal expectedPrice)
    {
        // Arrange
        var product = new Product { Price = originalPrice };
        
        // Act
        var result = PriceCalculator.CalculateSalePrice(product, discountPercent);
        
        // Assert
        Assert.AreEqual(expectedPrice, result);
    }
}
```

## Summary

The PartsUnlimited testing patterns demonstrate comprehensive testing strategies:

1. **Unit Tests**: Fast, isolated tests with mocked dependencies
2. **Integration Tests**: Tests with real database interactions
3. **Mock Data**: Consistent test data setup with builder patterns
4. **Error Testing**: Exception scenarios and edge cases
5. **Performance Testing**: Caching behavior validation
6. **Parameterized Tests**: Data-driven test scenarios

These patterns provide a solid foundation for testing similar .NET applications with Entity Framework, dependency injection, and layered architecture.