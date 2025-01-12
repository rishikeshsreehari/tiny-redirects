// functions/callback.js
export async function onRequest(context) {
    try {
      // Log the incoming request URL
      console.log("Callback URL:", context.request.url);
      
      const code = new URL(context.request.url).searchParams.get("code");
      console.log("Received code:", code);
  
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
      console.log("Token response:", data);
  
      return new Response(
        `<script>
          console.log("Sending message to opener");
          window.opener.postMessage(
            'authorization:github:success:${JSON.stringify(data)}',
            'https://r1l.in'
          );
          window.close();
        </script>`,
        {
          headers: {
            "Content-Type": "text/html",
          },
        }
      );
    } catch (error) {
      console.error("Error in callback:", error);
      return new Response(`Error: ${error.message}`, { status: 500 });
    }
  }