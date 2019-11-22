
export class ConfigSystem {
  public static UnLength = 16;
  public static PwdLength = [8, 32];
  public static EmailReg = /^[A-Za-z0-9一-龥]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
  public static CodeLength = 6;
  public static CodeSecond = 60;

  public static UnEmpty = "用户名未填写";
  public static UnLong = "用户名不得超过 16 位";

  public static PwdEmpty = "密码未填写";
  public static PwdLong = "密码不得超过 32 位";
  public static PwdShort = "密码不得少于 8 位";

  public static PwdDiff = "两次密码不一致";

  public static EmailEmpty = "邮箱未填写";
  public static EmailInvalid = "邮箱格式不正确";

  public static CodeEmpty = "验证码未填写";
  public static CodeShort = "请正确填写 6 位验证码";

  public static PnLength = 16;
  public static PDescLength = 256;

  public static PnEmpty = "项目名未填写";
  public static PnLong = "项目名不得超过 16 位";

  public static PTypeEmpty = "项目类型未选择";
  public static PTypeError = "项目类型选择错误";

  public static StartDateEmpty = "项目开始日期未选择";

  public static PDescLong = "项目描述过长";

  public static UnknownType = "未知类型";

  public static AddProjectText = "添加项目";
}
