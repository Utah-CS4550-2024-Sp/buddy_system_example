const api = (token) => {
  // generally, you access environment using `process.env`
  // in Vite, you access via `import.meta.env`
  //    - by default only gives access to env variables that
  //      are prefixed with `VITE_`
  // we can access env variables defined outside (eg export VITE_VAR=hi)
  // or defined in a .env file

  const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  // get("/users/me") ~> finish the same way we would with fetch
  const get = (url) => (
    fetch(baseUrl + url, { method: "GET", headers })
  );

  // post("/auth/registration", { username, email, password })
  const post = (url, body) => (
    fetch(
      baseUrl + url,
      {
        method: "POST",
        body: JSON.stringify(body),
        headers,
      },
    )
  );

  // postForm("/auth/token", { username, password })
  const postForm = (url, body) => (
    fetch(
      baseUrl + url,
      {
        method: "POST",
        body: new URLSearchParams(body),
        headers: {
          ...headers,
          "Content-Type": "application/x-www-form-urlencoded",
        },
      },
    )
  );

  return { get, post, postForm };
};

export default api;

