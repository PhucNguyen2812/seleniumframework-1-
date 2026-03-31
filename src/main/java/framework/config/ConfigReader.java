package framework.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public final class ConfigReader {

    private static ConfigReader instance;
    private final Properties props = new Properties();

    private final String env;
    private final String baseUrl;
    private final String browser;
    private final int explicitWait;
    private final int implicitWait;
    private final String screenshotPath;
    private final int retryCount;

    private ConfigReader() {
        this.env = System.getProperty("env", "dev");
        String fileName = "config-" + env + ".properties";

        try (InputStream input = ConfigReader.class.getClassLoader().getResourceAsStream(fileName)) {
            if (input == null) {
                throw new IllegalStateException("Cannot find config file: " + fileName);
            }
            props.load(input);
            // Log active environment for easier troubleshooting in CI/local runs.
            System.out.println("[ConfigReader] Using environment: " + env);
        } catch (IOException e) {
            throw new RuntimeException("Cannot load config file: " + fileName, e);
        }

        this.baseUrl = props.getProperty("base.url");
        this.browser = props.getProperty("browser", "chrome");
        this.explicitWait = parseInt(props.getProperty("explicit.wait"), 15, "explicit.wait");
        this.implicitWait = parseInt(props.getProperty("implicit.wait"), 5, "implicit.wait");
        this.screenshotPath = props.getProperty("screenshot.path", "target/screenshots/");
        this.retryCount = parseInt(props.getProperty("retry.count"), 1, "retry.count");
    }

    // Singleton access point for framework-wide config.
    public static synchronized ConfigReader getInstance() {
        if (instance == null) {
            instance = new ConfigReader();
        }
        return instance;
    }

    public String getBaseUrl() {
        return baseUrl;
    }

    public String getBrowser() {
        return browser;
    }

    public int getExplicitWait() {
        return explicitWait;
    }

    // implicit.wait is loaded and can be reused inside framework setup.
    public int getImplicitWait() {
        return implicitWait;
    }

    public int getRetryCount() {
        return retryCount;
    }

    public String getScreenshotPath() {
        return screenshotPath;
    }

    private int parseInt(String value, int defaultValue, String key) {
        if (value == null || value.isBlank()) {
            return defaultValue;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid number for key: " + key + " -> " + value, e);
        }
    }
}
