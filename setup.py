import os

project_dir = r"c:\Users\TonyTonyChopper\Desktop\lab_9.7"

def write(path, content):
    full_path = os.path.join(project_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# .gitignore
write(".gitignore", """
target/
.idea/
*.iml
screenshots/
.env
*.log
""")

# .github/workflows/selenium-ci.yml
write(".github/workflows/selenium-ci.yml", """
name: Selenium Test Suite
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
jobs:
  run-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chrome, firefox]
      fail-fast: false
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: maven
      - name: Run Selenium Tests
        run: mvn clean test -Dbrowser=${{ matrix.browser }} -Denv=dev -DsuiteXmlFile=testng-smoke.xml
        env:
          APP_PASSWORD: ${{ secrets.SAUCEDEMO_PASSWORD }}
          APP_USERNAME: ${{ secrets.SAUCEDEMO_USERNAME }}
      - name: Save test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.browser }}
          path: |
            target/surefire-reports/
            target/screenshots/
          retention-days: 30
""")

# .github/workflows/selenium-full.yml
write(".github/workflows/selenium-full.yml", """
name: Full Selenium CI Pipeline
on:
  push:
    branches: [ main, feature/vpbank-payment ]
  pull_request:
    branches: [ main, feature/vpbank-payment ]
  schedule:
    - cron: '0 2 * * 1-5'
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chrome, firefox]
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '17', distribution: 'temurin', cache: maven }
      - name: Run tests
        run: mvn clean test -Dbrowser=${{ matrix.browser }} -DsuiteXmlFile=testng-smoke.xml
        env:
          APP_USERNAME: ${{ secrets.SAUCEDEMO_USERNAME }}
          APP_PASSWORD: ${{ secrets.SAUCEDEMO_PASSWORD }}
      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-${{ matrix.browser }}
          path: target/allure-results/
          
  payment-test:
    if: github.base_ref == 'feature/vpbank-payment'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '17', distribution: 'temurin', cache: maven }
      - name: Run Payment Tests
        run: mvn test -DsuiteXmlFile=testng-payment.xml
        env:
          VPBANK_API_KEY: ${{ secrets.VPBANK_API_KEY }}
          APP_USERNAME: ${{ secrets.SAUCEDEMO_USERNAME }}
          APP_PASSWORD: ${{ secrets.SAUCEDEMO_PASSWORD }}

  publish-report:
    needs: test
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Download results Chrome
        uses: actions/download-artifact@v4
        with: { name: allure-results-chrome, path: allure-results/ }
      - name: Download results Firefox
        uses: actions/download-artifact@v4
        with: { name: allure-results-firefox, path: allure-results/ }
      - name: Publish Allure Report
        uses: simple-elf/allure-report-action@master
        with:
          allure_results: allure-results
          gh_pages: gh-pages
          allure_report: allure-report
""")

# docker-compose.yml
write("docker-compose.yml", """
version: '3.8'
services:
  selenium-hub:
    image: selenium/hub:4.18.1
    container_name: selenium-hub
    ports:
      - "4442:4442"
      - "4443:4443"
      - "4444:4444"
  chrome-node-1:
    image: selenium/node-chrome:4.18.1
    shm_size: 2gb
    depends_on: [ selenium-hub ]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_NODE_MAX_SESSIONS=3
      - SE_NODE_SESSION_TIMEOUT=300
  chrome-node-2:
    image: selenium/node-chrome:4.18.1
    shm_size: 2gb
    depends_on: [ selenium-hub ]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_NODE_MAX_SESSIONS=3
  firefox-node:
    image: selenium/node-firefox:4.18.1
    shm_size: 2gb
    depends_on: [ selenium-hub ]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_NODE_MAX_SESSIONS=2
""")

# DriverFactory.java (add Grid support)
df_content = """package framework.config;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import io.github.bonigarcia.wdm.WebDriverManager;
import java.net.URL;
import java.net.MalformedURLException;
import java.time.Duration;

public class DriverFactory {
    public static WebDriver createDriver(String browser) {
        String gridUrl = System.getProperty("grid.url");
        if (gridUrl != null && !gridUrl.isBlank()) {
            return createRemoteDriver(browser, gridUrl);
        }
        return createLocalDriver(browser);
    }
    
    private static WebDriver createLocalDriver(String browser) {
        boolean isCI = System.getenv("CI") != null;
        return switch (browser.toLowerCase()) {
            case "firefox" -> createFirefoxDriver(isCI);
            default -> createChromeDriver(isCI);
        };
    }

    private static WebDriver createRemoteDriver(String browser, String gridUrl) {
        DesiredCapabilities caps = new DesiredCapabilities();
        caps.setBrowserName(browser.toLowerCase());
        if (browser.equalsIgnoreCase("chrome")) {
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--no-sandbox", "--disable-dev-shm-usage");
            caps.merge(options);
        }
        try {
            URL gridEndpoint = new URL(gridUrl + "/wd/hub");
            RemoteWebDriver driver = new RemoteWebDriver(gridEndpoint, caps);
            driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
            return driver;
        } catch (MalformedURLException e) {
            throw new RuntimeException("Grid URL không hợp lệ: " + gridUrl);
        }
    }

    private static WebDriver createChromeDriver(boolean headless) {
        ChromeOptions options = new ChromeOptions();
        if (headless) {
            options.addArguments("--headless=new");
            options.addArguments("--no-sandbox");
            options.addArguments("--disable-dev-shm-usage");
            options.addArguments("--window-size=1920,1080");
        } else {
            options.addArguments("--start-maximized");
        }
        WebDriverManager.chromedriver().setup();
        return new ChromeDriver(options);
    }

    private static WebDriver createFirefoxDriver(boolean headless) {
        FirefoxOptions options = new FirefoxOptions();
        if (headless) options.addArguments("-headless");
        WebDriverManager.firefoxdriver().setup();
        return new FirefoxDriver(options);
    }
}
"""
write("src/main/java/framework/config/DriverFactory.java", df_content)

# testng-grid.xml
write("testng-grid.xml", """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "http://testng.org/testng-1.0.dtd">
<suite name="Grid Test Suite" parallel="tests" thread-count="4">
  <test name="Chrome - LoginTest">
    <parameter name="browser" value="chrome"/>
    <classes><class name="tests.LoginTest"/></classes>
  </test>
  <test name="Chrome - CartTest">
    <parameter name="browser" value="chrome"/>
    <classes><class name="tests.CartTest"/></classes>
  </test>
  <test name="Firefox - LoginTest">
    <parameter name="browser" value="firefox"/>
    <classes><class name="tests.LoginTest"/></classes>
  </test>
  <test name="Firefox - CartTest">
    <parameter name="browser" value="firefox"/>
    <classes><class name="tests.CartTest"/></classes>
  </test>
</suite>""")

# .env.example
write(".env.example", """# Sao chép file này thành .env rồi điền giá trị thật vào
APP_USERNAME=your_username_here
APP_PASSWORD=your_password_here
BASE_URL=https://www.saucedemo.com""")

print("Done setting up source files!")
