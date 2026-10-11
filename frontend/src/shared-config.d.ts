declare module '../../shared_config.json' {
  const value: {
    api_base_path: string;
    ports: {
      backend: number;
      frontend_web: number;
    };
    auth: {
      storage_key: string;
      login_request: {
        field_names: {
          email: string;
          password: string;
        };
      };
      login_response: {
        token_field: string;
        user_field: string;
      };
    };
    pagination: {
      default_page_size: number;
      max_page_size: number;
    };
    cors_origins: string[];
  };
  export default value;
}
