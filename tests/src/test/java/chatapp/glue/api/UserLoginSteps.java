package chatapp.glue.api;

import chatapp.api.user.UserApi;
import chatapp.dto.Login;
import chatapp.glue.BaseStep;
import chatapp.glue.TestContext;
import io.cucumber.java.en.Given;

public class UserLoginSteps extends BaseStep {

    public UserLoginSteps(TestContext testContext) {
        super(testContext);
    }

    @Given("user {string} is logged in")
    public void userIsLoggedIn(String user) {
        Login login = UserApi.getLoginFromResponse(
                UserApi.login(user, "test123")
        );

        getTestContext().setAuthenticationToken(login.token_type + " " + login.access_token);
    }
}
