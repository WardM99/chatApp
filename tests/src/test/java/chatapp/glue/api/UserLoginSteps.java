package chatapp.glue.api;

import chatapp.api.user.UserApi;
import io.cucumber.java.en.Given;

public class UserLoginSteps {
    @Given("user {string} is logged in")
    public void userIsLoggedIn(String user) {
        System.out.println(UserApi.login(user, "test123").statusCode());
    }
}
