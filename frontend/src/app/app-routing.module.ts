import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SetupComponent } from './modules/setup/setup.component';
import { EvaluationComponent } from './modules/evaluation/evaluation.component';

const routes: Routes = [
  {
    path: '',
    component: SetupComponent,
  },
  {
    path: 'eval/repo/:repoId/function/:functionName',
    component: EvaluationComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {
}
