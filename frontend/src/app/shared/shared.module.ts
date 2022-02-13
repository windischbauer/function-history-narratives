import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OverlaySpinnerComponent } from './components/overlay-spinner/overlay-spinner.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@NgModule({
  declarations: [OverlaySpinnerComponent],
  imports: [
    CommonModule,
    MatProgressSpinnerModule,
  ],
  exports: [
    OverlaySpinnerComponent,
  ],
})
export class SharedModule {
}
