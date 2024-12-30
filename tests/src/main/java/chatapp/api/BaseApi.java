package chatapp.api;

import io.restassured.RestAssured;
import io.restassured.specification.RequestSpecification;

public class BaseApi {
    public static RequestSpecification getDefaultAuthorizationGiven(String authorization) {
        return getDefaultGiven()
                .header("Authorization", authorization);
    }

    public static RequestSpecification getDefaultGiven() {
        return RestAssured
                .given()
                .relaxedHTTPSValidation()
                .accept("application/json");
    }
}
