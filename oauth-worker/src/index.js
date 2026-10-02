/*
 * OAuth broker for Decap CMS (GitHub backend) on Cloudflare Workers.
 *
 * Decap opens {base_url}/auth. We redirect to GitHub's authorize page.
 * GitHub redirects back to {base_url}/callback?code=... (this MUST match the
 * Authorization callback URL registered on the GitHub OAuth App).
 * We exchange the code for an access token and postMessage it back to the
 * Decap window, which completes the login.
 *
 * Required Worker secrets (set in the Cloudflare dashboard, never in code):
 *   GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
 */

const GITHUB_AUTHORIZE = "https://github.com/login/oauth/authorize";
const GITHUB_TOKEN = "https://github.com/login/oauth/access_token";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/auth") {
      const authorizeUrl =
        `${GITHUB_AUTHORIZE}?client_id=${encodeURIComponent(env.GITHUB_CLIENT_ID)}` +
        `&scope=${encodeURIComponent("repo")}`;
      return Response.redirect(authorizeUrl, 302);
    }

    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      if (!code) {
        return new Response("Missing OAuth code.", { status: 400 });
      }

      let token;
      try {
        const tokenRes = await fetch(GITHUB_TOKEN, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            client_id: env.GITHUB_CLIENT_ID,
            client_secret: env.GITHUB_CLIENT_SECRET,
            code,
          }),
        });
        const data = await tokenRes.json();
        token = data.access_token;
      } catch (e) {
        return new Response("Token exchange failed.", { status: 502 });
      }

      if (!token) {
        return new Response("GitHub did not return an access token.", { status: 502 });
      }

      // Decap CMS listens for: authorization:github:success:{"token":"...","provider":"github"}
      const payload = JSON.stringify({ token, provider: "github" });
      const html = `<!doctype html>
<html><head><meta charset="utf-8"><title>Login complete</title></head>
<body><p>Login complete. You can close this window.</p>
<script>
(function () {
  var message = "authorization:github:success:" + ${JSON.stringify(payload)};
  if (window.opener) {
    window.opener.postMessage(message, "*");
  }
})();
</script></body></html>`;
      return new Response(html, {
        headers: { "Content-Type": "text/html; charset=utf-8" },
      });
    }

    return new Response("Not found.", { status: 404 });
  },
};
