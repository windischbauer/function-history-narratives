export class GraphEdge {
  id?: string | number;
  to?: string | number;
  from?: string | number;

  constructor(id?: string | number, from?: string | number, to?: string | number) {
    if (id) {
      this.id = id;
    }
    if (to) {
      this.to = to;
    }
    if (from) {
      this.from = from;
    }
  }
}
