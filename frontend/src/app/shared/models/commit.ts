import { User } from '@models/user';
import { Snapshot } from '@models/snapshot';

export class Commit {
  id: number;
  // tslint:disable-next-line:variable-name
  rev_string: string;
  user: User;
  // tslint:disable-next-line:variable-name
  full_message: string;
  // tslint:disable-next-line:variable-name
  commit_time: Date;
  // tslint:disable-next-line:variable-name
  snapshot_list: Snapshot[];
  // tslint:disable-next-line:variable-name
  user_id: string | number;
  exploratory?: boolean;
}
