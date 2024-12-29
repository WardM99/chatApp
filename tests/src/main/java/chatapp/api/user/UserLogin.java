package chatapp.api.user;

import chatapp.api.BaseApi;
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
/*
PreemptiveBasicAuthScheme authScheme = new PreemptiveBasicAuthScheme();
authScheme.setUserName("login");
authScheme.setPassword("password");
RestAssured.authentication = authScheme;
 */
    //.("grant_type=password&username=test.user&password=test123&scope=&client_id=string&client_secret=string")
}
