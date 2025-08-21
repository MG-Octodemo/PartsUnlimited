using System;
using System.Configuration;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using PartsUnlimited.Utils;

namespace PartsUnlimited.UnitTests.Utils
{
    [TestClass]
    public class ConfigurationHelpersTests
    {
        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetString_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetString(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetString_WithEmptyName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetString("");
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetString_WithWhitespaceName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetString("   ");
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetInt32_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetInt32(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetBool_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetBool(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetTimeSpan_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetTimeSpan(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetTimeSpanMinutes_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetTimeSpanMinutes(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetTimeSpanSeconds_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetTimeSpanSeconds(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetUri_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetUri(null);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GetType_WithNullName_ThrowsArgumentException()
        {
            // Act & Assert
            ConfigurationHelpers.GetType(null);
        }
    }
}