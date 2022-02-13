export class Snapshot {
  id: number;
  filename: string;
  content: string;
  editList: string;
  commit_id?: number | string;
}
