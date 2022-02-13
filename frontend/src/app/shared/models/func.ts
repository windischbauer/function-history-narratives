import { ChangeType } from '@models/change-type';

export class Func {
  id: number;
  name: string;
  parameters: string;
  body: string;
  // tslint:disable-next-line:variable-name
  commit_rev_string: string;
  // tslint:disable-next-line:variable-name
  change_type?: ChangeType;
  // tslint:disable-next-line:variable-name
  commit_id?: number | string;
  last_commit_time?: Date;
  last_commit_rev?: string;
  commit_count?: number;
}
