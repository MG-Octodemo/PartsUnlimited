using System;
using System.Linq;
using PartsUnlimited.Utils;

namespace PartsUnlimited.Security
{
    public class ConfigurationLoginProviderCredentials : ILoginProviderCredentials
    {
        public ConfigurationLoginProviderCredentials(string providerName)
        {
            if (string.IsNullOrWhiteSpace(providerName))
                throw new ArgumentException("Provider name cannot be null or empty.", nameof(providerName));

            // Validate provider name to prevent injection attacks
            if (!IsValidProviderName(providerName))
                throw new ArgumentException("Provider name contains invalid characters.", nameof(providerName));

            Key = ConfigurationHelpers.GetString($"Authentication.{providerName}.Key");
            Secret = ConfigurationHelpers.GetString($"Authentication.{providerName}.Secret");

            Use = !string.IsNullOrWhiteSpace(Key) && !string.IsNullOrWhiteSpace(Secret);
        }

        public string Key { get; set; }
        public string Secret { get; set; }
        public bool Use { get; protected set; }

        private static bool IsValidProviderName(string providerName)
        {
            // Only allow alphanumeric characters and underscores to prevent injection
            return providerName.All(c => char.IsLetterOrDigit(c) || c == '_');
        }
    }
}