// functions/callback.js
export async function onRequest(context) {
    const code = new URL(context.request.url).searchParams.get("code");
    
    // Exchange code for token
    const tokenResponse = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        client_id: context.env.GITHUB_CLIENT_ID,
        client_secret: context.env.GITHUB_CLIENT_SECRET,
        code: code,
      }),
    });
  
    const data = await tokenResponse.json();
    
    // Return the token to the CMS
    return new Response(
      `<script>
        window.opener.postMessage(
          'authorization:github:success:${JSON.stringify(data)}',
          '*'
        );
        window.close();
      </script>`,
      {
        headers: {
          "Content-Type": "text/html",
        },
      }
    );
  }