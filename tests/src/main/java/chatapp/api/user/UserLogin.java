package chatapp.api.user;

import chatapp.api.BaseApi;
import chatapp.dto.Login;
import io.restassured.RestAssured;
import io.restassured.response.Response;

class UserLogin extends BaseApi {
    private static final String url = "http://127.0.0.1/users/login";

    protected static Response login(String username, String password) {
        return RestAssured
                .given(getDefaultGiven())
                .formParam("username", username)
                .formParam("password", password)
                .when()
                .post(url)
                .then()
                .extract()
                .response();

    }

    protected static Login getLoginFromResponse(Response response) {
        return response.getBody().as(Login.class);
    }
}
