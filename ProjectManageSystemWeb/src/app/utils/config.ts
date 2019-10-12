
var Config = {
  UnLength: 16,
  PwdLength: [8, 32],
  MailReg: /^[A-Za-z0-9一-龥]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
  CodeLength: 6,

  UnEmpty: "用户名未填写",
  UnLong: "用户名不得超过 16 位",

  PwdEmpty: "密码未填写",
  PwdLong: "密码不得超过 32 位",
  PwdShort: "密码不得少于 8 位",

  PwdDiff: "两次密码不一致",

  EmailEmpty: "邮箱未填写",
  EmailInvalid: "邮箱格式不正确",

  CodeEmpty: "验证码未填写",
  CodeShort: "请正确填写 6 位验证码"
};

export { Config }
