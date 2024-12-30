package chatapp.glue;

public class BaseStep {
    private final TestContext testContext;

    public BaseStep(TestContext testContext) {
        this.testContext = testContext;
    }

    public TestContext getTestContext() {
        return testContext;
    }
}
