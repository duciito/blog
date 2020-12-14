export interface User {
  id: number;
  username: string;
  password: string;
  firstName: string;
  lastName: string;
  email: string;
  profileDescription: string;
  joinedAt: Date;
  token: string;
}
