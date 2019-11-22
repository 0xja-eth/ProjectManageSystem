export class ViewSystem {
  static LoadingShown: boolean = false;
  static AlertShown: boolean = false;
  static AlertIconClass: string = '';
  static AlertTitle: string = '';
  static AlertContent: string = '';

  static SuccessIcon: string = 'el-icon-circle-check';
  static ErrorIcon: string = 'el-icon-warning';

  static ShowAlert(title, content, icon=ViewSystem.ErrorIcon) {
    ViewSystem.AlertTitle = title;
    ViewSystem.AlertContent = content;
    ViewSystem.AlertIconClass = icon;
    ViewSystem.AlertShown = true;
  }
  static HideAlert() {
    ViewSystem.AlertShown = false;
  }
  static ShowLoading() {
    ViewSystem.LoadingShown = true;
  }
  static HideLoading() {
    ViewSystem.LoadingShown = false;
  }
}
