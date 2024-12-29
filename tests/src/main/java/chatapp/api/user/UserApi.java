package chatapp.api.user;

import io.restassured.response.Response;

public class UserApi {
    public static Response login(String username, String password) {
        return UserLogin.login(username, password);
    }
}
