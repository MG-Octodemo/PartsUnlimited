# Technical Breakdown: Enhanced Shopping Cart

## Architecture Overview

### System Architecture
The Enhanced Shopping Cart feature follows a layered architecture pattern integrated with the existing PartsUnlimited application:

```
┌─────────────────────────────────────────────┐
│               Presentation Layer            │
│  ┌─────────────┐  ┌─────────────────────────┐│
│  │   MVC Views │  │    JavaScript/jQuery   ││
│  │             │  │    Cart Components      ││
│  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│              Application Layer              │
│  ┌─────────────┐  ┌─────────────────────────┐│
│  │ Controllers │  │    Cart Service         ││
│  │             │  │    Pricing Service      ││
│  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│               Business Layer                │
│  ┌─────────────┐  ┌─────────────────────────┐│
│  │   Models    │  │   Business Logic        ││
│  │             │  │   Validation Rules      ││
│  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│                Data Layer                   │
│  ┌─────────────┐  ┌─────────────────────────┐│
│  │ Entity      │  │    SQL Server           ││
│  │ Framework   │  │    Database             ││
│  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────┘
```

### Component Architecture

#### Cart Service Component
**Responsibility**: Core cart business logic and operations
**Technologies**: C#, .NET Framework, Entity Framework
**Key Classes**:
- `CartService`: Main service orchestrator
- `CartRepository`: Data access layer
- `CartValidator`: Business rule validation
- `CartCalculator`: Price and tax calculations

#### Pricing Engine Component
**Responsibility**: Dynamic pricing, discounts, and tax calculations
**Technologies**: C#, External pricing APIs
**Key Classes**:
- `PricingEngine`: Main pricing orchestrator
- `DiscountCalculator`: Discount logic implementation
- `TaxCalculator`: Tax computation by jurisdiction
- `ShippingCalculator`: Shipping cost estimation

#### Session Management Component
**Responsibility**: Cart persistence and user session handling
**Technologies**: ASP.NET Session, Redis Cache, SQL Server
**Key Classes**:
- `SessionManager`: Session lifecycle management
- `CartPersistence`: Cross-session cart storage
- `UserCartMigration`: Guest-to-user cart conversion

## Data Model Design

### Database Schema

#### Cart Tables
```sql
-- Main cart table
CREATE TABLE Carts (
    CartId UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    UserId UNIQUEIDENTIFIER NULL, -- NULL for guest carts
    SessionId NVARCHAR(128) NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ModifiedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ExpiryDate DATETIME2 NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CartStatus NVARCHAR(20) NOT NULL DEFAULT 'Active', -- Active, Abandoned, Converted
    TotalAmount DECIMAL(18,2) NULL,
    TaxAmount DECIMAL(18,2) NULL,
    DiscountAmount DECIMAL(18,2) NULL,
    ShippingAmount DECIMAL(18,2) NULL
);

-- Cart items table
CREATE TABLE CartItems (
    CartItemId UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    CartId UNIQUEIDENTIFIER NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(18,2) NOT NULL,
    LineTotal DECIMAL(18,2) NOT NULL,
    DiscountAmount DECIMAL(18,2) DEFAULT 0,
    AddedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ModifiedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ProductVariantId INT NULL, -- For size, color variants
    CustomOptions NVARCHAR(MAX) NULL, -- JSON for custom options
    
    FOREIGN KEY (CartId) REFERENCES Carts(CartId),
    FOREIGN KEY (ProductId) REFERENCES Products(ProductId)
);

-- Cart discounts and coupons
CREATE TABLE CartDiscounts (
    CartDiscountId UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    CartId UNIQUEIDENTIFIER NOT NULL,
    DiscountCode NVARCHAR(50) NULL,
    DiscountType NVARCHAR(20) NOT NULL, -- Percentage, FixedAmount, FreeShipping
    DiscountValue DECIMAL(18,2) NOT NULL,
    AppliedAmount DECIMAL(18,2) NOT NULL,
    AppliedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    FOREIGN KEY (CartId) REFERENCES Carts(CartId)
);
```

#### Indexes for Performance
```sql
-- Performance optimization indexes
CREATE INDEX IX_Carts_UserId ON Carts(UserId) WHERE UserId IS NOT NULL;
CREATE INDEX IX_Carts_SessionId ON Carts(SessionId);
CREATE INDEX IX_Carts_ExpiryDate ON Carts(ExpiryDate) WHERE IsActive = 1;
CREATE INDEX IX_CartItems_CartId ON CartItems(CartId);
CREATE INDEX IX_CartItems_ProductId ON CartItems(ProductId);
```

### Entity Models

#### Cart Entity
```csharp
public class Cart
{
    public Guid CartId { get; set; }
    public Guid? UserId { get; set; }
    public string SessionId { get; set; }
    public DateTime CreatedDate { get; set; }
    public DateTime ModifiedDate { get; set; }
    public DateTime ExpiryDate { get; set; }
    public bool IsActive { get; set; }
    public CartStatus Status { get; set; }
    public decimal? TotalAmount { get; set; }
    public decimal? TaxAmount { get; set; }
    public decimal? DiscountAmount { get; set; }
    public decimal? ShippingAmount { get; set; }
    
    // Navigation properties
    public virtual ICollection<CartItem> Items { get; set; }
    public virtual ICollection<CartDiscount> Discounts { get; set; }
    public virtual User User { get; set; }
}

public enum CartStatus
{
    Active,
    Abandoned,
    Converted,
    Expired
}
```

#### CartItem Entity
```csharp
public class CartItem
{
    public Guid CartItemId { get; set; }
    public Guid CartId { get; set; }
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal LineTotal { get; set; }
    public decimal DiscountAmount { get; set; }
    public DateTime AddedDate { get; set; }
    public DateTime ModifiedDate { get; set; }
    public int? ProductVariantId { get; set; }
    public string CustomOptions { get; set; } // JSON
    
    // Navigation properties
    public virtual Cart Cart { get; set; }
    public virtual Product Product { get; set; }
    public virtual ProductVariant ProductVariant { get; set; }
}
```

## API Design

### RESTful Cart API Endpoints

#### Cart Operations
```csharp
// GET /api/cart - Get current user's cart
[HttpGet]
public async Task<ActionResult<CartDto>> GetCart()

// POST /api/cart/items - Add item to cart
[HttpPost("items")]
public async Task<ActionResult<CartDto>> AddItem([FromBody] AddCartItemRequest request)

// PUT /api/cart/items/{itemId} - Update cart item
[HttpPut("items/{itemId}")]
public async Task<ActionResult<CartDto>> UpdateItem(Guid itemId, [FromBody] UpdateCartItemRequest request)

// DELETE /api/cart/items/{itemId} - Remove item from cart
[HttpDelete("items/{itemId}")]
public async Task<ActionResult<CartDto>> RemoveItem(Guid itemId)

// POST /api/cart/discounts - Apply discount code
[HttpPost("discounts")]
public async Task<ActionResult<CartDto>> ApplyDiscount([FromBody] ApplyDiscountRequest request)

// DELETE /api/cart/discounts/{discountId} - Remove discount
[HttpDelete("discounts/{discountId}")]
public async Task<ActionResult<CartDto>> RemoveDiscount(Guid discountId)

// POST /api/cart/calculate - Recalculate cart totals
[HttpPost("calculate")]
public async Task<ActionResult<CartDto>> CalculateCart()

// DELETE /api/cart - Clear entire cart
[HttpDelete]
public async Task<ActionResult> ClearCart()
```

#### Request/Response Models
```csharp
public class AddCartItemRequest
{
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public int? ProductVariantId { get; set; }
    public Dictionary<string, object> CustomOptions { get; set; }
}

public class UpdateCartItemRequest
{
    public int Quantity { get; set; }
    public Dictionary<string, object> CustomOptions { get; set; }
}

public class ApplyDiscountRequest
{
    public string DiscountCode { get; set; }
}

public class CartDto
{
    public Guid CartId { get; set; }
    public DateTime CreatedDate { get; set; }
    public DateTime ModifiedDate { get; set; }
    public List<CartItemDto> Items { get; set; }
    public List<CartDiscountDto> Discounts { get; set; }
    public CartTotalsDto Totals { get; set; }
}

public class CartTotalsDto
{
    public decimal SubTotal { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal ShippingAmount { get; set; }
    public decimal Total { get; set; }
}
```

## Service Layer Design

### Cart Service Implementation
```csharp
public interface ICartService
{
    Task<Cart> GetCartAsync(string sessionId, Guid? userId = null);
    Task<Cart> AddItemAsync(Guid cartId, AddCartItemRequest request);
    Task<Cart> UpdateItemAsync(Guid cartId, Guid itemId, UpdateCartItemRequest request);
    Task<Cart> RemoveItemAsync(Guid cartId, Guid itemId);
    Task<Cart> ApplyDiscountAsync(Guid cartId, string discountCode);
    Task<Cart> RemoveDiscountAsync(Guid cartId, Guid discountId);
    Task<Cart> CalculateCartAsync(Guid cartId);
    Task ClearCartAsync(Guid cartId);
    Task<Cart> MergeCartsAsync(string guestSessionId, Guid userId);
    Task CleanupExpiredCartsAsync();
}

public class CartService : ICartService
{
    private readonly ICartRepository _cartRepository;
    private readonly IPricingEngine _pricingEngine;
    private readonly IInventoryService _inventoryService;
    private readonly ILogger<CartService> _logger;

    public CartService(
        ICartRepository cartRepository,
        IPricingEngine pricingEngine,
        IInventoryService inventoryService,
        ILogger<CartService> logger)
    {
        _cartRepository = cartRepository;
        _pricingEngine = pricingEngine;
        _inventoryService = inventoryService;
        _logger = logger;
    }

    public async Task<Cart> AddItemAsync(Guid cartId, AddCartItemRequest request)
    {
        // Validate inventory availability
        var isAvailable = await _inventoryService.CheckAvailabilityAsync(
            request.ProductId, 
            request.Quantity);
        
        if (!isAvailable)
        {
            throw new InsufficientInventoryException(
                $"Product {request.ProductId} does not have sufficient inventory");
        }

        var cart = await _cartRepository.GetCartAsync(cartId);
        var existingItem = cart.Items.FirstOrDefault(i => 
            i.ProductId == request.ProductId && 
            i.ProductVariantId == request.ProductVariantId);

        if (existingItem != null)
        {
            // Update existing item quantity
            existingItem.Quantity += request.Quantity;
            existingItem.ModifiedDate = DateTime.UtcNow;
        }
        else
        {
            // Add new item to cart
            var product = await _productService.GetProductAsync(request.ProductId);
            var cartItem = new CartItem
            {
                CartItemId = Guid.NewGuid(),
                CartId = cartId,
                ProductId = request.ProductId,
                Quantity = request.Quantity,
                UnitPrice = product.Price,
                ProductVariantId = request.ProductVariantId,
                CustomOptions = JsonConvert.SerializeObject(request.CustomOptions),
                AddedDate = DateTime.UtcNow,
                ModifiedDate = DateTime.UtcNow
            };
            
            cart.Items.Add(cartItem);
        }

        // Recalculate cart totals
        await _pricingEngine.CalculateCartAsync(cart);
        
        // Save changes
        await _cartRepository.SaveCartAsync(cart);
        
        return cart;
    }
}
```

### Pricing Engine Implementation
```csharp
public interface IPricingEngine
{
    Task<Cart> CalculateCartAsync(Cart cart);
    Task<decimal> CalculateTaxAsync(Cart cart, Address shippingAddress);
    Task<decimal> CalculateShippingAsync(Cart cart, Address shippingAddress);
    Task<bool> ValidateDiscountAsync(string discountCode, Cart cart);
    Task<decimal> ApplyDiscountAsync(Cart cart, string discountCode);
}

public class PricingEngine : IPricingEngine
{
    private readonly IDiscountService _discountService;
    private readonly ITaxService _taxService;
    private readonly IShippingService _shippingService;

    public async Task<Cart> CalculateCartAsync(Cart cart)
    {
        // Calculate line totals for each item
        foreach (var item in cart.Items)
        {
            item.LineTotal = item.UnitPrice * item.Quantity - item.DiscountAmount;
        }

        // Calculate subtotal
        var subtotal = cart.Items.Sum(i => i.LineTotal);

        // Apply cart-level discounts
        var discountAmount = await CalculateDiscountsAsync(cart);

        // Calculate tax on discounted amount
        var taxableAmount = subtotal - discountAmount;
        var taxAmount = await _taxService.CalculateTaxAsync(taxableAmount, cart.ShippingAddress);

        // Calculate shipping
        var shippingAmount = await _shippingService.CalculateShippingAsync(cart);

        // Apply free shipping discount if applicable
        if (subtotal >= 75) // Free shipping threshold
        {
            shippingAmount = 0;
        }

        // Update cart totals
        cart.TotalAmount = subtotal - discountAmount + taxAmount + shippingAmount;
        cart.TaxAmount = taxAmount;
        cart.DiscountAmount = discountAmount;
        cart.ShippingAmount = shippingAmount;
        cart.ModifiedDate = DateTime.UtcNow;

        return cart;
    }
}
```

## Frontend Implementation

### JavaScript Cart Component
```javascript
class CartManager {
    constructor() {
        this.cartId = null;
        this.items = [];
        this.totals = {};
        this.isLoading = false;
    }

    async addItem(productId, quantity, options = {}) {
        this.setLoading(true);
        try {
            const response = await fetch('/api/cart/items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    productId: productId,
                    quantity: quantity,
                    customOptions: options
                })
            });

            if (response.ok) {
                const cart = await response.json();
                this.updateCart(cart);
                this.showSuccessMessage('Item added to cart');
            } else {
                const error = await response.json();
                this.showErrorMessage(error.message);
            }
        } catch (error) {
            this.showErrorMessage('Failed to add item to cart');
        } finally {
            this.setLoading(false);
        }
    }

    async updateQuantity(itemId, quantity) {
        if (quantity <= 0) {
            return this.removeItem(itemId);
        }

        this.setLoading(true);
        try {
            const response = await fetch(`/api/cart/items/${itemId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    quantity: quantity
                })
            });

            if (response.ok) {
                const cart = await response.json();
                this.updateCart(cart);
            } else {
                const error = await response.json();
                this.showErrorMessage(error.message);
            }
        } catch (error) {
            this.showErrorMessage('Failed to update cart');
        } finally {
            this.setLoading(false);
        }
    }

    updateCart(cart) {
        this.cartId = cart.cartId;
        this.items = cart.items;
        this.totals = cart.totals;
        this.renderCart();
        this.updateCartBadge();
    }

    renderCart() {
        const cartContainer = document.getElementById('cart-container');
        if (!cartContainer) return;

        cartContainer.innerHTML = this.generateCartHTML();
        this.attachEventListeners();
    }

    generateCartHTML() {
        if (this.items.length === 0) {
            return '<div class="empty-cart">Your cart is empty</div>';
        }

        return `
            <div class="cart-items">
                ${this.items.map(item => this.generateItemHTML(item)).join('')}
            </div>
            <div class="cart-totals">
                ${this.generateTotalsHTML()}
            </div>
            <div class="cart-actions">
                <button class="btn btn-primary btn-checkout" onclick="cartManager.proceedToCheckout()">
                    Proceed to Checkout
                </button>
            </div>
        `;
    }
}

// Initialize cart manager
const cartManager = new CartManager();
document.addEventListener('DOMContentLoaded', () => {
    cartManager.loadCart();
});
```

## Performance Optimization

### Caching Strategy
- **Redis Cache**: Session-based cart data with 30-minute TTL
- **Application Cache**: Product pricing data with 5-minute TTL  
- **Browser Cache**: Static cart UI components with 24-hour TTL
- **CDN Cache**: Cart JavaScript/CSS files with 7-day TTL

### Database Optimization
- **Connection Pooling**: 50-connection pool for cart operations
- **Query Optimization**: Indexed queries for cart retrieval
- **Lazy Loading**: Product details loaded on demand
- **Batch Operations**: Bulk cart updates in single transaction

### Frontend Optimization
- **AJAX Operations**: Asynchronous cart updates without page refresh
- **Optimistic Updates**: Immediate UI feedback with rollback on error
- **Debounced Inputs**: Quantity updates debounced to 500ms
- **Progressive Enhancement**: Works without JavaScript for basic operations

## Security Implementation

### Data Protection
- **Input Validation**: Server-side validation for all cart operations
- **SQL Injection Prevention**: Parameterized queries and Entity Framework
- **XSS Prevention**: HTML encoding and Content Security Policy
- **CSRF Protection**: Anti-forgery tokens for state-changing operations

### Authorization
- **Cart Ownership**: Users can only access their own carts
- **Session Validation**: Cart operations validate session ownership
- **Administrative Access**: Admin users can view any cart for support
- **Audit Logging**: All cart modifications logged for security

This technical breakdown provides the foundation for implementing the Enhanced Shopping Cart feature with proper architecture, security, and performance considerations.