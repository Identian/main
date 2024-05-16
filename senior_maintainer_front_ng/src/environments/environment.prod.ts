export const environment = {
  production: true,
  apiConfiguration: {
    apiBaseURI:"https://maintainer.precia.co/api/",
    apiEndPoints:{
      fieldsEndpoint:"maintainer-fields",
      queryVerificatorEndpoint:"query-verificator",
      requestEndpoint:"request"
    }
  },
  azureAuthConfig: {
    clientId: 'client-id',
    authority: 'https://login.microsoftonline.com/tenant',
  }
};
