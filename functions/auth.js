// functions/auth.js
export async function onRequest(context) {
    const clientId = context.env.GITHUB_CLIENT_ID;
    const redirectUri = new URL("/callback", context.request.url).toString();
    
    return Response.redirect(
      `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo`,
      301
    );
  }