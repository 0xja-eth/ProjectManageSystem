class InputConfig {
  placeholder?: string = "请输入内容";
  maxLength?: number | string = 0;
  password?: boolean = false;
  button?: string;
}

export class InputData {
  constructor(public text: string, public value: string,
              public type: "Text" | "Password" = "Text",
              public config: InputConfig) {}
}
