using System;
using System.Configuration;

namespace PartsUnlimited.Utils
{
    public static class ConfigurationHelpers
    {
        public static Uri GetUri(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            string setting = GetSetting(name);

            try
            {
                return new Uri(setting);
            }
            catch (Exception ex)
            {
                throw new ConfigurationErrorsException(
                    $"Configuration setting '{name}': Unable to parse value as a Uri", ex);
            }
        }

        public static int GetInt32(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            string setting = GetSetting(name);

            if (int.TryParse(setting, out int result))
                return result;

            throw new ConfigurationErrorsException($"Configuration setting '{name}': Unable to parse value as an integer");
        }

        public static string GetString(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            return GetSetting(name);
        }

        public static bool GetBool(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            string setting = GetSetting(name);

            if (bool.TryParse(setting, out bool result))
                return result;

            throw new ConfigurationErrorsException($"Configuration setting '{name}': Unable to parse value as a boolean");
        }

        public static TimeSpan GetTimeSpan(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            string setting = GetSetting(name);

            if (TimeSpan.TryParse(setting, out TimeSpan result))
                return result;

            throw new ConfigurationErrorsException($"Configuration setting '{name}': Unable to parse value as a TimeSpan");
        }

        public static TimeSpan GetTimeSpanMinutes(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            int minutes = GetInt32(name);

            if (minutes <= 0)
            {
                throw new ConfigurationErrorsException($"Configuration setting '{name}': TimeSpan value must be greater than 0 minutes.");
            }

            return TimeSpan.FromMinutes(minutes);
        }

        public static TimeSpan GetTimeSpanSeconds(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            int seconds = GetInt32(name);

            if (seconds <= 0)
            {
                throw new ConfigurationErrorsException($"Configuration setting '{name}': TimeSpan value must be greater than 0 seconds.");
            }

            return TimeSpan.FromSeconds(seconds);
        }

        public static Type GetType(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Configuration setting name cannot be null or empty.", nameof(name));

            string stringType = GetString(name);

            try
            {
                return Type.GetType(stringType, true, true);
            }
            catch (Exception ex)
            {
                throw new ConfigurationErrorsException($"Configuration setting '{name}': Unable to load type", ex);
            }
        }

        private static string GetSetting(string name)
        {
            try
            {
                return ConfigurationManager.AppSettings[name];
            }
            catch (Exception ex)
            {
                throw new ConfigurationErrorsException($"Configuration setting '{name}': Unable to retrieve setting from configuration", ex);
            }
        }
    }
}