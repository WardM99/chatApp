package chatapp.glue.api;

import chatapp.api.user.UserApi;
import chatapp.dto.User;
import chatapp.glue.BaseStep;
import chatapp.glue.TestContext;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class UserSteps extends BaseStep {
    public UserSteps(TestContext testContext) {
        super(testContext);
    }

    @When("info about current user is asked")
    public void infoAboutCurrentUserIsAsked() {
        getTestContext().setResponse(
                UserApi.getCurrentUserResponse(getTestContext().getAuthenticationToken())
        );
    }

    @Then("the current user is {string}")
    public void theCurrentUserIs(String expectedCurrentUserName) {
        User currentUser = UserApi.getUserFromResponse(getTestContext().getResponse());
        assertEquals(expectedCurrentUserName, currentUser.name);
    }
}
