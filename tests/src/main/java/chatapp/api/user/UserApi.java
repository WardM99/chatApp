package chatapp.api.user;

import chatapp.dto.Login;
import chatapp.dto.User;
import io.restassured.response.Response;

public class UserApi {
    public static Response login(String username, String password) {
        return UserLogin.login(username, password);
    }

    public static Login getLoginFromResponse(Response response) {
        return UserLogin.getLoginFromResponse(response);
    }

    public static Response getCurrentUserResponse(String authenticationToken) {
        return CurrentUser.getCurrentUserResponse(authenticationToken);
    }

    public static User getUserFromResponse(Response response) {
        return CurrentUser.getCurrentUserFromResponse(response);
    }
}
