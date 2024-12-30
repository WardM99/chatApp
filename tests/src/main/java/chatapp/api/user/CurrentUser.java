package chatapp.api.user;

import chatapp.api.BaseApi;
import chatapp.dto.User;
import io.restassured.RestAssured;
import io.restassured.response.Response;

class CurrentUser extends BaseApi {
    private static final String url = "http://127.0.0.1/users";

    protected static Response getCurrentUserResponse(String authenticationToken) {
        return RestAssured
                .given(getDefaultAuthorizationGiven(authenticationToken))
                .when()
                .get(url)
                .then()
                .extract()
                .response();
    }

    protected static User getCurrentUserFromResponse(Response response) {
        return response.getBody().as(User.class);
    }

}
