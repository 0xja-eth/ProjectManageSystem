export class ViewSystem {
  static LoadingShown: boolean = false;
  static AlertShown: boolean = false;
  static AlertIconClass: string = 'el-icon-warning';
  static AlertTitle: string = '';
  static AlertContent: string = '';

  static ShowAlert(title, content, icon='el-icon-warning') {
    ViewSystem.AlertTitle = title;
    ViewSystem.AlertContent = content;
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
