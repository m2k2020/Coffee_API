/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: "mhbaando.us", // the auth0 domain prefix
    audience: "coffee", // the audience set for the auth0 app
    clientId: "Vvk1BJZHkGe2kRlxxiqkYVcQqjgRVzpq", // the client id generated for the auth0 app
    callbackURL: "http://127.0.0.1:4200", // the base url of the running ionic application.
  },
};

// https://mhbaando.us.auth0.com/authorize?audience=image&scope=SCOPE&response_type=code&client_id=4p6xv7uymgHfCGEExQsIXG4ZLRQSzV9W&redirect_uri=https://localhost:5000/login-result
