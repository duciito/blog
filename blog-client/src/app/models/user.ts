export interface User {
  id?: number;
  username: string;
  password?: string;
  first_name: string;
  last_name: string;
  email: string;
  profile_description: string;
  joined_at?: Date;
  token?: string;
}
