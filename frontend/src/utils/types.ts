interface UserData {
  id: number;
  email: string;
  name: string;
}

interface UserDataCreate {
  email: string;
  name: string;
}

interface ConnectionData {
  id: string;
  sender_id: number;
  receiver_id: number;
  answered: boolean | null;
}
