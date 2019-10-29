import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { environment } from './environments/environment';

if (environment.production) {
  enableProdMode();
}

String.prototype['format'] = function () {
  const e = arguments;
  return !!this && this.replace(/\{(\d+)\}/g, function (t, r) {
    return e[r] ? e[r] : t;
  });
};

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
