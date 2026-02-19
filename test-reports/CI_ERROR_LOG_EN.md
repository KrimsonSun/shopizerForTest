# CI Assignment Error Log (English)

> Record date: 2026-02-18  
> Goal: capture each build/test error step-by-step for assignment evidence (process + issues + handling).

## Logging Rules
- Add one entry for every key step (setup, build, test, push, CI trigger).
- Even when a step succeeds, record it as “Success (no error)” for traceability.
- For failures, always capture: command, exit code, error summary, initial analysis, and next action.

## Error Timeline (Chronological)

### Step 1: Run test via VS Code test tool
- **Action**: run `ProductPricePartitionTest.java`
- **Result**: no actual Java test execution stats (`passed=0 failed=0`)
- **Issue/Observation**: tool did not return real JUnit execution output
- **Initial Analysis**: this tool path did not properly execute Maven/JUnit tests in current project setup
- **Next Action**: switch to Maven CLI (same execution path used by CI)

### Step 2: Run targeted test in sm-core
- **Command**: `./mvnw -pl sm-core -Dtest=ProductPricePartitionTest test`
- **Exit code**: `1`
- **Result**: `BUILD FAILURE`
- **Key error summary**:
  - `Tests run: 21, Failures: 5, Errors: 0, Skipped: 0`
  - Failing tests include:
    - `testPartition5_InvalidNegativePrice`
    - `testPartition5_BoundaryNegative_JustBelowZero`
    - `testPartition6_InvalidDecimalPrecision_ThreeDecimals`
    - `testPartition6_InvalidDecimalPrecision_ExtremeDecimals`
    - `testPartition7_InvalidNullPrice_HandlesGracefully`
- **Additional log signal**: `NullPointerException` from `CacheManagerImpl` appears during startup logs
- **Initial Analysis**: this class currently contains expected failing scenarios (defect-revealing tests), so it is not suitable as a default “must-pass CI gate” test target
- **Next Action**: keep this class as defect evidence; choose a stable CI test subset or fix business logic first

### Step 3: Run targeted test in sm-shop
- **Command**: `./mvnw -pl sm-shop -Dtest=GeneratePasswordTest test`
- **Exit code**: `1`
- **Result**: `BUILD FAILURE`
- **Key error summary**:
  - `Could not resolve dependencies`
  - `Failed to collect dependencies at com.shopizer:sm-core:jar:3.2.5`
  - `Could not transfer artifact ... from/to spring-releases ... : Not authorized`
- **Initial Analysis**:
  - Maven attempted to fetch `com.shopizer:sm-core:3.2.5` from remote `spring-releases`, which is unauthorized;
  - local reactor artifacts were not used/pre-installed for dependency resolution.
- **Next Action (recommended)**:
  - pre-install reactor modules from repo root: `./mvnw -DskipTests install`, then run target tests;
  - or build dependency modules automatically with `-am`: `./mvnw -pl sm-shop -am test`.

### Step 4: Validate sm-core-model module build
- **Command**: `./mvnw -pl sm-core-model test`
- **Exit code**: `0`
- **Result**: `BUILD SUCCESS`
- **Execution summary**: `No tests to run.`
- **Note**: useful as build-proof, but not enough alone to prove test-case execution.

### Step 5: Validate executable tests in sm-core (DataUtils)
- **Command**: `./mvnw -pl sm-core -Dtest=DataUtilsTest test`
- **Exit code**: `0`
- **Result**: `BUILD SUCCESS`
- **Execution summary**: `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`
- **Additional signal**: JaCoCo instrumentation warnings appear for high JDK class version (`Unsupported class file major version 69`), but build still succeeds.
- **Conclusion**: this is a stable baseline command for CI that actually executes tests.

### Step 6: Validate another test target (ShippingMethodDecisionTest)
- **Command**: `./mvnw -pl sm-core -Dtest=ShippingMethodDecisionTest test`
- **Exit code**: `0`
- **Result**: `BUILD SUCCESS`
- **Execution summary**: `Tests run: 1, Failures: 0, Errors: 0, Skipped: 1`
- **Note**: this test is skipped, so it is not ideal as the main evidence of executed test cases.

### Step 7: Reproduce CI command locally (first attempt failed)
- **Command**: `./mvnw -B -ntp -pl sm-core -Dtest=DataUtilsTest test`
- **Exit code**: `1`
- **Result**: `BUILD FAILURE`
- **Key error summary**: `Unable to parse command line options: Unrecognized option: -ntp`
- **Initial Analysis**: project Maven Wrapper is 3.5.2, which does not support `-ntp`.
- **Next Action**: remove `-ntp` from workflow command.

### Step 8: Re-test after command fix
- **Command**: `./mvnw -B -pl sm-core -Dtest=DataUtilsTest test`
- **Exit code**: `0`
- **Result**: `BUILD SUCCESS`
- **Execution summary**: `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`
- **Conclusion**: fixed command is ready for GitHub Actions.

### Step 9: Add CI configuration file
- **File**: `.github/workflows/ci.yml`
- **Core flow**: `checkout` + `setup-java(17)` + `./mvnw -B -pl sm-core -Dtest=DataUtilsTest test`
- **Status**: created and ready to run after push.

### Step 10: First GitHub Actions web run failed (dependency resolution)
- **Symptom**: CI log shows `Could not resolve dependencies ... com.shopizer:sm-core-model ... from/to spring-releases ... Not authorized`
- **Root cause**: workflow built only `sm-core` and did not build required local dependency modules in the same reactor; Maven then tried remote resolution for `sm-core-model` and hit authorization failure.
- **Fix**: update command to `./mvnw -B -pl sm-core -am -Dtest=DataUtilsTest test` so Maven also builds required modules (`-am`).
- **Submission note**: commit this fix and re-run Actions, then capture screenshots for both “failed run” and “fixed successful run”.

---

## Assignment-ready Issue Description Template
- **Issue**: command/step name
- **Symptoms**: key error + screenshot
- **Root-cause hypothesis**: dependency/environment/test data/code defect
- **Resolution attempts**: what was tried and why
- **Outcome**: resolved / unresolved (with next plan)

## To Be Added in Next Runs
- GitHub Actions workflow trigger screenshots
- CI `build` and `test` job log screenshots
- Re-run screenshots after fixes showing successful pipeline
