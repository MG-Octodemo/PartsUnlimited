using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using PartsUnlimited.Security;

namespace PartsUnlimited.UnitTests.Security
{
    [TestClass]
    public class ConfigurationLoginProviderCredentialsTests
    {
        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void Constructor_WithNullProviderName_ThrowsArgumentException()
        {
            // Act & Assert
            new ConfigurationLoginProviderCredentials(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void Constructor_WithEmptyProviderName_ThrowsArgumentException()
        {
            // Act & Assert
            new ConfigurationLoginProviderCredentials("");
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void Constructor_WithWhitespaceProviderName_ThrowsArgumentException()
        {
            // Act & Assert
            new ConfigurationLoginProviderCredentials("   ");
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void Constructor_WithInvalidCharactersInProviderName_ThrowsArgumentException()
        {
            // Act & Assert - provider name with potential injection characters
            new ConfigurationLoginProviderCredentials("provider.with.dots");
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void Constructor_WithSpecialCharactersInProviderName_ThrowsArgumentException()
        {
            // Act & Assert - provider name with special characters
            new ConfigurationLoginProviderCredentials("provider@domain");
        }
    }
}