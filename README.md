# Lab 9.7 - ConfigReader

## Cach chay

- Moi truong mac dinh (dev):

```bash
mvn test
```

- Moi truong staging:

```bash
mvn test -Denv=staging
```

## Tai sao can nhieu moi truong?

- Cung mot bo test can chay o dev, staging, production-like de kiem tra dung bieu hien tung he thong.
- Moi moi truong co config rieng (URL, wait time, retry) nen can file rieng de de quan ly.

## Tai sao khong hardcode URL trong code?

- Hardcode URL lam test kho tai su dung khi doi moi truong.
- Doi URL bat buoc sua source va build lai, rat bat tien khi chay CI/CD.
- Tach URL ra config giup doi moi truong nhanh, an toan va de bao tri.

## File chinh

- src/main/java/framework/config/ConfigReader.java
- src/main/resources/config-dev.properties
- src/main/resources/config-staging.properties
