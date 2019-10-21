
class Message {
  speaker: string;
  content: string;
}

export class Chat {
  id: number;
  name: string;
  msg: Message[];
  group?: boolean;
}
