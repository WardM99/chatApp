package chatapp.glue.api;

import chatapp.glue.BaseStep;
import chatapp.glue.TestContext;
import io.cucumber.java.en.Then;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ApiSteps extends BaseStep {
    public ApiSteps(TestContext testContext) {
        super(testContext);
    }

    @Then("the status code is {int}")
    public void theStatusCodeIs(int expectedStatusCode) {
        assertEquals(expectedStatusCode, getTestContext().getResponse().getStatusCode());
    }
}
