using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using PartsUnlimited.Models;
using PartsUnlimited.Utils;

namespace PartsUnlimited.UnitTests.Utils
{
    [TestClass]
    public class PartsUnlimitedDbInitializerTests
    {
        [TestMethod]
        public void GetRainchecks_WithNullStores_ThrowsArgumentNullException()
        {
            // Arrange
            var products = new List<Product> { new Product { ProductId = 1 } };

            // Act & Assert
            Assert.ThrowsException<ArgumentNullException>(() =>
            {
                var result = PartsUnlimitedDbInitializer.GetRainchecks(null, products);
                result.ToList(); // Force enumeration
            });
        }

        [TestMethod]
        public void GetRainchecks_WithNullProducts_ThrowsArgumentNullException()
        {
            // Arrange
            var stores = new List<Store> { new Store { StoreId = 1 } };

            // Act & Assert
            Assert.ThrowsException<ArgumentNullException>(() =>
            {
                var result = PartsUnlimitedDbInitializer.GetRainchecks(stores, null);
                result.ToList(); // Force enumeration
            });
        }

        [TestMethod]
        public void GetRainchecks_WithEmptyProducts_ReturnsEmptyEnumerable()
        {
            // Arrange
            var stores = new List<Store> { new Store { StoreId = 1 } };
            var products = new List<Product>();

            // Act
            var result = PartsUnlimitedDbInitializer.GetRainchecks(stores, products);

            // Assert
            Assert.IsFalse(result.Any());
        }

        [TestMethod]
        public void GetRainchecks_WithValidInputs_GeneratesRainchecks()
        {
            // Arrange
            var stores = new List<Store> 
            { 
                new Store { StoreId = 1 },
                new Store { StoreId = 2 }
            };
            var products = new List<Product> 
            { 
                new Product { ProductId = 1 },
                new Product { ProductId = 2 }
            };

            // Act
            var result = PartsUnlimitedDbInitializer.GetRainchecks(stores, products).ToList();

            // Assert
            Assert.IsTrue(result.Count > 0);
            Assert.IsTrue(result.All(r => r.StoreId > 0));
            Assert.IsTrue(result.All(r => r.ProductId > 0));
            Assert.IsTrue(result.All(r => r.Count > 0));
            Assert.IsTrue(result.All(r => !string.IsNullOrEmpty(r.Name)));
            Assert.IsTrue(result.All(r => r.SalePrice >= 0));
        }

        [TestMethod]
        public void GetRainchecks_WithSameSeed_GeneratesConsistentResults()
        {
            // Arrange
            var stores = new List<Store> { new Store { StoreId = 1 } };
            var products = new List<Product> { new Product { ProductId = 1 } };

            // Act
            var result1 = PartsUnlimitedDbInitializer.GetRainchecks(stores, products).ToList();
            var result2 = PartsUnlimitedDbInitializer.GetRainchecks(stores, products).ToList();

            // Assert - Results should be identical due to deterministic seed
            Assert.AreEqual(result1.Count, result2.Count);
            for (int i = 0; i < result1.Count; i++)
            {
                Assert.AreEqual(result1[i].StoreId, result2[i].StoreId);
                Assert.AreEqual(result1[i].Name, result2[i].Name);
                Assert.AreEqual(result1[i].Count, result2[i].Count);
                Assert.AreEqual(result1[i].ProductId, result2[i].ProductId);
                Assert.AreEqual(result1[i].SalePrice, result2[i].SalePrice);
            }
        }
    }
}