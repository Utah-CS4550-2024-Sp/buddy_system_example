import { http, HttpResponse } from "msw";
import { currentUser } from "./fixtures";

const baseUrl = "http://127.0.0.1:8000";

const handlers = [
  http.get(baseUrl + "/users/me", () => (
    HttpResponse.json(currentUser)
  )),
  http.post(baseUrl + "/auth/token", () => (
    HttpResponse.json({
      access_token: "fake access token",
      token_type: "Bearer",
      expires_in: 3600,
    })
  )),
  http.post(baseUrl + "/animals", () => (
    HttpResponse.json({
      meta: { count: 0 },
      animals: [],
    })
  )),
];

export { handlers };

