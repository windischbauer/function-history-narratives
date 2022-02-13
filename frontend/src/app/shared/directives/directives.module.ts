import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SelectNodeDirective } from './select-node.directive';


@NgModule({
  declarations: [SelectNodeDirective],
  imports: [
    CommonModule,
  ],
  exports: [SelectNodeDirective],
})
export class DirectivesModule {
}
