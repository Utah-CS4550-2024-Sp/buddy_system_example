const api = (token) => {
  const baseUrl = "http://127.0.0.1:8000";

  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  const get = (url) => (
    fetch(baseUrl + url, { method: "GET", headers, })
  );

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

