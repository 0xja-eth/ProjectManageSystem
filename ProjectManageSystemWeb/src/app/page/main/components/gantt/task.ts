export class Task {
  id: number;
  start: string;
  end: string;
  text: string;
  complete: number;
  chlidren: Task[];
}
